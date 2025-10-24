"""
AndesMindHack - Sistema de Autogestión de Vacaciones para Comfachocó
FastAPI Backend Application
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime, timedelta, date
from typing import Optional, List, Dict, Any
import os
from enum import Enum

# Initialize FastAPI app
app = FastAPI(
    title="AndesMindHack API",
    description="Sistema de Autogestión de Vacaciones para Comfachocó",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    # Add production frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Enums
class UserRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR_ADMIN = "hr_admin"

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class PolicyType(str, Enum):
    VACATION = "vacation"
    SICK_LEAVE = "sick_leave"
    PERSONAL_LEAVE = "personal_leave"

# Pydantic Models
class UserBase(BaseModel):
    email: EmailStr
    name: str
    employee_id: str
    department: Optional[str] = None
    position: Optional[str] = None

class UserRegister(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    vacation_balance: Optional[Dict[str, Any]] = None
    manager: Optional[Dict[str, Any]] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PolicyResponse(BaseModel):
    id: int
    name: str
    type: PolicyType
    days_allocated: int
    requires_approval: bool
    advance_notice_days: int
    max_consecutive_days: Optional[int]
    is_active: bool

class RequestCreate(BaseModel):
    policy_id: int
    start_date: date
    end_date: date
    reason: str
    notes: Optional[str] = None
    half_day: bool = False
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be >= start_date')
        return v

class RequestResponse(BaseModel):
    id: int
    user_id: int
    policy: PolicyResponse
    start_date: date
    end_date: date
    business_days: int
    calendar_days: int
    reason: str
    notes: Optional[str]
    status: RequestStatus
    half_day: bool
    created_at: datetime
    updated_at: datetime
    approver: Optional[Dict[str, Any]] = None
    user: Optional[Dict[str, Any]] = None

class ApprovalAction(BaseModel):
    notes: Optional[str] = None

class RejectionAction(BaseModel):
    reason: str
    notes: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str

# In-memory storage for demo (replace with actual database)
FAKE_DB = {
    "users": [
        {
            "id": 1,
            "email": "admin@comfachoco.com",
            "name": "Administrador Sistema",
            "employee_id": "ADM001",
            "department": "RRHH",
            "position": "Administrador",
            "role": "hr_admin",
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "hashed_password": "$2b$12$dummy_hash_for_demo"
        },
        {
            "id": 2,
            "email": "manager@comfachoco.com",
            "name": "María García",
            "employee_id": "MGR001",
            "department": "Tecnología",
            "position": "Gerente de TI",
            "role": "manager",
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "hashed_password": "$2b$12$dummy_hash_for_demo"
        },
        {
            "id": 3,
            "email": "empleado@comfachoco.com",
            "name": "Juan Pérez",
            "employee_id": "EMP001",
            "department": "Tecnología",
            "position": "Desarrollador Senior",
            "role": "employee",
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "hashed_password": "$2b$12$dummy_hash_for_demo"
        }
    ],
    "policies": [
        {
            "id": 1,
            "name": "Vacaciones Anuales",
            "type": "vacation",
            "days_allocated": 15,
            "requires_approval": True,
            "advance_notice_days": 7,
            "max_consecutive_days": 30,
            "is_active": True
        },
        {
            "id": 2,
            "name": "Licencia por Enfermedad",
            "type": "sick_leave",
            "days_allocated": 5,
            "requires_approval": False,
            "advance_notice_days": 0,
            "max_consecutive_days": 3,
            "is_active": True
        },
        {
            "id": 3,
            "name": "Permiso Personal",
            "type": "personal_leave",
            "days_allocated": 3,
            "requires_approval": True,
            "advance_notice_days": 1,
            "max_consecutive_days": 2,
            "is_active": True
        }
    ],
    "requests": [
        {
            "id": 1,
            "user_id": 3,
            "policy_id": 1,
            "start_date": "2024-12-15",
            "end_date": "2024-12-20",
            "business_days": 4,
            "calendar_days": 6,
            "reason": "Vacaciones familiares",
            "notes": "Viaje programado con anticipación",
            "status": "pending",
            "half_day": False,
            "approver_id": 2,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
    ]
}

# Utility functions
def get_user_by_email(email: str) -> Optional[Dict]:
    return next((user for user in FAKE_DB["users"] if user["email"] == email), None)

def get_user_by_id(user_id: int) -> Optional[Dict]:
    return next((user for user in FAKE_DB["users"] if user["id"] == user_id), None)

def get_policy_by_id(policy_id: int) -> Optional[Dict]:
    return next((policy for policy in FAKE_DB["policies"] if policy["id"] == policy_id), None)

def calculate_business_days(start_date: date, end_date: date) -> int:
    """Calculate business days between two dates (excluding weekends)"""
    current_date = start_date
    business_days = 0
    
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days

def get_current_user_mock() -> Dict:
    """Mock function to get current user (replace with JWT validation)"""
    return FAKE_DB["users"][2]  # Return employee user for demo

# API Endpoints

@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.get("/api/v1/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": {
                "status": "healthy",
                "response_time_ms": 12,
                "connection_pool": {
                    "active": 2,
                    "idle": 8,
                    "max": 20
                }
            },
            "email": {
                "status": "healthy",
                "last_sent": datetime.utcnow().isoformat()
            }
        },
        "metrics": {
            "active_users": len([u for u in FAKE_DB["users"] if u["is_active"]]),
            "pending_requests": len([r for r in FAKE_DB["requests"] if r["status"] == "pending"]),
            "requests_today": len(FAKE_DB["requests"])
        }
    }

# Authentication Endpoints
@app.post("/api/v1/auth/register", status_code=201, response_model=UserResponse)
async def register(user_data: UserRegister):
    """Register a new user"""
    # Check if user already exists
    if get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Check if employee_id already exists
    if any(u["employee_id"] == user_data.employee_id for u in FAKE_DB["users"]):
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )
    
    # Create new user
    new_user = {
        "id": len(FAKE_DB["users"]) + 1,
        "email": user_data.email,
        "name": user_data.name,
        "employee_id": user_data.employee_id,
        "department": user_data.department,
        "position": user_data.position,
        "role": "employee",
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "hashed_password": f"$2b$12$hashed_{user_data.password}"  # Mock hash
    }
    
    FAKE_DB["users"].append(new_user)
    
    # Return user without password
    return UserResponse(
        id=new_user["id"],
        email=new_user["email"],
        name=new_user["name"],
        employee_id=new_user["employee_id"],
        department=new_user["department"],
        position=new_user["position"],
        role=UserRole(new_user["role"]),
        is_active=new_user["is_active"],
        created_at=datetime.fromisoformat(new_user["created_at"])
    )

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Authenticate user and return tokens"""
    user = get_user_by_email(credentials.email)
    
    if not user or not user["is_active"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials or inactive user"
        )
    
    # Mock password verification (replace with actual password hashing)
    # In production: verify_password(credentials.password, user["hashed_password"])
    
    # Mock JWT tokens (replace with actual JWT generation)
    access_token = f"mock_access_token_for_{user['id']}"
    refresh_token = f"mock_refresh_token_for_{user['id']}"
    
    user_response = UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        employee_id=user["employee_id"],
        department=user["department"],
        position=user["position"],
        role=UserRole(user["role"]),
        is_active=user["is_active"],
        created_at=datetime.fromisoformat(user["created_at"]),
        vacation_balance={
            "annual_days": 15,
            "used_days": 5,
            "remaining_days": 10,
            "accrual_rate": 1.25
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response
    )

