# -------------------------------------------------------------------------
# 🤖 AI-ENGINE WEBSERVER HUB (ALIVE KEEP-ALIVE DASHBOARD)
# 👦 POWERED & LOGGED BY: Ovesh (https://t.me/OveshBoss)
# 📡 OFFICIAL UPDATES: OveshBossOfficial (https://t.me/OveshBossOfficial)
# -------------------------------------------------------------------------

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Simple HTML responsive template designed for Ovesh Advanced Forwarder
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Forwarder Engine Status</title>
        <style>
            body {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background-color: #1e293b;
                padding: 2.5rem;
                border-radius: 16px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
                text-align: center;
                border: 1px solid #334155;
                max-width: 450px;
            }
            h1 {
                color: #38bdf8;
                font-size: 1.8rem;
                margin-bottom: 0.5rem;
            }
            p {
                color: #94a3b8;
                font-size: 1rem;
                line-height: 1.5;
            }
            .status-badge {
                background-color: #059669;
                color: #ffffff;
                padding: 0.4rem 1rem;
                border-radius: 9999px;
                font-size: 0.85rem;
                font-weight: 600;
                display: inline-block;
                margin-top: 1rem;
                letter-spacing: 0.05em;
                animation: pulse 2s infinite;
            }
            a {
                color: #38bdf8;
                text-decoration: none;
                font-weight: 500;
            }
            a:hover {
                text-decoration: underline;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🧬 AI FORWARDER ENGINE</h1>
            <p>Core system status is active. All multi-threaded event loops are running flawlessly at maximum performance.</p>
            <hr style="border-color: #334155; margin: 1.5rem 0;">
            <p>⚡ Developed & Engineered by: <a href="https://t.me/OveshBoss" target="_blank">Ovesh</a></p>
            <p>📢 Join Channel: <a href="https://t.me/OveshBossOfficial" target="_blank">@OveshBossOfficial</a></p>
            <div class="status-badge">SYSTEM ONLINE</div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    # Server configuration optimized for low latency web hooks
    app.run()
