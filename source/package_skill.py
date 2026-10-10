"""Check the skill and package it as dist/dev-icons.zip for claude.ai uploads.

Run from the repo root:  python source/package_skill.py
Exits with an error (and no zip) if any check fails. GitHub Actions runs the same script.
"""
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "dev-icons"
OUT = ROOT / "dist" / "dev-icons.zip"
MAX_FILES = 200            # claude.ai skill upload limit
MAX_DESCRIPTION = 1024

errors = []


def check(ok, message):
    if not ok:
        errors.append(message)
    return ok


def skill_files():
    """Every file that belongs in the upload: no Python caches."""
    return sorted(
        p for p in SKILL.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    )


def check_frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not check(match, "SKILL.md has no YAML frontmatter"):
        return
    fields = dict(line.split(": ", 1) for line in match.group(1).splitlines() if ": " in line)
    name, description = fields.get("name", ""), fields.get("description", "")
    check(re.fullmatch(r"[a-z0-9-]{1,64}", name), f'skill name "{name}" must be lowercase letters, digits and hyphens')
    check("claude" not in name and "anthropic" not in name, "skill name can't contain claude or anthropic")
    check(0 < len(description) <= MAX_DESCRIPTION, f"description must be 1-{MAX_DESCRIPTION} characters")
    check("<" not in description and ">" not in description, "description can't contain < or >")


def check_versions():
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    check(plugin["version"] == package["version"],
          f'version mismatch: plugin.json {plugin["version"]}, package.json {package["version"]}')
    return plugin["version"]


def smoke_test():
    """Run each script once so a broken skill never gets released."""
    scripts = SKILL / "scripts"
    with tempfile.TemporaryDirectory() as tmp:
        runs = [
            ["find.py", "react", "k8s"],
            ["find.py", "--list"],
            ["compose.py", "react,ts,nodejs", "-o", f"{tmp}/stack.svg"],
            ["export.py", "docker", "--format", "both", "--size", "512", "-o", f"{tmp}/icons"],
            ["animate.py", "react,ts", "-o", f"{tmp}/intro.html"],
        ]
        for script, *args in runs:
            result = subprocess.run([sys.executable, str(scripts / script), *args],
                                    capture_output=True, text=True)
            check(result.returncode == 0, f"{script} {' '.join(args)} failed:\n{result.stderr.strip()}")
        check(Path(tmp, "stack.svg").exists(), "compose.py wrote no output")


def main():
    files = skill_files()
    check((SKILL / "SKILL.md").exists(), "skills/dev-icons/SKILL.md is missing")
    check(len(files) <= MAX_FILES, f"{len(files)} files in the skill, the upload limit is {MAX_FILES}")
    nested = [p.name for p in files if p.suffix.lower() in (".zip", ".skill")]
    check(not nested, f"uploads can't contain archives: {', '.join(nested)}")
    check_frontmatter()
    version = check_versions()
    smoke_test()

    if errors:
        print("FAILED: skill check found problems:")
        for e in errors:
            print("  - " + e)
        sys.exit(1)

    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            # forward slashes and a top-level dev-icons/ folder, as claude.ai expects
            z.write(p, "dev-icons/" + p.relative_to(SKILL).as_posix())
    size = OUT.stat().st_size / 1e6
    print(f"OK: skill v{version} passed all checks ({len(files)} files)")
    print(f"OK: wrote {OUT.relative_to(ROOT).as_posix()} ({size:.1f} MB)")


if __name__ == "__main__":
    main()