@app.post("/api/v1/auth/refresh", response_model=Dict[str, Any])
async def refresh_token(token_data: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    # Mock token refresh (replace with actual JWT validation and generation)
    if not token_data.refresh_token.startswith("mock_refresh_token"):
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    
    # Extract user ID from mock token
    user_id = token_data.refresh_token.split("_")[-1]
    new_access_token = f"mock_access_token_for_{user_id}"
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 900
    }

@app.post("/api/v1/auth/logout")
async def logout():
    """Logout user (invalidate tokens)"""
    # In production: add tokens to blacklist
    return {"message": "Logout exitoso"}

# User Endpoints
@app.get("/api/v1/users/me", response_model=UserResponse)
async def get_current_user():
    """Get current user profile"""
    user = get_current_user_mock()
    
    # Find manager
    manager = None
    if user["role"] == "employee":
        manager = next((u for u in FAKE_DB["users"] if u["role"] == "manager" and u["department"] == user["department"]), None)
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        employee_id=user["employee_id"],
        department=user["department"],
        position=user["position"],
        role=UserRole(user["role"]),
        is_active=user["is_active"],
        created_at=datetime.fromisoformat(user["created_at"]),
        vacation_balance={
            "annual_days": 15,
            "used_days": 5,
            "remaining_days": 10,
            "accrual_rate": 1.25
        },
        manager={
            "id": manager["id"],
            "name": manager["name"],
            "email": manager["email"]
        } if manager else None
    )

