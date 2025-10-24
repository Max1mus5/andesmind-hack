# Requisitos Backend — AndesMindHack

## Especificación de API REST

### Base URL
```
Desarrollo: http://localhost:8000/api/v1
Producción: https://andesmind-hack.railway.app/api/v1
```

## Endpoints de Autenticación

### POST /api/v1/auth/register
Registro de nuevos usuarios (empleados).

**Request Body:**
```json
{
  "email": "empleado@comfachoco.com",
  "password": "SecurePass123!",
  "name": "Juan Pérez",
  "employee_id": "EMP001",
  "department": "Tecnología",
  "position": "Desarrollador Senior"
}
```

**Response 201:**
```json
{
  "id": 1,
  "email": "empleado@comfachoco.com",
  "name": "Juan Pérez",
  "employee_id": "EMP001",
  "department": "Tecnología",
  "position": "Desarrollador Senior",
  "role": "employee",
  "is_active": true,
  "created_at": "2024-10-24T15:30:00Z"
}
```

**Validaciones:**
- Email único y formato válido
- Contraseña mínimo 8 caracteres, al menos 1 mayúscula, 1 número
- employee_id único en la organización

### POST /api/v1/auth/login
Autenticación de usuarios existentes.

**Request Body:**
```json
{
  "email": "empleado@comfachoco.com",
  "password": "SecurePass123!"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": 1,
    "email": "empleado@comfachoco.com",
    "name": "Juan Pérez",
    "role": "employee"
  }
}
```

### POST /api/v1/auth/refresh
Renovación de access token usando refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### POST /api/v1/auth/logout
Invalidación de tokens (blacklist).

**Headers:** `Authorization: Bearer <access_token>`

**Response 200:**
```json
{
  "message": "Logout exitoso"
}
```

## Endpoints de Usuario

### GET /api/v1/users/me
Obtener perfil del usuario autenticado.

**Headers:** `Authorization: Bearer <access_token>`

**Response 200:**
```json
{
  "id": 1,
  "email": "empleado@comfachoco.com",
  "name": "Juan Pérez",
  "employee_id": "EMP001",
  "department": "Tecnología",
  "position": "Desarrollador Senior",
  "role": "employee",
  "vacation_balance": {
    "annual_days": 15,
    "used_days": 5,
    "remaining_days": 10,
    "accrual_rate": 1.25
  },
  "manager": {
    "id": 5,
    "name": "María García",
    "email": "maria.garcia@comfachoco.com"
  }
}
```

### PUT /api/v1/users/me
Actualizar perfil del usuario.

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "name": "Juan Carlos Pérez",
  "phone": "+57 300 123 4567",
  "emergency_contact": {
    "name": "Ana Pérez",
    "phone": "+57 300 987 6543",
    "relationship": "Esposa"
  }
}
```

## Endpoints de Solicitudes

### POST /api/v1/requests
Crear nueva solicitud de tiempo libre.

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "policy_id": 1,
  "start_date": "2024-12-15",
  "end_date": "2024-12-20",
  "reason": "Vacaciones familiares",
  "notes": "Viaje programado con anticipación",
  "half_day": false,
  "attachments": [
    {
      "filename": "reserva_hotel.pdf",
      "content_type": "application/pdf",
      "size": 245760
    }
  ]
}
```

**Response 201:**
```json
{
  "id": 15,
  "user_id": 1,
  "policy": {
    "id": 1,
    "name": "Vacaciones Anuales",
    "type": "vacation",
    "requires_approval": true
  },
  "start_date": "2024-12-15",
  "end_date": "2024-12-20",
  "business_days": 4,
  "calendar_days": 6,
  "reason": "Vacaciones familiares",
  "notes": "Viaje programado con anticipación",
  "status": "pending",
  "created_at": "2024-10-24T15:30:00Z",
  "approver": {
    "id": 5,
    "name": "María García"
  }
}
```

