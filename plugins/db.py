# -------------------------------------------------------------------------
# 🗄️ ADVANCED MULTI-NODE MONGO CLUSTER STORAGE ENGINE
# 👦 DESIGNED & ARCHITECTURED BY: Ovesh (https://t.me/Ovesh_Boss)
# 📡 CENTRAL UPDATE STREAM: OveshBossOfficial (https://t.me/OveshBossOfficial)
# -------------------------------------------------------------------------

import asyncio
import logging
import motor.motor_asyncio

logger = logging.getLogger("Ovesh-DBEngine")

class MongoDB:
    def __init__(self, uri: str, db_name: str, collection: str):
        self.uri = uri
        self.db_name = db_name
        self.collection = collection 
        self.client = None
        self.db = None
        self.files = None

    async def connect(self) -> bool:
        """Establishes an optimized asynchronous pool connection to MongoDB."""
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                self.uri,
                serverSelectionTimeoutMS=5000,
                retryWrites=True
            )
            self.db = self.client[self.db_name]
            self.files = self.db[self.collection]
            return True
        except Exception as e:
            logger.error(f"Failed to connect to cluster node [{self.db_name}]: {e}")
            return False

    async def close(self):
        """Gracefully disconnects and releases active database sockets."""
        if self.client:
            self.client.close()

    async def add_file(self, file_id: str):
        """Indexes a unique file entity into the secure user collection document."""
        file = {"file_id": file_id}
        return await self.files.insert_one(file)
        
    async def is_file_exit(self, file_id: str) -> bool:
        """Validates if the specified document footprint already exists."""
        f = await self.files.find_one({"file_id": file_id})
        return bool(f)
        
    async def get_all_files(self):
        """Retrieves cursor streams for all documents assigned to the collection."""
        return self.files.find({})
        
    async def drop_all(self):
        """Wipes the active user workspace node storage structure completely."""
        if self.files is not None:
            return await self.files.drop()

async def connect_user_db(user_id: int, uri: str, chat: str) -> tuple:
    """
    Dynamically initializes and switches connection layers for targeted 
    user data channels isolated in independent forward spaces.
    """
    chat_identifier = f"{user_id}{chat}"
    dbname = f"{user_id}-Forward-Bot"
    
    db = MongoDB(uri, dbname, chat_identifier)
    
    # Executing localized async storage handshaking
    is_connected = await db.connect()
    if not is_connected:
        return False, db
        
    return True, db