# Policies Endpoints
@app.get("/api/v1/policies", response_model=List[PolicyResponse])
async def get_policies():
    """Get all active policies"""
    active_policies = [p for p in FAKE_DB["policies"] if p["is_active"]]
    
    return [
        PolicyResponse(
            id=policy["id"],
            name=policy["name"],
            type=PolicyType(policy["type"]),
            days_allocated=policy["days_allocated"],
            requires_approval=policy["requires_approval"],
            advance_notice_days=policy["advance_notice_days"],
            max_consecutive_days=policy.get("max_consecutive_days"),
            is_active=policy["is_active"]
        )
        for policy in active_policies
    ]

# Requests Endpoints
@app.post("/api/v1/requests", status_code=201, response_model=RequestResponse)
async def create_request(request_data: RequestCreate):
    """Create a new time-off request"""
    current_user = get_current_user_mock()
    policy = get_policy_by_id(request_data.policy_id)
    
    if not policy:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )
    
    # Validate dates are not in the past
    if request_data.start_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be in the past"
        )
    
    # Calculate business days
    business_days = calculate_business_days(request_data.start_date, request_data.end_date)
    calendar_days = (request_data.end_date - request_data.start_date).days + 1
    
    # Find approver (manager of the same department)
    approver = next((u for u in FAKE_DB["users"] if u["role"] == "manager" and u["department"] == current_user["department"]), None)
    
    # Create new request
    new_request = {
        "id": len(FAKE_DB["requests"]) + 1,
        "user_id": current_user["id"],
        "policy_id": request_data.policy_id,
        "start_date": request_data.start_date.isoformat(),
        "end_date": request_data.end_date.isoformat(),
        "business_days": business_days,
        "calendar_days": calendar_days,
        "reason": request_data.reason,
        "notes": request_data.notes,
        "status": "pending",
        "half_day": request_data.half_day,
        "approver_id": approver["id"] if approver else None,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    FAKE_DB["requests"].append(new_request)
    
    return RequestResponse(
        id=new_request["id"],
        user_id=new_request["user_id"],
        policy=PolicyResponse(
            id=policy["id"],
            name=policy["name"],
            type=PolicyType(policy["type"]),
            days_allocated=policy["days_allocated"],
            requires_approval=policy["requires_approval"],
            advance_notice_days=policy["advance_notice_days"],
            max_consecutive_days=policy.get("max_consecutive_days"),
            is_active=policy["is_active"]
        ),
        start_date=date.fromisoformat(new_request["start_date"]),
        end_date=date.fromisoformat(new_request["end_date"]),
        business_days=new_request["business_days"],
        calendar_days=new_request["calendar_days"],
        reason=new_request["reason"],
        notes=new_request["notes"],
        status=RequestStatus(new_request["status"]),
        half_day=new_request["half_day"],
        created_at=datetime.fromisoformat(new_request["created_at"]),
        updated_at=datetime.fromisoformat(new_request["updated_at"]),
        approver={
            "id": approver["id"],
            "name": approver["name"]
        } if approver else None
    )

@app.get("/api/v1/requests", response_model=Dict[str, Any])
async def get_user_requests(
    status: Optional[str] = None,
    policy_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = 1,
    limit: int = 20
):
    """Get user's requests with optional filters"""
    current_user = get_current_user_mock()
    
    # Filter requests for current user
    user_requests = [r for r in FAKE_DB["requests"] if r["user_id"] == current_user["id"]]
    
    # Apply filters
    if status:
        user_requests = [r for r in user_requests if r["status"] == status]
    
    # Convert to response format
    requests_response = []
    for request in user_requests:
        policy = get_policy_by_id(request["policy_id"])
        approver = get_user_by_id(request.get("approver_id")) if request.get("approver_id") else None
        
        requests_response.append({
            "id": request["id"],
            "policy": {
                "id": policy["id"],
                "name": policy["name"],
                "type": policy["type"]
            },
            "start_date": request["start_date"],
            "end_date": request["end_date"],
            "business_days": request["business_days"],
            "status": request["status"],
            "created_at": request["created_at"],
            "approver": {
                "name": approver["name"]
            } if approver else None
        })
    
    # Pagination
    total = len(requests_response)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_requests = requests_response[start_idx:end_idx]
    
    return {
        "items": paginated_requests,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "has_next": end_idx < total,
        "has_prev": page > 1
    }

@app.get("/api/v1/requests/{request_id}", response_model=RequestResponse)
async def get_request_details(request_id: int):
    """Get detailed information about a specific request"""
    request = next((r for r in FAKE_DB["requests"] if r["id"] == request_id), None)
    
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )
    
    current_user = get_current_user_mock()
    
    # Check if user can access this request
    if request["user_id"] != current_user["id"] and current_user["role"] not in ["manager", "hr_admin"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
    
    policy = get_policy_by_id(request["policy_id"])
    user = get_user_by_id(request["user_id"])
    approver = get_user_by_id(request.get("approver_id")) if request.get("approver_id") else None
    
    return RequestResponse(
        id=request["id"],
        user_id=request["user_id"],
        policy=PolicyResponse(
            id=policy["id"],
            name=policy["name"],
            type=PolicyType(policy["type"]),
            days_allocated=policy["days_allocated"],
            requires_approval=policy["requires_approval"],
            advance_notice_days=policy["advance_notice_days"],
            max_consecutive_days=policy.get("max_consecutive_days"),
            is_active=policy["is_active"]
        ),
        start_date=date.fromisoformat(request["start_date"]),
        end_date=date.fromisoformat(request["end_date"]),
        business_days=request["business_days"],
        calendar_days=request["calendar_days"],
        reason=request["reason"],
        notes=request["notes"],
        status=RequestStatus(request["status"]),
        half_day=request["half_day"],
        created_at=datetime.fromisoformat(request["created_at"]),
        updated_at=datetime.fromisoformat(request["updated_at"]),
        user={
            "id": user["id"],
            "name": user["name"],
            "employee_id": user["employee_id"]
        },
        approver={
            "id": approver["id"],
            "name": approver["name"],
            "email": approver["email"]
        } if approver else None
    )

# Admin/Manager Endpoints
@app.get("/api/v1/requests/pending", response_model=List[Dict[str, Any]])
async def get_pending_requests():
    """Get all pending requests for approval (managers/HR only)"""
    current_user = get_current_user_mock()
    
    if current_user["role"] not in ["manager", "hr_admin"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Manager or HR role required."
        )
    
    pending_requests = [r for r in FAKE_DB["requests"] if r["status"] == "pending"]
    
    # If manager, only show requests from their department
    if current_user["role"] == "manager":
        department_users = [u["id"] for u in FAKE_DB["users"] if u["department"] == current_user["department"]]
        pending_requests = [r for r in pending_requests if r["user_id"] in department_users]
    
    # Format response
    response = []
    for request in pending_requests:
        user = get_user_by_id(request["user_id"])
        policy = get_policy_by_id(request["policy_id"])
        
        response.append({
            "id": request["id"],
            "user": {
                "id": user["id"],
                "name": user["name"],
                "employee_id": user["employee_id"],
                "department": user["department"]
            },
            "policy": {
                "name": policy["name"],
                "type": policy["type"]
            },
            "start_date": request["start_date"],
            "end_date": request["end_date"],
            "business_days": request["business_days"],
            "reason": request["reason"],
            "created_at": request["created_at"]
        })
    
    return response

@app.post("/api/v1/requests/{request_id}/approve")
async def approve_request(request_id: int, approval: ApprovalAction):
    """Approve a pending request"""
    current_user = get_current_user_mock()
    
    if current_user["role"] not in ["manager", "hr_admin"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Manager or HR role required."
        )
    
    request = next((r for r in FAKE_DB["requests"] if r["id"] == request_id), None)
    
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )
    
    if request["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail="Request is not pending approval"
        )
    
    # Update request status
    request["status"] = "approved"
    request["approved_at"] = datetime.utcnow().isoformat()
    request["approved_by"] = current_user["id"]
    request["approval_notes"] = approval.notes
    request["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "message": "Solicitud aprobada exitosamente",
        "id": request_id,
        "status": "approved",
        "approved_at": request["approved_at"],
        "approved_by": {
            "id": current_user["id"],
            "name": current_user["name"]
        }
    }