**Validaciones:**
- start_date <= end_date
- No solapamiento con solicitudes aprobadas del mismo usuario
- Saldo suficiente para el tipo de solicitud
- Fechas no pueden ser en el pasado (excepto admin)
- Máximo 30 días consecutivos para vacaciones

### GET /api/v1/requests
Listar solicitudes del usuario autenticado.

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `status`: pending, approved, rejected, cancelled
- `policy_type`: vacation, sick_leave, personal_leave
- `date_from`: YYYY-MM-DD
- `date_to`: YYYY-MM-DD
- `page`: número de página (default: 1)
- `limit`: elementos por página (default: 20, max: 100)

**Response 200:**
```json
{
  "items": [
    {
      "id": 15,
      "policy": {
        "id": 1,
        "name": "Vacaciones Anuales",
        "type": "vacation"
      },
      "start_date": "2024-12-15",
      "end_date": "2024-12-20",
      "business_days": 4,
      "status": "pending",
      "created_at": "2024-10-24T15:30:00Z",
      "approver": {
        "name": "María García"
      }
    }
  ],
  "total": 1,
  "page": 1,
  "pages": 1,
  "has_next": false,
  "has_prev": false
}
```

### GET /api/v1/requests/{id}
Obtener detalles de una solicitud específica.

**Headers:** `Authorization: Bearer <access_token>`

**Response 200:**
```json
{
  "id": 15,
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "employee_id": "EMP001"
  },
  "policy": {
    "id": 1,
    "name": "Vacaciones Anuales",
    "type": "vacation",
    "deducts_from_balance": true
  },
  "start_date": "2024-12-15",
  "end_date": "2024-12-20",
  "business_days": 4,
  "calendar_days": 6,
  "reason": "Vacaciones familiares",
  "notes": "Viaje programado con anticipación",
  "status": "pending",
  "created_at": "2024-10-24T15:30:00Z",
  "updated_at": "2024-10-24T15:30:00Z",
  "approver": {
    "id": 5,
    "name": "María García",
    "email": "maria.garcia@comfachoco.com"
  },
  "approval_history": [
    {
      "action": "submitted",
      "timestamp": "2024-10-24T15:30:00Z",
      "user": "Juan Pérez",
      "notes": null
    }
  ],
  "attachments": [
    {
      "id": 1,
      "filename": "reserva_hotel.pdf",
      "content_type": "application/pdf",
      "size": 245760,
      "uploaded_at": "2024-10-24T15:30:00Z"
    }
  ]
}
```

