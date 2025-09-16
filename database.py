

import motor.motor_asyncio

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "assessment_db"
COLLECTION = "employees"

client = None
db = None

async def connect_to_mongo():
    global client, db
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    await db[COLLECTION].create_index("employee_id", unique=True)
    print("Connected to MongoDB with unique employee_id index.")

def get_db():
    if db is None:
        raise Exception("Database not initialized. Call connect_to_mongo first.")
    return db

def close_mongo_connection():
    if client:
        client.close()
        print("MongoDB connection closed.")
