# =========================================================================
#  🧬 ADVANCED AUTOMATION ENGINE - DOCKER RUNTIME ENVIRONMENT
#  👦 LEAD DEVELOPER & MODDER: Ovesh (https://t.me/OveshBoss)
#  📡 OFFICIAL CHANNEL: OveshBossOfficial (https://t.me/OveshBossOfficial)
# =========================================================================

# Debian Bullseye is solid and perfect for VPS deployment
FROM python:3.10-slim-bullseye

# System updates and required build essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Upgrade pip first to avoid wheels build errors
RUN pip3 install -U pip

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copy the rest of the application files
COPY . .

# Setup execution permissions for our custom production runner
RUN chmod +x run.sh

# Start the Ovesh Automation Stack via the runner script
CMD ["./run.sh"]
