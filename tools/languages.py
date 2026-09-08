#!/usr/bin/env python3
"""Répartition des langages sur plusieurs dépôts, en lignes réelles.

Sert à produire les pourcentages du README sans dépendre d'un service tiers
(github-readme-stats ne voit que les dépôts publics, et son instance hébergée
tombe régulièrement). Ici on compte ce qui est sur le disque, dépôts privés
compris.

Usage :
    python3 tools/languages.py ../Colibri ../The-new-MEE6 ../elipse-rsai
    python3 tools/languages.py --json langs.json <chemins...>

Ce qui est exclu : les dossiers d'artefacts (node_modules, .next, dist, build,
coverage, target, vendor…) et tout ce qui n'a pas d'extension reconnue. On
compte des LIGNES, pas des octets : un binaire commité ne peut pas gonfler le
résultat, et un fichier minifié compte pour ce qu'il est — une ligne.
"""
import argparse
import collections
import json
import os
import sys

EXCLUDE_DIRS = {
    "node_modules", ".next", ".git", "dist", "build", "coverage", ".turbo",
    "out", ".venv", "__pycache__", ".gradle", "target", "vendor", ".cache",
}

# Plusieurs extensions peuvent pointer vers un même langage (.ts et .tsx).
LANGUAGES = {
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".dart": "Dart", ".py": "Python", ".java": "Java", ".kt": "Kotlin",
    ".ps1": "PowerShell", ".sh": "Shell", ".bash": "Shell",
    ".sql": "SQL", ".prisma": "Prisma",
    ".css": "HTML / CSS", ".scss": "HTML / CSS", ".html": "HTML / CSS",
    ".php": "PHP", ".rs": "Rust", ".go": "Go", ".c": "C", ".cpp": "C++",
}


def count_repo(path):
    """Lignes par langage pour un dépôt. Les fichiers illisibles sont ignorés."""
    counts = collections.Counter()
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            lang = LANGUAGES.get(os.path.splitext(name)[1].lower())
            if lang is None:
                continue
            try:
                with open(os.path.join(root, name), "rb") as fh:
                    counts[lang] += sum(1 for _ in fh)
            except OSError:
                continue
    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chemins", nargs="+", help="dépôts à parcourir")
    ap.add_argument("--json", help="écrire le résultat dans ce fichier")
    ap.add_argument("--seuil", type=float, default=0.1,
                    help="masquer les langages sous ce pourcentage (défaut 0.1)")
    args = ap.parse_args()

    total = collections.Counter()
    per_repo = {}
    for path in args.chemins:
        if not os.path.isdir(path):
            print(f"ignoré (introuvable) : {path}", file=sys.stderr)
            continue
        counts = count_repo(path)
        per_repo[os.path.basename(os.path.abspath(path))] = dict(counts)
        total += counts

    grand = sum(total.values())
    if not grand:
        print("aucune ligne comptée", file=sys.stderr)
        return 1

    print(f"{len(per_repo)} dépôts  —  {grand:,} lignes".replace(",", " "))
    print("-" * 42)
    for lang, n in total.most_common():
        pct = 100.0 * n / grand
        if pct < args.seuil:
            continue
        print(f"{lang:<14}{n:>9,}".replace(",", " ") + f"{pct:>7.1f} %")

    if args.json:
        payload = {"total_lignes": grand, "par_langage": dict(total),
                   "par_depot": per_repo}
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"\n→ JSON écrit : {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