### PUT /api/v1/requests/{id}
Actualizar solicitud (solo si status = pending).

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "start_date": "2024-12-16",
  "end_date": "2024-12-21",
  "reason": "Vacaciones familiares - fechas actualizadas",
  "notes": "Cambio de fechas por disponibilidad de vuelos"
}
```

### DELETE /api/v1/requests/{id}
Cancelar solicitud (solo si status = pending).

**Headers:** `Authorization: Bearer <access_token>`

**Response 200:**
```json
{
  "message": "Solicitud cancelada exitosamente",
  "id": 15,
  "status": "cancelled"
}
```

## Endpoints de Aprobación (Managers/RRHH)

### POST /api/v1/requests/{id}/approve
Aprobar solicitud.

**Headers:** `Authorization: Bearer <access_token>`
**Permisos:** role = manager o hr_admin

**Request Body:**
```json
{
  "notes": "Aprobado. Que disfrute sus vacaciones."
}
```

**Response 200:**
```json
{
  "message": "Solicitud aprobada exitosamente",
  "id": 15,
  "status": "approved",
  "approved_at": "2024-10-25T10:15:00Z",
  "approved_by": {
    "id": 5,
    "name": "María García"
  }
}
```

### POST /api/v1/requests/{id}/reject
Rechazar solicitud.

**Headers:** `Authorization: Bearer <access_token>`
**Permisos:** role = manager o hr_admin

**Request Body:**
```json
{
  "reason": "Conflicto con proyecto crítico",
  "notes": "Por favor reagenda para después del 15 de enero"
}
```

**Response 200:**
```json
{
  "message": "Solicitud rechazada",
  "id": 15,
  "status": "rejected",
  "rejected_at": "2024-10-25T10:15:00Z",
  "rejected_by": {
    "id": 5,
    "name": "María García"
  }
}
```

### GET /api/v1/requests/pending
Listar solicitudes pendientes de aprobación.

**Headers:** `Authorization: Bearer <access_token>`
**Permisos:** role = manager o hr_admin

**Query Parameters:**
- `department`: filtrar por departamento
- `employee_id`: filtrar por empleado específico
- `policy_type`: vacation, sick_leave, personal_leave
- `page`, `limit`: paginación

## Endpoints de Calendario

### GET /api/v1/calendar
Obtener calendario de ausencias del equipo.

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `start_date`: YYYY-MM-DD (default: inicio del mes actual)
- `end_date`: YYYY-MM-DD (default: fin del mes actual)
- `department`: filtrar por departamento
- `include_pending`: incluir solicitudes pendientes (default: false)

**Response 200:**
```json
{
  "period": {
    "start_date": "2024-12-01",
    "end_date": "2024-12-31"
  },
  "absences": [
    {
      "user": {
        "id": 1,
        "name": "Juan Pérez",
        "department": "Tecnología"
      },
      "request_id": 15,
      "start_date": "2024-12-15",
      "end_date": "2024-12-20",
      "policy_type": "vacation",
      "status": "approved"
    },
    {
      "user": {
        "id": 3,
        "name": "Ana López",
        "department": "Tecnología"
      },
      "request_id": 18,
      "start_date": "2024-12-23",
      "end_date": "2024-12-27",
      "policy_type": "vacation",
      "status": "pending"
    }
  ],
  "summary": {
    "total_absences": 2,
    "by_department": {
      "Tecnología": 2,
      "Ventas": 0
    },
    "by_status": {
      "approved": 1,
      "pending": 1
    }
  }
}
```

## Endpoints Administrativos

### GET /api/v1/admin/users
Listar todos los usuarios (solo RRHH).

**Headers:** `Authorization: Bearer <access_token>`
**Permisos:** role = hr_admin

**Query Parameters:**
- `department`: filtrar por departamento
- `role`: employee, manager, hr_admin
- `is_active`: true, false
- `search`: buscar por nombre o email
- `page`, `limit`: paginación

### POST /api/v1/admin/users/{id}/deactivate
Desactivar usuario.

**Headers:** `Authorization: Bearer <access_token>`
**Permisos:** role = hr_admin

### GET /api/v1/admin/reports/summary
Reporte resumen de solicitudes.

**Headers:** `Authorization: Bearer <access_token>`
**Permisos:** role = manager o hr_admin

**Query Parameters:**
- `period`: month, quarter, year
- `year`: YYYY
- `month`: MM (si period = month)
- `department`: filtrar por departamento

**Response 200:**
```json
{
  "period": {
    "type": "month",
    "year": 2024,
    "month": 10
  },
  "summary": {
    "total_requests": 45,
    "approved": 38,
    "rejected": 4,
    "pending": 3,
    "total_days_taken": 156,
    "average_days_per_employee": 3.9
  },
  "by_department": [
    {
      "department": "Tecnología",
      "employees": 12,
      "requests": 18,
      "days_taken": 67,
      "average_per_employee": 5.6
    }
  ],
  "by_policy_type": {
    "vacation": 28,
    "sick_leave": 12,
    "personal_leave": 5
  }
}
```

### GET /api/v1/admin/policies
Gestionar políticas de tiempo libre.

**Headers:** `Authorization: Bearer <access_token>`
**Permisos:** role = hr_admin

**Response 200:**
```json
{
  "policies": [
    {
      "id": 1,
      "name": "Vacaciones Anuales",
      "type": "vacation",
      "days_allocated": 15,
      "requires_approval": true,
      "advance_notice_days": 7,
      "max_consecutive_days": 30,
      "accrual_rate": 1.25,
      "is_active": true
    },
    {
      "id": 2,
      "name": "Licencia por Enfermedad",
      "type": "sick_leave",
      "days_allocated": 5,
      "requires_approval": false,
      "advance_notice_days": 0,
      "max_consecutive_days": 3,
      "accrual_rate": 0.42,
      "is_active": true
    }
  ]
}
```

## Endpoints de Salud y Monitoreo

### GET /healthz
Health check básico.

**Response 200:**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-24T15:30:00Z",
  "version": "1.0.0",
  "environment": "development"
}
```

