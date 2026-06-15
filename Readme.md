# Mywebsite Django Portfolio

A production-ready Django portfolio site—deployed seamlessly to AWS Lightsail with security best practices.

---

## 🚀 Project Overview

**mywebsite** is a personal Django-based web portfolio. It showcases modern Django development, best static/media file handling, strong environment-based security, and a professional production deployment using Gunicorn, Nginx, and HTTPS—all on AWS Lightsail.

---

## 🌟 Features

- Django 5.x project structure (apps, static, media, templates)
- Organized for both local development and cloud deployment
- Secure environment variable support using [python-decouple](https://pypi.org/project/python-decouple/)
- Gunicorn WSGI server with Nginx reverse proxy for fast, scalable production
- Full static and media file pipeline: `static/`, `staticfiles/`, `/images/`
- HTTPS by default (Encrypt on Nginx)
- Minimal, cost-effective, and easy-to-scale AWS Lightsail hosting

---

## 🛠️ Deployment Highlights

**AWS Lightsail**
- Ubuntu 22.04 LTS instance
- Codebase cloned from GitHub and deployed via virtualenv
- Gunicorn managed by systemd; Nginx reverse proxies to Gunicorn socket
- Secured with Let's Encrypt SSL/TLS via certbot
- GoDaddy domain integration [amnindersahota.com](https://www.amnindersahota.com/)

---

## Local Development (uv)

This project now uses [`uv`](https://docs.astral.sh/uv/) for dependency management and virtual environment workflows.

```bash
# Install project + dev dependencies
uv sync --locked --dev

# Run Django locally
uv run python manage.py runserver

# Common Django commands
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py collectstatic
```

---

## Code Quality Tools

```bash
# One-time setup
uv sync --locked --dev
uv run pre-commit install

# Run manually against entire repo
uv run pre-commit run --all-files

# Format/lint checks
uv run ruff format .
uv run ruff check .

# Phased typing rollout (start with app code)
uv run ty check home
```

Pre-commit auto-formats and fixes where possible on each commit. If Ruff modifies
files, stage the changes and commit again.

---

## CI (GitHub Actions)

Continuous integration is defined in `.github/workflows/ci.yml` and runs on pushes to `main`
and all pull requests.

The workflow runs:

- `uv sync --locked --all-extras --dev`
- `uv run ruff format --check .`
- `uv run ruff check .`
- `uv run ty check home`
- `uv run python manage.py check`
- `uv run python manage.py makemigrations --check --dry-run`
- `uv run python manage.py test`


---

## CD (Automated Deployment to Lightsail)

Production deployment is handled by `.github/workflows/deploy.yml` using SSH to the existing
AWS Lightsail server (Nginx + Gunicorn + systemd). Deploys trigger on push to `main` and can
also be run manually with `workflow_dispatch`.

The workflow runs `scripts/deploy_lightsail.sh` remotely to:

- deploy the target commit SHA
- run `uv sync --locked --no-dev`
- run Django checks/migrations/static collection
- restart Gunicorn only after successful update steps
- verify site availability with a smoke check for `https://amnindersahota.com`

---

## Compatibility Note

- `uv.lock` is the source of truth for dependency resolution.
- `requirements.txt` is retained for compatibility with external environments that still expect pip-style installs.
- To refresh `requirements.txt` from the lockfile:

```bash
uv export --format requirements-txt --no-dev -o requirements.txt
```
