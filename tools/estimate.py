#!/usr/bin/env python3
"""
estimate.py — Estimation d'effort et de coût de développement d'un dépôt.

Principe : une moyenne globale de lignes/jour est trompeuse, parce qu'une ligne
de code de paiement (idempotence, webhooks, rapprochement, litiges) ne coûte pas
le même prix qu'une ligne de CRUD. On classe donc chaque fichier dans une ZONE,
et chaque zone a sa propre productivité (lignes retenues par heure de dev senior).

Quatre apports par rapport à une estimation au doigt mouillé :
  1. ZONES pondérées      -> où part réellement l'argent.
  2. LIGNES qualifiées    -> une ligne vide ne coûte rien, un commentaire se
                             facture au tarif de la documentation (voir 1ter).
  3. CHURN git            -> le code écrit puis jeté/réécrit a coûté aussi.
  4. TYPES DE COMMITS     -> part de feature / debug / doc / refonte.

Un dépôt Godot (project.godot à la racine) est trié avec sa propre table de
zones : voir GODOT_ZONES plus bas, et pourquoi.

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
     r"(^|/)(prometheus|grafana|loki)|(^|/)(android|ios|windows|linux|macos)/|gradle|\.kts$"),
    ("compliance", "Juridique & conformité", 6,
     r"factur|(^|/|-)fec(-|/|\.|$)|rgpd|gdpr|duerp|qualiopi|(^|[/-])bpf([/-]|\.|$)|cnil|"
     # NB : « report » et « moderation » ont été retirés — trop génériques : ils
     # attrapaient les commandes de modération Discord de Marcus, qui sont des
     # fonctionnalités produit ordinaires, pas du travail juridique.
     r"legal|conformite|reglementation|reglementaire|registre|dsa|lcen|mentions|cgv|cgu|privacy|consent|opt-out|"
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
     r"push|sms|brevo|nodemailer|websocket|ffmpeg|canvas|pdf|(^|/)sync/|sauvegarde|backup"),
    ("ui", "Interface & composants", 30,
     r"\.(tsx|jsx|css|scss|html|svg)$|(^|/)(components|pages|views|app|ui|ecrans|composants)/"),
    ("server", "Logique métier serveur", 20,
     r"\.(ts|js|mjs|cjs|py|java|dart|kt)$"),
    ("other", "Divers", 40, r".*"),
]

# Dossiers qui ne contiennent jamais de code écrit à la main.
ALWAYS_EXCLUDED = {
    "node_modules", ".next", ".git", ".turbo", ".venv", "__pycache__",
    ".gradle", ".cache", ".godot",
}
# Noms ambigus : « build » est la sortie d'un bundler dans un projet web, mais
# c'est le mode construction dans le code source d'un jeu (src/build/). On les
# exclut donc partout SAUF sous un dossier src/, où ce sont des sources.
ARTIFACT_NAMES = {"dist", "build", "out", "coverage", "target", "vendor"}


def excluded_dir(parents, name: str) -> bool:
    """`parents` : segments du chemin relatif situés au-dessus du dossier `name`."""
    if name in ALWAYS_EXCLUDED:
        return True
    return name in ARTIFACT_NAMES and "src" not in parents


def path_excluded(path: str) -> bool:
    """Le fichier (chemin relatif au dépôt, séparé par /) est-il sous un dossier exclu ?"""
    segs = path.split("/")[:-1]
    return any(excluded_dir(segs[:i], seg) for i, seg in enumerate(segs))

# Fichiers dont le volume est généré/mécanique : exclus du churn git pour ne pas
# fausser le calcul (un lockfile peut ajouter 15 000 lignes en un commit).
GENERATED = re.compile(
    r"(pnpm-lock\.yaml|package-lock\.json|yarn\.lock|\.min\.(js|css)$|"
    r"(^|/)public/|"                       # assets statiques : le nb de lignes n'est pas un effort
    r"\.svg$|"                             # SVG exportés : 5 logos = 9 664 lignes, à exclure
    r"\.(png|jpg|jpeg|gif|webp|ico|woff2?|pbf|zip|pdf)$)"
)

COMPILED = [(k, lbl, loc_h, re.compile(pat)) for k, lbl, loc_h, pat in ZONES]

# --------------------------------------------------------------------------
# 1bis. Projets Godot — détectés par un project.godot à la racine du dépôt.
#   Les zones à mots-clés ci-dessus décrivent un logiciel de gestion : argent,
#   authentification, conformité, services externes. Un jeu n'en contient pas,
#   et leurs mots-clés y tombent à faux : « verify » y rangeait 77 bancs de test
#   en sécurité à 9 lignes/heure, « merchant » y rangeait le marchand du jeu en
#   facturation. Pour un projet Godot, cette table remplace donc la précédente.
#   Mêmes clés, donc mêmes productivités : seules les règles de tri changent.
# --------------------------------------------------------------------------

GODOT_ZONES = [
    ("docs", r"\.mdx?$"),
    # Sérialisé par l'éditeur bien plus qu'écrit à la main.
    ("config", r"\.(godot|cfg|tscn|tres)$|(^|/)\.gitignore$"),
    # Tout ce qui vérifie le jeu : tests, portes (tools/verify_*), captures et
    # mesures qui les accompagnent, benchmarks, et les labos de scenes/dev/.
    ("tests", r"(^|/)tests?/|(^|/)bench/|(^|/)scenes/dev/|"
              r"(^|/)tools/(verify|shot|measure)_"),
    ("infra", r"(^|/)tools/|(^|/)deploy/|\.(sh|ps1|bat)$"),
    ("ui", r"(^|/)(ui|site)/|\.(html|css)$"),
    # Le jeu lui-même : règles, monde, réseau, rendu, créatures.
    ("server", r"\.(gd|gdshader|gdshaderinc|py)$"),
    ("other", r".*"),
]
COMPILED_GODOT = [(k, re.compile(pat)) for k, pat in GODOT_ZONES]

# Produit par l'éditeur ou par un outil, ou venu de tiers : jamais compté.
GENERATED_GODOT = re.compile(
    r"\.(uid|import|log)$|"          # un .uid par script, un .import par asset
    r"(^|/)files/(pack|sounds)/"      # packs de ressources et sons de tiers
)


def detect_profile(repo: str) -> str:
    return "godot" if os.path.isfile(os.path.join(repo, "project.godot")) else "standard"


def is_generated(path: str, profile: str = "standard") -> bool:
    p = path.lower()
    return bool(GENERATED.search(p)) or (profile == "godot" and bool(GENERATED_GODOT.search(p)))


def classify(path: str, profile: str = "standard") -> str:
    p = path.lower()
    if profile == "godot":
        for key, rx in COMPILED_GODOT:
            if rx.search(p):
                return key
        return "other"
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
# 1ter. Toutes les lignes ne se valent pas
#   Une ligne vide ne coûte rien. Un commentaire s'écrit au rythme d'une
#   documentation, pas à celui du code qu'il explique : le facturer au tarif
#   de la zone gonflait surtout les dépôts très commentés (un quart des lignes
#   de Fallended sont des commentaires). Il est donc compté au tarif « docs »,
#   ou à celui de sa zone quand elle va plus vite (un commentaire de fichier de
#   configuration ne coûte pas plus cher que la configuration elle-même).
#   Détection en début de ligne seulement : un commentaire placé après du code
#   reste compté comme du code, ce qui garde l'erreur du côté haut.
# --------------------------------------------------------------------------

DOC_RATE = 55  # lignes/heure, même valeur que la zone « docs »

C_LIKE_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".dart", ".java", ".kt",
              ".kts", ".scala", ".go", ".rs", ".c", ".h", ".cpp", ".hpp", ".cs",
              ".swift", ".php", ".prisma", ".css", ".scss", ".gdshader", ".gdshaderinc"}
HASH_EXT = {".gd", ".py", ".sh", ".bash", ".ps1", ".rb", ".toml", ".yml", ".yaml"}

# extension -> (préfixes de commentaire de ligne, commentaires /* … */ possibles)
COMMENT_SYNTAX = {ext: ((b"//",), True) for ext in C_LIKE_EXT}
COMMENT_SYNTAX.update({ext: ((b"#",), False) for ext in HASH_EXT})
COMMENT_SYNTAX[".sql"] = ((b"--",), True)


def split_lines(raw: bytes, ext: str):
    """(vides, commentaires, code) d'un fichier. Le total égale le nombre de
    lignes compté partout ailleurs. Sans syntaxe connue, rien n'est commentaire."""
    parts = raw.split(b"\n")
    if parts and parts[-1] == b"":
        parts.pop()
    syntax = COMMENT_SYNTAX.get(ext)
    blank = comments = code = 0
    in_block = False
    for part in parts:
        s = part.strip()
        if not s:
            blank += 1
        elif syntax is None:
            code += 1
        elif in_block:
            comments += 1
            in_block = b"*/" not in s
        elif s.startswith(syntax[0]):
            comments += 1
        elif syntax[1] and s.startswith(b"/*"):
            comments += 1
            in_block = b"*/" not in s[2:]
        else:
            code += 1
    return blank, comments, code