@app.post("/api/v1/requests/{request_id}/reject")
async def reject_request(request_id: int, rejection: RejectionAction):
    """Reject a pending request"""
    current_user = get_current_user_mock()
    
    if current_user["role"] not in ["manager", "hr_admin"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Manager or HR role required."
        )
    
    request = next((r for r in FAKE_DB["requests"] if r["id"] == request_id), None)
    
    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )
    
    if request["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail="Request is not pending approval"
        )
    
    # Update request status
    request["status"] = "rejected"
    request["rejected_at"] = datetime.utcnow().isoformat()
    request["rejected_by"] = current_user["id"]
    request["rejection_reason"] = rejection.reason
    request["rejection_notes"] = rejection.notes
    request["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "message": "Solicitud rechazada",
        "id": request_id,
        "status": "rejected",
        "rejected_at": request["rejected_at"],
        "rejected_by": {
            "id": current_user["id"],
            "name": current_user["name"]
        }
    }

# Calendar Endpoint
@app.get("/api/v1/calendar")
async def get_team_calendar(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    department: Optional[str] = None,
    include_pending: bool = False
):
    """Get team calendar with approved absences"""
    current_user = get_current_user_mock()
    
    # Default to current month if no dates provided
    if not start_date:
        today = date.today()
        start_date = today.replace(day=1).isoformat()
    
    if not end_date:
        today = date.today()
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        end_date = end_date.isoformat()
    
    # Filter requests by date range and status
    calendar_requests = []
    for request in FAKE_DB["requests"]:
        if request["status"] == "approved" or (include_pending and request["status"] == "pending"):
            req_start = date.fromisoformat(request["start_date"])
            req_end = date.fromisoformat(request["end_date"])
            filter_start = date.fromisoformat(start_date)
            filter_end = date.fromisoformat(end_date)
            
            # Check if request overlaps with filter period
            if req_start <= filter_end and req_end >= filter_start:
                calendar_requests.append(request)
    
    # Format response
    absences = []
    for request in calendar_requests:
        user = get_user_by_id(request["user_id"])
        policy = get_policy_by_id(request["policy_id"])
        
        # Filter by department if specified
        if department and user["department"] != department:
            continue
        
        absences.append({
            "user": {
                "id": user["id"],
                "name": user["name"],
                "department": user["department"]
            },
            "request_id": request["id"],
            "start_date": request["start_date"],
            "end_date": request["end_date"],
            "policy_type": policy["type"],
            "status": request["status"]
        })
    
    # Summary statistics
    departments = {}
    statuses = {}
    
    for absence in absences:
        dept = absence["user"]["department"]
        status = absence["status"]
        
        departments[dept] = departments.get(dept, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
    
    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "absences": absences,
        "summary": {
            "total_absences": len(absences),
            "by_department": departments,
            "by_status": statuses
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )