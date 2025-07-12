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