def line_hours(code: int, comments: int, loc_h: float) -> float:
    return code / loc_h + comments / max(loc_h, DOC_RATE)


# --------------------------------------------------------------------------
# 2. Scan de l'arbre courant (code RETENU)
# --------------------------------------------------------------------------

def scan_tree(repo: str, profile: str = "standard"):
    stats = defaultdict(lambda: {"files": 0, "lines": 0, "blank": 0, "comments": 0,
                                 "code": 0, "hours": 0.0})
    per_module = defaultdict(lambda: {"lines": 0, "hours": 0.0})
    for root, dirs, files in os.walk(repo):
        rel_root = os.path.relpath(root, repo)
        parents = [] if rel_root == "." else rel_root.split(os.sep)
        dirs[:] = [d for d in dirs if not excluded_dir(parents, d)]
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, repo).replace(os.sep, "/")
            if is_generated(rel, profile):
                continue
            try:
                if os.path.getsize(full) > 4_000_000:
                    continue
                with open(full, "rb") as fh:
                    raw = fh.read()
                if b"\0" in raw[:2048]:      # binaire
                    continue
            except (OSError, ValueError):
                continue
            blank, comments, code = split_lines(raw, os.path.splitext(fn)[1].lower())
            lines = blank + comments + code
            if lines == 0:
                continue
            z = classify(rel, profile)
            _lbl, loc_h = zone_meta(z)
            hours = line_hours(code, comments, loc_h)
            s = stats[z]
            s["files"] += 1
            s["lines"] += lines
            s["blank"] += blank
            s["comments"] += comments
            s["code"] += code
            s["hours"] += hours
            per_module[module_of(rel)]["lines"] += lines
            per_module[module_of(rel)]["hours"] += hours
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

