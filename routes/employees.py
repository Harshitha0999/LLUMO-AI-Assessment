from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from database import get_db
from models import EmployeeBase, EmployeeCreate
from auth import verify_token

router = APIRouter(prefix="/employees", tags=["employees"])
COLLECTION = "employees"

def clean_doc(doc):
    doc.pop("_id", None)
    return doc
@router.post("/", response_model=EmployeeBase)
async def create_employee(employee: EmployeeCreate, token: dict = Depends(verify_token)):
    db = get_db()
    existing = await db[COLLECTION].find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists")
    await db[COLLECTION].insert_one(employee.dict())
    return employee

@router.get("/", response_model=dict)
async def list_employees(
    department: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
):
    db = get_db()
    query = {}
    if department:
        query["department"] = department
    total = await db[COLLECTION].count_documents(query)
    cursor = db[COLLECTION].find(query).sort("joining_date", -1).skip(skip).limit(limit)
    items = [clean_doc(doc) async for doc in cursor]
    return {"total": total, "limit": limit, "skip": skip, "items": items}
