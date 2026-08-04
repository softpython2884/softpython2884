#!/usr/bin/env python3
"""
estimate.py — Estimation d'effort et de coût de développement d'un dépôt.

Principe : une moyenne globale de lignes/jour est trompeuse, parce qu'une ligne
de code de paiement (idempotence, webhooks, rapprochement, litiges) ne coûte pas
le même prix qu'une ligne de CRUD. On classe donc chaque fichier dans une ZONE,
et chaque zone a sa propre productivité (lignes retenues par heure de dev senior).

Trois apports par rapport à une estimation au doigt mouillé :
  1. ZONES pondérées      -> où part réellement l'argent.
  2. CHURN git            -> le code écrit puis jeté/réécrit a coûté aussi.
  3. TYPES DE COMMITS     -> part de feature / debug / doc / refonte.

Usage :
    python3 estimate.py <chemin_du_depot> [--nom NOM] [--json fichier.json]
                        [--tjm 600] [--heures-jour 7] [--modules chemin]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

# --------------------------------------------------------------------------
# 1. ZONES — patterns (ordre important : du plus spécifique au plus générique)
#    loc_h = lignes retenues produites par heure par un dev senior (10-11 ans),
#            analyse + écriture + relecture + tests + debug inclus.
# --------------------------------------------------------------------------

ZONES = [
    # (clé, libellé, loc/h, regex sur le chemin en minuscules)
    ("docs", "Documentation & specs", 55, r"\.mdx?$"),
    ("config", "Configuration / boilerplate", 90,
     r"(^|/)(package\.json|package-lock\.json|pnpm-lock\.yaml|yarn\.lock|tsconfig[^/]*\.json|"
     r"next\.config\.[mc]?[jt]s|tailwind\.config\.[jt]s|postcss\.config\.[jt]s|vite\.config\.[jt]s|"
     r"vitest\.config\.[jt]s|\.eslintrc[^/]*|\.prettierrc[^/]*|components\.json|manifest\.webmanifest|"
     r"\.env\.example|pnpm-workspace\.yaml|\.gitignore|\.dockerignore)$"),
    ("tests", "Tests", 45,
     r"(\.(test|spec)\.[jt]sx?$)|(^|/)(tests?|__tests__|e2e)/"),
    ("db", "Modèle de données & migrations", 28,
     r"(\.prisma$)|(\.sql$)|((^|/)(migrations?|tenant-migrations)/)"),
    ("infra", "Infra, DevOps & déploiement", 14,
     r"(^|/)(dockerfile|docker-compose)|(^|/)docker/|caddyfile|(^|/)nginx|"
     r"(^|/)\.github/workflows/|(^|/)scripts?/|\.(sh|ps1|bat)$|(^|/)deploy/|\.toml$|"
     r"(^|/)(prometheus|grafana|loki)"),
    ("compliance", "Juridique & conformité", 6,
     r"factur|(^|/|-)fec(-|/|\.|$)|rgpd|gdpr|duerp|qualiopi|(^|[/-])bpf([/-]|\.|$)|cnil|"
     # NB : « report » et « moderation » ont été retirés — trop génériques : ils
     # attrapaient les commandes de modération Discord de Marcus, qui sont des
     # fonctionnalités produit ordinaires, pas du travail juridique.
     r"legal|conformite|registre|dsa|lcen|mentions|cgv|cgu|privacy|consent|opt-out|"
     r"retention|anonymi|audit-log|auditlog"),
    ("money", "Paiement, facturation & comptabilité", 9,
     r"stripe|billing|invoice|payment|payout|refund|checkout|pricing|subscri|quote|"
     r"accounting|payroll|donation|merchant|wallet|credit|(^|[/-])tax|(^|[/-])fee|"
     r"cart|order|ticketing|pos[-/]|money|clawback|statement|dunning|installment|licence|license|drm"),
    ("security", "Sécurité, auth & cryptographie", 9,
     r"auth|rbac|permission|(^|[/-])acl|crypto|encrypt|decrypt|token|jwt|secret|"
     r"password|session|sanitiz|csrf|totp|signature|hash|guard|rate-limit|ratelimit|"
     r"security|middleware|access|unlock|verify|2fa|argon|bcrypt"),
    ("integration", "Intégrations & services externes", 13,
     r"ovh|(^|[/-])dns|powerdns|(^|[/-])mail|smtp|imap|stalwart|roundcube|jitsi|visio|"
     r"pterodactyl|discord|gemini|genkit|(^|/)ai/|(^|[/-])ai[-.]|webhook|meili|minio|"
     r"(^|[/-])s3|storage|sirene|(^|[/-])ics|(^|[/-])rss|oauth|sso|pubsub|realtime|"
     r"push|sms|brevo|nodemailer|websocket|ffmpeg|canvas|pdf"),
    ("ui", "Interface & composants", 30,
     r"\.(tsx|jsx|css|scss|html|svg)$|(^|/)(components|pages|views|app)/"),
    ("server", "Logique métier serveur", 20,
     r"\.(ts|js|mjs|cjs|py|java)$"),
    ("other", "Divers", 40, r".*"),
]

EXCLUDE_DIRS = {
    "node_modules", ".next", ".git", "dist", "build", "coverage", ".turbo",
    "out", ".venv", "__pycache__", ".gradle", "target", "vendor", ".cache",
}

# Fichiers dont le volume est généré/mécanique : exclus du churn git pour ne pas
# fausser le calcul (un lockfile peut ajouter 15 000 lignes en un commit).
GENERATED = re.compile(
    r"(pnpm-lock\.yaml|package-lock\.json|yarn\.lock|\.min\.(js|css)$|"
    r"(^|/)public/|"                       # assets statiques : le nb de lignes n'est pas un effort
    r"\.svg$|"                             # SVG exportés : 5 logos = 9 664 lignes, à exclure
    r"\.(png|jpg|jpeg|gif|webp|ico|woff2?|pbf|zip|pdf)$)"
)

COMPILED = [(k, lbl, loc_h, re.compile(pat)) for k, lbl, loc_h, pat in ZONES]


def classify(path: str) -> str:
    p = path.lower()
    for key, _lbl, _loc_h, rx in COMPILED:
        if rx.search(p):
            return key
    return "other"


def zone_meta(key: str):
    for k, lbl, loc_h, _rx in ZONES:
        if k == key:
            return lbl, loc_h
    return key, 40


# --------------------------------------------------------------------------
# 2. Scan de l'arbre courant (code RETENU)
# --------------------------------------------------------------------------

def scan_tree(repo: str):
    stats = defaultdict(lambda: {"files": 0, "lines": 0})
    per_module = defaultdict(lambda: {"lines": 0, "hours": 0.0})
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, repo)
            if GENERATED.search(rel.lower()):
                continue
            try:
                if os.path.getsize(full) > 4_000_000:
                    continue
                with open(full, "rb") as fh:
                    raw = fh.read()
                if b"\0" in raw[:2048]:      # binaire
                    continue
                lines = raw.count(b"\n") + (1 if raw and not raw.endswith(b"\n") else 0)
            except (OSError, ValueError):
                continue
            if lines == 0:
                continue
            z = classify(rel)
            stats[z]["files"] += 1
            stats[z]["lines"] += lines
            _lbl, loc_h = zone_meta(z)
            per_module[module_of(rel)]["lines"] += lines
            per_module[module_of(rel)]["hours"] += lines / loc_h
    return stats, per_module


def module_of(rel: str) -> str:
    """Regroupement grossier par grande partie du produit (pour le détail)."""
    p = rel.replace("\\", "/")
    m = re.match(r"src/server/modules/([^/]+)/", p)
    if m:
        return f"module:{m.group(1)}"
    m = re.match(r"(src/app/\([^)]+\)/[^/]+)/", p)
    if m:
        return m.group(1)
    parts = p.split("/")
    return "/".join(parts[:2]) if len(parts) > 1 else parts[0]


# --------------------------------------------------------------------------
# 3. Churn git — le code écrit puis jeté a coûté aussi
# --------------------------------------------------------------------------

def git_churn(repo: str):
    try:
        out = subprocess.run(
            ["git", "-C", repo, "log", "--numstat", "--format=__C__%H", "--no-merges"],
            capture_output=True, text=True, timeout=600,
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return None
    ins = dele = 0
    commits = 0
    for line in out.splitlines():
        if line.startswith("__C__"):
            commits += 1
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        a, d, path = parts
        if a == "-" or d == "-":            # binaire
            continue
        if GENERATED.search(path.lower()):
            continue
        if any(seg in EXCLUDE_DIRS for seg in path.split("/")):
            continue
        ins += int(a)
        dele += int(d)
    return {"commits": commits, "insertions": ins, "deletions": dele}


# --------------------------------------------------------------------------
# 4. Nature du travail d'après les messages de commit
# --------------------------------------------------------------------------

KINDS = [
    # L'ordre compte : un message peut contenir plusieurs signaux, le 1er gagne.
    ("fix", r"^(fix|hotfix|bugfix|correctif)|^\W*(fix|correctif)|\bfixe?s?\b|\bbugs?\b|"
            r"corrig|répare|repare|réparé|resout|résout|\bpatch|régression|regression|"
            r"^retours?\b|\bcassé|casse[rz]?\b|plantage|crash|\berreur"),
    ("docs", r"^docs?\b|^doc\(|^documentation|\bclaude\.md\b|^doc :|readme|changelog|"
             r"^notes? |\bbannière\b"),
    ("refactor", r"^refactor|refonte|réécrit|reecrit|nettoyage|cleanup|simplif|renomm|"
                 r"extrait|factoris|harmonis|unifi"),
    ("test", r"^test[s(:]|^tests? |vitest|playwright|couverture de test"),
    ("chore", r"^chore|^ci[(:]|^build[(:]|^config\b|dépendance|dependance|\bdeps\b|bump|"
              r"\blint\b|\.env|pin \w|docker|install"),
    ("perf", r"^perf|performance|optimis|accélér|acceler"),
    # Livraison de fonctionnalité : très souvent préfixée d'un code de lot maison
    # (RH-4b, Phase 8.A, G3, S-B, COMMS-RICH, FIXES-UX lot F5, BT-6, CRM-3…)
    ("feat", r"^feat|^[A-Z]{1,10}[-.]?\d|^phase\s|^lot\s|\blot\b|ajoute|ajout |nouvelle|"
             r"nouveau|implémente|implemente|livré|livre\b|support de|met en place|"
             r"^[A-Z]{3,12}(-[A-Z]+)*\s*[—:-]"),
]
KINDS_C = [(k, re.compile(p, re.I)) for k, p in KINDS]


def git_kinds(repo: str):
    try:
        out = subprocess.run(
            ["git", "-C", repo, "log", "--format=%s", "--no-merges"],
            capture_output=True, text=True, timeout=300,
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return None
    counts = defaultdict(int)
    total = 0
    for subject in out.splitlines():
        s = subject.strip()
        if not s:
            continue
        total += 1
        for key, rx in KINDS_C:
            if rx.search(s):
                counts[key] += 1
                break
        else:
            counts["autre"] += 1
    return {"total": total, "counts": dict(counts)}


# --------------------------------------------------------------------------
# 4bis. Évolution mois par mois : où est passé l'effort dans le temps
# --------------------------------------------------------------------------

def git_timeline(repo: str):
    """Lignes ajoutées par mois, regroupées en grandes familles de travail."""
    try:
        out = subprocess.run(
            ["git", "-C", repo, "log", "--numstat", "--no-merges",
             "--format=__C__%ad", "--date=format:%Y-%m"],
            capture_output=True, text=True, timeout=600,
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return None

    FAMILY = {
        "docs": "doc", "tests": "test", "infra": "infra", "config": "infra",
        "db": "code", "server": "code", "ui": "code", "other": "code",
        "money": "sensible", "security": "sensible", "compliance": "sensible",
        "integration": "sensible",
    }
    months = defaultdict(lambda: defaultdict(int))
    month = None
    for line in out.splitlines():
        if line.startswith("__C__"):
            month = line[5:].strip()
            continue
        parts = line.split("\t")
        if len(parts) != 3 or month is None:
            continue
        a, _d, path = parts
        if a == "-" or GENERATED.search(path.lower()):
            continue
        if any(seg in EXCLUDE_DIRS for seg in path.split("/")):
            continue
        months[month][FAMILY.get(classify(path), "code")] += int(a)
    return dict(months)


def print_timeline(tl):
    if not tl:
        return
    fams = ["code", "sensible", "doc", "test", "infra"]
    print()
    print("  Évolution (lignes ajoutées par mois) :")
    print(f"    {'mois':<9}{'code':>9}{'sensible':>10}{'doc':>8}{'test':>8}{'infra':>8}   profil")
    for m in sorted(tl):
        row = tl[m]
        tot = sum(row.get(f, 0) for f in fams) or 1
        bar = ""
        for f, ch in zip(fams, "#=.:+"):
            bar += ch * int(round(28 * row.get(f, 0) / tot))
        print(f"    {m:<9}" + "".join(f"{row.get(f, 0):>9,}" if f == 'code'
                                      else f"{row.get(f, 0):>10,}" if f == 'sensible'
                                      else f"{row.get(f, 0):>8,}" for f in fams).replace(",", " ")
              + f"   {bar}")
    print("    légende : # code   = sensible(argent/sécu/légal/intégration)   . doc   : test   + infra")


# --------------------------------------------------------------------------
# 5. Rapport
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--nom", default=None)
    ap.add_argument("--tjm", type=float, default=600.0, help="taux journalier senior (€)")
    ap.add_argument("--heures-jour", type=float, default=7.0, dest="hj")
    ap.add_argument("--overhead", type=float, default=1.20,
                    help="travail sans artefact : ops, décisions produit, déploiements")
    ap.add_argument("--rework", type=float, default=0.5,
                    help="part du code jeté/réécrit facturée (0 = ignoré, 1 = plein tarif)")
    ap.add_argument("--json", default=None)
    ap.add_argument("--modules", type=int, default=0, help="afficher N plus gros ensembles")
    ap.add_argument("--timeline", action="store_true", help="évolution mois par mois")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    name = args.nom or os.path.basename(repo)

    stats, per_module = scan_tree(repo)
    churn = git_churn(repo)
    kinds = git_kinds(repo)
    timeline = git_timeline(repo) if args.timeline else None

    rows = []
    base_hours = 0.0
    total_lines = 0
    for key, lbl, loc_h, _rx in ZONES:
        if key not in stats:
            continue
        lines = stats[key]["lines"]
        files = stats[key]["files"]
        hours = lines / loc_h
        base_hours += hours
        total_lines += lines
        rows.append({"zone": key, "libelle": lbl, "fichiers": files, "lignes": lines,
                     "loc_h": loc_h, "heures": round(hours)})
    rows.sort(key=lambda r: -r["heures"])

    # --- rework : lignes insérées au fil de l'histoire mais absentes de l'arbre
    rework_hours = 0.0
    churn_ratio = None
    if churn and total_lines:
        discarded = max(0, churn["insertions"] - total_lines)
        churn_ratio = churn["insertions"] / total_lines
        avg_loc_h = total_lines / base_hours if base_hours else 25
        rework_hours = (discarded / avg_loc_h) * args.rework

    subtotal = base_hours + rework_hours
    total_hours = subtotal * args.overhead
    days = total_hours / args.hj
    months = days / 20.0
    cost = days * args.tjm

    w = 78
    print("=" * w)
    print(f"  {name}  —  estimation d'effort et de coût")
    print("=" * w)
    print(f"{'Zone':<38}{'Fichiers':>9}{'Lignes':>10}{'L/h':>6}{'Heures':>9}")
    print("-" * w)
    for r in rows:
        print(f"{r['libelle']:<38}{r['fichiers']:>9}{r['lignes']:>10,}"
              f"{r['loc_h']:>6}{r['heures']:>9,}".replace(",", " "))
    print("-" * w)
    print(f"{'CODE RETENU':<38}{sum(r['fichiers'] for r in rows):>9}"
          f"{total_lines:>10,}{'':>6}{round(base_hours):>9,}".replace(",", " "))

    if churn:
        print()
        print(f"  Historique git : {churn['commits']:,} commits, "
              f"{churn['insertions']:,} lignes ajoutées, "
              f"{churn['deletions']:,} supprimées".replace(",", " "))
        if churn_ratio:
            print(f"  Ratio écrit/retenu : {churn_ratio:.2f}x  "
                  f"→ {round(rework_hours):,} h de code réécrit ou abandonné "
                  f"(facturé à {int(args.rework*100)} %)".replace(",", " "))

    print_timeline(timeline)

    if kinds and kinds["total"]:
        print()
        print("  Nature du travail (messages de commit) :")
        order = sorted(kinds["counts"].items(), key=lambda kv: -kv[1])
        for k, v in order:
            pct = 100.0 * v / kinds["total"]
            bar = "#" * int(pct / 2)
            print(f"    {k:<10}{v:>6}  {pct:>5.1f} %  {bar}")

    print()
    print(f"  Sous-total (code + reprise)      {round(subtotal):>10,} h".replace(",", " "))
    print(f"  Overhead x{args.overhead:<22}{round(total_hours - subtotal):>10,} h".replace(",", " "))
    print("  " + "-" * (w - 4))
    print(f"  TOTAL                            {round(total_hours):>10,} h".replace(",", " "))
    print(f"  soit                             {round(days):>10,} j "
          f"({months:.1f} mois-homme)".replace(",", " "))
    print(f"  COÛT à {args.tjm:.0f} €/j{' ' * 18}{round(cost):>10,} €".replace(",", " "))
    print("=" * w)

    if args.modules:
        print(f"\n  Plus gros ensembles ({args.modules}) :")
        top = sorted(per_module.items(), key=lambda kv: -kv[1]["hours"])[:args.modules]
        for mod, d in top:
            j = d["hours"] * args.overhead / args.hj
            print(f"    {mod:<46}{d['lines']:>8,} l  "
                  f"{round(j):>5,} j  {round(j * args.tjm):>9,} €".replace(",", " "))

    if args.json:
        payload = {
            "nom": name, "zones": rows, "lignes_retenues": total_lines,
            "heures_code": round(base_hours), "heures_reprise": round(rework_hours),
            "overhead": args.overhead, "heures_total": round(total_hours),
            "jours": round(days), "mois_homme": round(months, 1),
            "cout_eur": round(cost), "tjm": args.tjm,
            "churn": churn, "commits_par_type": kinds,
        }
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"\n  → JSON écrit : {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
