# from fastapi import FastAPI
# from database import connect_to_mongo, close_mongo_connection, get_db
# from routes import employees
# from pymongo.errors import OperationFailure

# app = FastAPI()

# employee_validator = {
#     "$jsonSchema": {
#         "bsonType": "object",
#         "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
#         "properties": {
#             "employee_id": {"bsonType": "string"},
#             "name": {"bsonType": "string"},
#             "department": {"bsonType": "string"},
#             "salary": {"bsonType": ["int", "double", "decimal"]},
#             "joining_date": {
#                 "bsonType": "string",
#                 "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
#             },
#             "skills": {
#                 "bsonType": "array",
#                 "items": {"bsonType": "string"}
#             }
#         }
#     }
# }

# @app.on_event("startup")
# async def startup_event():
    
#     await connect_to_mongo()
#     db = get_db()

#     existing = await db.list_collection_names()
#     if "employees" not in existing:
#         await db.create_collection("employees", validator=employee_validator)
#         print("Created employees collection with JSON schema validator")
#     else:
#         try:
#             await db.command({
#                 "collMod": "employees",
#                 "validator": employee_validator,
#                 "validationLevel": "moderate"
#             })
#             print("Applied validator to employees collection (collMod)")
#         except OperationFailure as e:
#             print("Warning: Could not apply validator. Maybe already exists:", e)

# @app.on_event("shutdown")
# def shutdown_event():
#     close_mongo_connection()

# app.include_router(employees.router)





from fastapi import FastAPI
from database import connect_to_mongo, close_mongo_connection, get_db
from routes import employees, auth
from pymongo.errors import OperationFailure

app = FastAPI()

employee_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
        "properties": {
            "employee_id": {"bsonType": "string"},
            "name": {"bsonType": "string"},
            "department": {"bsonType": "string"},
            "salary": {"bsonType": ["int", "double", "decimal"]},
            "joining_date": {"bsonType": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
            "skills": {"bsonType": "array", "items": {"bsonType": "string"}}
        }
    }
}

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    db = get_db()
    if "employees" not in await db.list_collection_names():
        await db.create_collection("employees", validator=employee_validator)
        print("Created employees collection with validator")
    else:
        try:
            await db.command({"collMod": "employees", "validator": employee_validator, "validationLevel": "moderate"})
            print("Applied validator to employees collection")
        except OperationFailure as e:
            print("Warning: Could not apply validator:", e)

@app.on_event("shutdown")
def shutdown_event():
    close_mongo_connection()

# Include routes
app.include_router(auth.router)
app.include_router(employees.router)
