#!/usr/bin/env bash
#
# First-time setup on the VPS. Run it once:
#
#   bash deploy/setup-vps.sh
#
# Override REPO_URL or APP_DIR when needed:
#
#   REPO_URL=git@github.com:user/private-repo.git bash deploy/setup-vps.sh
set -euo pipefail

REPO_URL="${REPO_URL:-[[ repo_url ]]}"
APP_DIR="${APP_DIR:-[[ vps_path ]]}"
APP_PORT="${APP_PORT:-[[ app_port ]]}"

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  SUDO="sudo"
fi

if ! command -v git >/dev/null 2>&1; then
  if ! command -v apt-get >/dev/null 2>&1; then
    echo "git is missing and apt-get was not found; install git and run again." >&2
    exit 1
  fi
  $SUDO apt-get update
  $SUDO apt-get install -y git
fi

if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | $SUDO sh
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required (docker compose)." >&2
  exit 1
fi

mkdir -p "$(dirname "$APP_DIR")"

if [ ! -d "$APP_DIR/.git" ]; then
  git clone "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"

if [ ! -f .env ]; then
  if command -v openssl >/dev/null 2>&1; then
    secret="$(openssl rand -hex 32)"
  else
    secret="$(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')"
  fi

  cat > .env <<EOF
FLASK_ENV=production
FLASK_SECRET_KEY=$secret
GUNICORN_BIND=0.0.0.0:8000
GUNICORN_WORKERS=2
GUNICORN_WORKER_CLASS=sync
GUNICORN_TIMEOUT=60
GUNICORN_LOG_LEVEL=info
EOF
  chmod 600 .env
fi

docker compose up -d --build

echo "Deployed. Health check: http://127.0.0.1:${APP_PORT}/healthz"