### GET /api/v1/health/detailed
Health check detallado (requiere autenticación).

**Headers:** `Authorization: Bearer <access_token>`

**Response 200:**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-24T15:30:00Z",
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
      "last_sent": "2024-10-24T14:45:00Z"
    }
  },
  "metrics": {
    "active_users": 45,
    "pending_requests": 8,
    "requests_today": 12
  }
}
```

## Modelos de Base de Datos

### Tabla: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(100),
    position VARCHAR(100),
    role VARCHAR(20) DEFAULT 'employee',
    manager_id INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT true,
    phone VARCHAR(20),
    emergency_contact JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: policies
```sql
CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    days_allocated INTEGER DEFAULT 0,
    requires_approval BOOLEAN DEFAULT true,
    advance_notice_days INTEGER DEFAULT 0,
    max_consecutive_days INTEGER,
    accrual_rate DECIMAL(4,2) DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: requests
```sql
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    policy_id INTEGER NOT NULL REFERENCES policies(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    business_days INTEGER NOT NULL,
    calendar_days INTEGER NOT NULL,
    reason TEXT,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    half_day BOOLEAN DEFAULT false,
    approver_id INTEGER REFERENCES users(id),
    approved_at TIMESTAMP,
    rejected_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: user_balances
```sql
CREATE TABLE user_balances (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    policy_id INTEGER NOT NULL REFERENCES policies(id),
    allocated_days DECIMAL(5,2) DEFAULT 0,
    used_days DECIMAL(5,2) DEFAULT 0,
    remaining_days DECIMAL(5,2) DEFAULT 0,
    year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, policy_id, year)
);
```

## Contratos Pydantic

### Modelos de Request
```python
from pydantic import BaseModel, EmailStr, validator
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR_ADMIN = "hr_admin"

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    employee_id: str
    department: Optional[str] = None
    position: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

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
```

## Autenticación y Seguridad

### Configuración JWT
```python
# Configuración recomendada
JWT_SECRET_KEY = "your-super-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Headers de seguridad
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'"
}
```

### Rate Limiting
```python
# Límites recomendados
RATE_LIMITS = {
    "/api/v1/auth/login": "5/minute",
    "/api/v1/auth/register": "3/minute", 
    "/api/v1/requests": "10/minute",
    "default": "100/minute"
}
```

## Migraciones con Alembic

### Configuración inicial
```bash
# Inicializar Alembic
alembic init alembic

# Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head
```

### Estructura de migraciones
```
backend/
├── alembic/
│   ├── versions/
│   │   ├── 001_initial_migration.py
│   │   ├── 002_add_user_balances.py
│   │   └── 003_add_audit_logs.py
│   ├── env.py
│   └── script.py.mako
└── alembic.ini
```

## Testing

### Estructura de tests
```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/api/v1/auth/register", json={
        "email": "test@comfachoco.com",
        "password": "TestPass123!",
        "name": "Test User",
        "employee_id": "TEST001"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@comfachoco.com"

def test_login_user():
    # Primero registrar
    client.post("/api/v1/auth/register", json={
        "email": "test@comfachoco.com",
        "password": "TestPass123!",
        "name": "Test User",
        "employee_id": "TEST001"
    })
    
    # Luego login
    response = client.post("/api/v1/auth/login", json={
        "email": "test@comfachoco.com",
        "password": "TestPass123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Comandos de testing
```bash
# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_auth.py -v
```

---

*Documento técnico para AndesMindHack Backend - Comfachocó 2024*