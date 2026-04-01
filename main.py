from fastapi import FastAPI, HTTPException, APIRouter
from operations import *
from db import test_connection
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional

app = FastAPI()

# Read FRONTEND_URL from environment for production CORS
FRONTEND_URL = os.environ.get("FRONTEND_URL")
if FRONTEND_URL:
    allowed_origins = [FRONTEND_URL]
else:
    # Fallback to wildcard for local development when FRONTEND_URL not provided
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Initializing Backend...")
    print(f"FRONTEND_URL={FRONTEND_URL}")
    ok, ver = test_connection()
    if ok:
        print(f"Database Connected. MySQL Version: {ver}")
    else:
        print("Database Connection Failed!")

class CaseCreate(BaseModel):
    case_number: str
    case_type: str
    client_id: int
    lawyer_id: int
    filing_date: str
    description: str
    
class CaseResponse(BaseModel):
    case_id: int
    case_number: str
    case_type: str
    status: str
    client_id: int
    lawyer_id: int
    filing_date: str
    description: str

class CaseStatusUpdate(BaseModel):
    status: str

class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str


class LawyerCreate(BaseModel):
    name: str
    specialization: str


class HearingCreate(BaseModel):
    case_id: int
    hearing_date: str
    notes: Optional[str] = None

# Endpoints
router = APIRouter()

@router.get("/")
def home():
    return {"message": "Legal Case Management Backend is running"}

@router.get("/cases")
def fetch_cases():
    try:
        return get_all_cases()
    except Exception as e:
        print(f"Error fetching cases: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/cases/{case_id}")
def fetch_case_details(case_id: int):
    try:
        case = get_case_by_id(case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        return case
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching case details: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/cases")
def create_case(case: CaseCreate):
    try:
        add_case(
            case.case_number,
            case.case_type,
            case.client_id,
            case.lawyer_id,
            case.filing_date,
            case.description
        )
        return {"message": "Case created successfully"}
    except Exception as e:
        print(f"Error creating case: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/cases/{case_id}")
def update_case(case_id: int, data: CaseStatusUpdate):
    try:
        update_case_status(case_id, data.status)
        return {"message": "Case updated successfully"}
    except Exception as e:
        print(f"Error updating case: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/clients")
def fetch_clients():
    try:
        return get_clients()
    except Exception as e:
        print(f"Error fetching clients: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/clients")
def create_client(client: ClientCreate):
    try:
        add_client(
            client.first_name,
            client.last_name,
            client.email,
            client.phone,
            client.address
        )
        return {"message": "Client created successfully"}
    except Exception as e:
        print(f"Error adding client: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/lawyers")
def fetch_lawyers():
    try:
        return get_lawyers()
    except Exception as e:
        print(f"Error fetching lawyers: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/lawyers")
def create_lawyer(lawyer: LawyerCreate):
    try:
        add_lawyer(lawyer.name, lawyer.specialization)
        return {"message": "Lawyer added successfully"}
    except Exception as e:
        print(f"Error adding lawyer: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/hearings")
def fetch_hearings(case_id: Optional[int] = None):
    try:
        return get_hearings(case_id)
    except Exception as e:
        print(f"Error fetching hearings: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/hearings")
def create_hearing(hearing: HearingCreate):
    try:
        case = get_case_by_id(hearing.case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        add_hearing(hearing.case_id, hearing.hearing_date, hearing.notes)
        return {"message": "Hearing added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error adding hearing: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

app.include_router(router)
app.include_router(router, prefix="/api")

# Start configuration for Railway/Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)