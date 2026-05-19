#!/usr/bin/env bash
# Remote deploy script piped from GitHub Actions to the Lightsail server.
# Do not run manually unless you understand each step and its ordering.
#
# Usage (via GitHub Actions):
#   ssh user@host 'bash -s' <app_dir> <commit_sha> <gunicorn_service> < scripts/deploy_lightsail.sh
#
# Positional arguments:
#   $1  APP_DIR         Absolute path to the app repo on the server
#   $2  COMMIT_SHA      Git SHA to deploy (the exact commit CI passed on)
#   $3  SERVICE_NAME    systemd unit name for Gunicorn (e.g. gunicorn)

set -euo pipefail

APP_DIR="${1:?APP_DIR argument is required}"
COMMIT_SHA="${2:?COMMIT_SHA argument is required}"
SERVICE_NAME="${3:?SERVICE_NAME argument is required}"

log() { echo "[deploy $(date -u +%H:%M:%SZ)] $*"; }

# Non-interactive SSH sessions often omit user-local bin directories.
export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
    log "ERROR: uv is not available in PATH: $PATH"
    log "Install uv or expose it via ~/.local/bin before deploying."
    exit 127
fi

log "Starting deploy of ${COMMIT_SHA}"
log "App dir: ${APP_DIR} | Service: ${SERVICE_NAME}"

cd "${APP_DIR}"

log "Fetching latest code from origin"
git fetch origin

log "Checking out ${COMMIT_SHA}"
git -c advice.detachedHead=false checkout "${COMMIT_SHA}"

log "Syncing production dependencies (no dev)"
# --locked: assert uv.lock is up to date with pyproject.toml at this SHA
# --no-dev: omit the [dependency-groups].dev group (ruff, ty) in production
uv sync --locked --no-dev

log "Running Django system checks"
uv run python manage.py check

log "Applying database migrations"
uv run python manage.py migrate --noinput

log "Collecting static files"
# WhiteNoise CompressedManifestStaticFilesStorage regenerates the manifest on each run.
# No --clear flag: avoids a brief window where all static files are absent.
uv run python manage.py collectstatic --noinput

log "Restarting Gunicorn (${SERVICE_NAME})"
sudo systemctl restart "${SERVICE_NAME}"

log "Verifying service health"
# Poll up to ~10s for systemd to confirm the unit is active after restart.
for i in 1 2 3 4 5; do
    if sudo systemctl is-active --quiet "${SERVICE_NAME}"; then
        log "Service ${SERVICE_NAME} is active"
        break
    fi
    if [ "${i}" -eq 5 ]; then
        log "ERROR: ${SERVICE_NAME} failed to become active after restart"
        sudo systemctl status "${SERVICE_NAME}" --no-pager --lines=30 || true
        exit 1
    fi
    sleep 2
done

log "Deploy of ${COMMIT_SHA} completed successfully"
