#!/usr/bin/env python3
"""Create a new project from this template.

The generator has no third-party dependencies: plain Python 3.11+ is enough.

Placeholders use double square brackets, for example ``[[ project_name ]]``.
GitHub Actions expressions such as ``${{ secrets.VPS_SSH_KEY }}`` are left
untouched because they do not use the same delimiters.
"""

from __future__ import annotations

import argparse
import os
import re
import secrets
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE_DIR = ROOT / "template"

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
}
IGNORED_FILES = {".DS_Store", "Thumbs.db"}

TOKEN_PATTERN = re.compile(r"\[\[\s*([a-z_][a-z0-9_]*)\s*\]\]")
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def git_config(key: str) -> str | None:
    """Read a git config value, returning None when git is unavailable."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", key],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None

    value = result.stdout.strip()
    return value or None


def default_repo_url(project_name: str) -> str:
    """Guess the new repository URL from the template clone's origin."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return f"https://github.com/your-user/{project_name}.git"

    url = result.stdout.strip()
    if not url:
        return f"https://github.com/your-user/{project_name}.git"

    prefix, _, repository = url.rpartition("/")
    if not prefix:
        return url

    repository_name = repository.removesuffix(".git")
    if repository_name in {"flask-template", "flask_template"}:
        return f"{prefix}/{project_name}.git"

    # The repository was created with "Use this template", so its URL is
    # already the final one.
    return url


def render(text: str, values: dict[str, str], source: Path) -> str:
    """Replace ``[[ token ]]`` placeholders, failing loudly on typos."""

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise SystemExit(f"Unknown placeholder '[[ {key} ]]' in {source}")
        return values[key]

    return TOKEN_PATTERN.sub(replace, text)


def copy_template(target: Path, values: dict[str, str]) -> None:
    """Copy and render every UTF-8 text file from the template directory."""
    for current_dir, dir_names, file_names in os.walk(TEMPLATE_DIR):
        dir_names[:] = [
            name for name in dir_names if name not in IGNORED_DIRS
        ]

        current_path = Path(current_dir)
        for file_name in file_names:
            if file_name in IGNORED_FILES:
                continue

            source = current_path / file_name
            destination = target / source.relative_to(TEMPLATE_DIR)
            destination.parent.mkdir(parents=True, exist_ok=True)

            data = source.read_bytes()
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                # Binary asset: copy verbatim.
                shutil.copy2(source, destination)
                continue

            rendered = render(text, values, source.relative_to(TEMPLATE_DIR))
            with destination.open("w", encoding="utf-8", newline="") as file:
                file.write(rendered)


def write_local_env(target: Path) -> None:
    """Create a gitignored .env with a random secret so the app runs at once."""
    example = target / ".env.example"
    if not example.is_file():
        return

    content = example.read_text(encoding="utf-8")
    secret = secrets.token_hex(32)
    content = re.sub(
        r"^FLASK_SECRET_KEY=.*$",
        f"FLASK_SECRET_KEY={secret}",
        content,
        count=1,
        flags=re.MULTILINE,
    )

    with (target / ".env").open("w", encoding="utf-8", newline="") as file:
        file.write(content)


def init_git(target: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "init", "-b", "main"],
            cwd=target,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return False

    return result.returncode == 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="create_project.py",
        description="Create a new Flask + React project from this template.",
    )
    parser.add_argument("-n", "--name", required=True, help="Project name (kebab-case)")
    parser.add_argument(
        "--path",
        type=Path,
        help="Destination directory (default: sibling folder named after the project)",
    )
    parser.add_argument(
        "-a",
        "--author",
        default=git_config("user.name") or "Your Name",
        help="Author name used in pyproject.toml",
    )
    parser.add_argument(
        "-e",
        "--email",
        default=git_config("user.email") or "you@example.com",
        help="Author email used in pyproject.toml",
    )
    parser.add_argument(
        "--vps-host",
        required=True,
        help="VPS host or IP embedded in the GitHub Actions deploy workflow",
    )
    parser.add_argument(
        "--vps-user",
        default="root",
        help="SSH user used by the deploy workflow (default: root)",
    )
    parser.add_argument(
        "--vps-path",
        help="Project directory on the VPS (default: /opt/<name>)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Public HTTP port on the VPS (default: 8000)",
    )
    parser.add_argument(
        "--repo-url",
        help="Repository URL used by the VPS setup script (default: inferred from origin)",
    )
    parser.add_argument(
        "--no-git-init",
        action="store_true",
        help="Do not run 'git init' in the generated project",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    project_name = args.name.strip()
    if not NAME_PATTERN.fullmatch(project_name) or len(project_name) > 50:
        raise SystemExit(
            "Invalid project name. Use kebab-case starting with a letter "
            "(for example: my-api). Maximum of 50 characters."
        )

    if not 1 <= args.port <= 65535:
        raise SystemExit("--port must be between 1 and 65535.")

    target = (args.path or ROOT.parent / project_name).expanduser().resolve()
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Destination is not empty: {target}")

    if not TEMPLATE_DIR.is_dir():
        raise SystemExit(f"Template directory not found: {TEMPLATE_DIR}")

    repo_url = args.repo_url or default_repo_url(project_name)
    vps_path = args.vps_path or f"/opt/{project_name}"

    values = {
        "project_name": project_name,
        "author": args.author,
        "author_email": args.email,
        "repo_url": repo_url,
        "vps_host": args.vps_host,
        "vps_user": args.vps_user,
        "vps_path": vps_path,
        "app_port": str(args.port),
        "year": str(date.today().year),
    }

    target.mkdir(parents=True, exist_ok=True)
    copy_template(target, values)
    write_local_env(target)

    git_initialized = False
    if not args.no_git_init:
        git_initialized = init_git(target)

    print(f"Created {project_name} in {target}")
    if git_initialized:
        print("Initialized an empty git repository on branch 'main'.")
    elif not args.no_git_init:
        print("Git was not found; skipped 'git init'.")

    print(
        "\nNext steps:\n"
        f"  cd {target}\n"
        "  uv sync --extra dev\n"
        "  uv run flask --app project.app run --debug\n"
        "\n"
        "In another terminal (frontend):\n"
        f"  cd {target / 'frontend'}\n"
        "  npm install\n"
        "  npm run dev\n"
        "\n"
        "Open http://localhost:5173 (dev) or http://localhost:5000 (API).\n"
        "See README.md for deployment instructions."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
