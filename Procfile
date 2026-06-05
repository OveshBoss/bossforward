# -------------------------------------------------------------------------
# 🤖 AI-ENGINE PROCESS MANAGEMENT MANAGER (DEPLOYMENT CONTROLLER)
# 👦 POWERED BY: Ovesh (https://t.me/OveshBoss)
# 📡 OFFICIAL UPDATES: OveshBossOfficial (https://t.me/OveshBossOfficial)
# -------------------------------------------------------------------------

# Web process to bind ports and keep web app dashboard online 24/7
web: gunicorn app:app --worker-class gthread --workers 2 --threads 4 --daemon

# High-performance main background process running the forwarder loop
worker: python3 main.py
