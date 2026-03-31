from fastapi import FastAPI, HTTPException, APIRouter
from operations import *
from db import test_connection
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# Enable CORS for all domains for initial deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Initializing Database...")
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

class LawyerCreate(BaseModel):
    name: str
    specialization: str

class HearingCreate(BaseModel):
    case_id: int
    hearing_date: str
    notes: str

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
        print(f"Error creating lawyer: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/hearings")
def fetch_hearings():
    try:
        return get_hearings()
    except Exception as e:
        print(f"Error fetching hearings: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/hearings")
def create_hearing(hearing: HearingCreate):
    try:
        add_hearing(hearing.case_id, hearing.hearing_date, hearing.notes)
        return {"message": "Hearing added successfully"}
    except Exception as e:
        print(f"Error adding hearing: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/dashboard-stats")
def fetch_dashboard_stats():
    try:
        cases = get_all_cases()
        lawyers = get_lawyers()
        clients = get_clients()
        hearings = get_hearings()
        
        active_cases = len([c for c in cases if c['status'] == 'Active'])
        total_cases = len(cases)
        total_lawyers = len(lawyers)
        total_clients = len(clients)
        total_hearings = len(hearings)
        
        return {
            "active_cases": active_cases,
            "total_cases": total_cases,
            "total_lawyers": total_lawyers,
            "total_clients": total_clients,
            "total_hearings": total_hearings
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

app.include_router(router)
app.include_router(router, prefix="/api")

# Start configuration for Railway/Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)