def git_churn(repo: str, profile: str = "standard"):
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
        if is_generated(path, profile) or path_excluded(path):
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

def git_timeline(repo: str, profile: str = "standard"):
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
        if a == "-" or is_generated(path, profile) or path_excluded(path):
            continue
        months[month][FAMILY.get(classify(path, profile), "code")] += int(a)
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

    profile = detect_profile(repo)
    stats, per_module = scan_tree(repo, profile)
    churn = git_churn(repo, profile)
    kinds = git_kinds(repo)
    timeline = git_timeline(repo, profile) if args.timeline else None

    rows = []
    base_hours = 0.0
    total_lines = total_code = total_comments = total_blank = 0
    for key, lbl, loc_h, _rx in ZONES:
        if key not in stats:
            continue
        s = stats[key]
        base_hours += s["hours"]
        total_lines += s["lines"]
        total_code += s["code"]
        total_comments += s["comments"]
        total_blank += s["blank"]
        rows.append({"zone": key, "libelle": lbl, "fichiers": s["files"],
                     "lignes": s["lines"], "code": s["code"],
                     "commentaires": s["comments"], "vides": s["blank"],
                     "loc_h": loc_h, "heures": round(s["hours"])})
    rows.sort(key=lambda r: -r["heures"])

    # --- rework : lignes insérées au fil de l'histoire mais absentes de l'arbre.
    #     Elles comptent vides et commentaires : on les convertit donc avec le
    #     rythme moyen du dépôt, lignes de toute nature comprises.
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

    def nb(n, width=0):
        """Entier avec une espace pour séparateur de milliers."""
        return f"{n:,}".replace(",", " ").rjust(width)

    w = 96
    print("=" * w)
    print(f"  {name}  —  estimation d'effort et de coût  (table : {profile})")
    print("=" * w)
    print(f"{'Zone':<38}{'Fichiers':>9}{'Lignes':>10}{'dont code':>11}"
          f"{'comment.':>10}{'L/h':>6}{'Heures':>9}")
    print("-" * w)
    for r in rows:
        print(f"{r['libelle']:<38}{r['fichiers']:>9}{nb(r['lignes'], 10)}{nb(r['code'], 11)}"
              f"{nb(r['commentaires'], 10)}{r['loc_h']:>6}{nb(r['heures'], 9)}")
    print("-" * w)
    print(f"{'CODE RETENU':<38}{sum(r['fichiers'] for r in rows):>9}"
          f"{nb(total_lines, 10)}{nb(total_code, 11)}{nb(total_comments, 10)}"
          f"{'':>6}{nb(round(base_hours), 9)}")
    if total_lines:
        print(f"  Lignes vides : {nb(total_blank)} ({100 * total_blank / total_lines:.1f} %), "
              f"non facturées. Commentaires : {100 * total_comments / total_lines:.1f} %, "
              f"au tarif documentation ({DOC_RATE} L/h).")

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
            "nom": name, "profil": profile, "zones": rows, "lignes_retenues": total_lines,
            "lignes_code": total_code, "lignes_commentaires": total_comments,
            "lignes_vides": total_blank,
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
