# ==========================================================
# 🧠 Ovesh AI Runtime Memory Manager
# Handles Active Tasks, Cache & Forward Sessions
# ==========================================================

class temp:
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []

    CACHE = {}
    ACTIVE_TASKS = {}from os import environ

class Config:
    API_ID = int(environ.get("API_ID", "23903140"))
    API_HASH = environ.get("API_HASH", "579f1bcf3eac1660d81ef34b09906012")
    BOT_TOKEN = environ.get("BOT_TOKEN", "8587894507:AAG4ar588fHgoIrgs_b3NGoTL6kABv2WBPM")

    BOT_SESSION = environ.get("BOT_SESSION", "ovesh_forward_bot")

    DATABASE_URI = environ.get("DATABASE_URI", "mongodb+srv://bosstgbots_db_user:DiRFdWd2U9kHoP4j@cluster0.g6p3m4j.mongodb.net/?appName=Cluster0")
    DATABASE_NAME = environ.get("DATABASE_NAME", "ovesh-forward-bot")

    BOT_OWNER = int(environ.get("BOT_OWNER", "1416433622"))


class temp:
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []

    CACHE = {}
    ACTIVE_TASKS = {}
