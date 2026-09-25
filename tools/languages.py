#!/usr/bin/env python3
"""Répartition des langages sur plusieurs dépôts, en lignes réelles.

Sert à produire les pourcentages du README sans dépendre d'un service tiers
(github-readme-stats ne voit que les dépôts publics, et son instance hébergée
tombe régulièrement). Ici on compte ce qui est sur le disque, dépôts privés
compris.

Usage :
    python3 tools/languages.py ../Colibri ../The-new-MEE6 ../elipse-rsai ../fallended
    python3 tools/languages.py --json langs.json <chemins...>

Ce qui est exclu : les dossiers d'artefacts (node_modules, .next, dist, build,
coverage, target, vendor…) et tout ce qui n'a pas d'extension reconnue. Les
noms ambigus (build, dist, out…) ne sont exclus qu'en dehors de src/ : dans un
jeu, src/build/ est le mode construction, pas une sortie de compilation. On
compte des LIGNES, pas des octets : un binaire commité ne peut pas gonfler le
résultat, et un fichier minifié compte pour ce qu'il est — une ligne.
"""
import argparse
import collections
import json
import os
import sys

# Même règle que tools/estimate.py.
ALWAYS_EXCLUDED = {
    "node_modules", ".next", ".git", ".turbo", ".venv", "__pycache__",
    ".gradle", ".cache", ".godot",
}
ARTIFACT_NAMES = {"dist", "build", "out", "coverage", "target", "vendor"}


def excluded_dir(parents, name):
    if name in ALWAYS_EXCLUDED:
        return True
    return name in ARTIFACT_NAMES and "src" not in parents


# Plusieurs extensions peuvent pointer vers un même langage (.ts et .tsx).
LANGUAGES = {
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".dart": "Dart", ".py": "Python", ".java": "Java", ".kt": "Kotlin",
    ".ps1": "PowerShell", ".sh": "Shell", ".bash": "Shell",
    ".sql": "SQL", ".prisma": "Prisma",
    ".css": "HTML / CSS", ".scss": "HTML / CSS", ".html": "HTML / CSS",
    ".php": "PHP", ".rs": "Rust", ".go": "Go", ".c": "C", ".cpp": "C++",
    ".gd": "GDScript", ".gdshader": "GDShader", ".gdshaderinc": "GDShader",
}


def count_repo(path):
    """Lignes par langage pour un dépôt. Les fichiers illisibles sont ignorés."""
    counts = collections.Counter()
    for root, dirs, files in os.walk(path):
        rel_root = os.path.relpath(root, path)
        parents = [] if rel_root == "." else rel_root.split(os.sep)
        dirs[:] = [d for d in dirs if not excluded_dir(parents, d)]
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
