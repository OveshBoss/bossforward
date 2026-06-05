# -------------------------------------------------------------------------
# 🤖 AI-ENGINE HYPER-CONFIG CONTROL HUB (ADVANCED ENVIRONMENT LOADER)
# 👦 POWERED & LOGGED BY: Ovesh (https://t.me/OveshBoss)
# 📡 OFFICIAL UPDATES: OveshBossOfficial (https://t.me/OveshBossOfficial)
# -------------------------------------------------------------------------

from os import environ 

class Config:
    # -------------------------------------------------------------------------
    # 📌 [1] TELEGRAM API CREDENTIALS
    # -------------------------------------------------------------------------
    
    # KYA HAI: Telegram core server se connect karne ke liye unique Numeric ID.
    # KAHAN SE MILEGA: Google pe 'my.telegram.org' kholo, login karo aur 'API development tools' me jao.
    API_ID = int(environ.get("API_ID", "23903140"))
    
    # KYA HAI: API ID ke sath milne waala ek secret secure alphanumeric code string.
    # KAHAN SE MILEGA: Yeh bhi usi 'my.telegram.org' wale same page se mil jayega.
    API_HASH = environ.get("API_HASH", "579f1bcf3eac1660d81ef34b09906012")
    
    # KYA HAI: Tumhare telegram bot ka main password/token jo bot ko control karta hai.
    # KAHAN SE MILEGA: Telegram par @BotFather ke paas jao, /newbot banao ya purane bot ka token copy karo.
    BOT_TOKEN = environ.get("BOT_TOKEN", "8587894507:AAG4ar588fHgoIrgs_b3NGoTL6kABv2WBPM") 

    # -------------------------------------------------------------------------
    # 📌 [2] SESSION & STORAGE VARIABLES
    # -------------------------------------------------------------------------
    
    # KYA HAI: Bot ke internal local session database ka naam (Pyrogram system file name).
    # KAHAN SE MILEGA: Yeh tum apne hisab se kuch bhi naam rakh sakte ho (e.g., "ovesh_session").
    BOT_SESSION = environ.get("BOT_SESSION", "ovesh_forward_bot") 
    
    # -------------------------------------------------------------------------
    # 📌 [3] MONGODB DATABASE CONFIGURATION
    # -------------------------------------------------------------------------
    
    # KYA HAI: MongoDB Cloud Database ka URL jahan users ka data aur settings save hoti hain.
    # KAHAN SE MILEGA: 'mongodb.com' (Atlas) par free account banakar, cluster setup karke connect string milti hai.
    DATABASE_URI = environ.get("DATABASE_URI", "mongodb+srv://bosstgbots_db_user:DiRFdWd2U9kHoP4j@cluster0.g6p3m4j.mongodb.net/?appName=Cluster0")
    
    # KYA HAI: MongoDB cluster ke andar tumhare bot ke specific database ka naam.
    # KAHAN SE MILEGA: Yeh tum jo chaho naam rakh sakte ho, database automatic is naam se create ho jayega.
    DATABASE_NAME = environ.get("DATABASE_NAME", "ovesh-forward-bot")

    # -------------------------------------------------------------------------
    # 📌 [4] ADMIN CONTROL & SECURITY
    # -------------------------------------------------------------------------
    
    # KYA HAI: Main bot owner/creator ki unique Telegram numeric user ID.
    # KAHAN SE MILEGA: Telegram par @MissRose_bot ya @Userinfobot par /id likh kar apni ID copy karo.
    # NOTE: Sirf is ID wale user ke paas bot ko poori tarah control (Ban/Unban/Stats) karne ka access hoga.
    BOT_OWNER = int(environ.get("BOT_OWNER", "1416433622"))


# -------------------------------------------------------------------------
# 🧬 AI DYNAMIC MEMORY SYSTEM (DO NOT EDIT THIS SECTION)
# 👦 OPTIMIZED BY OVESH (t.me/Ovesh_Boss)
# -------------------------------------------------------------------------
class temp(object): 
    # KYA HAI: Ek time par ek user ek hi forward command chalaye, usko crash hone se rokne ka lock matrix.
    lock = {}
    
    # KYA HAI: Agar user beech me /cancel dabaye toh chalte huye process ko instantly kill karne ki dictionary.
    CANCEL = {}
    
    # KYA HAI: Live tracking counter—is waqt poore bot me kitne logs forward ho rahe hain.
    forwardings = 0
    
    # KYA HAI: Bot se block kiye huye users ki real-time memory list taaki DB par baar-baar load na pade.
    BANNED_USERS = []
    
    # KYA HAI: Un active chats ki list jinka forwarding process abhi background me live chal raha hai.
    IS_FRWD_CHAT = []

# --- CONFIGURATION LOG ENDS HERE ---
# Engine optimized for maximum threading and 0ms latency.
