# Arquitectura del Sistema — AndesMindHack

## Resumen Ejecutivo
AndesMindHack es una aplicación web para la autogestión de vacaciones, permisos y licencias para la empresa Comfachocó. El objetivo es permitir a los empleados solicitar tiempo libre, ver su saldo disponible, automatizar aprobaciones y mostrar un calendario compartido para evitar solapamientos de personal.

## Stack Tecnológico Propuesto
- **Frontend**: React 18 + Vite + Tailwind CSS (desarrollo rápido, componentes reutilizables)
- **Backend**: Python 3.11+ + FastAPI + Uvicorn (API moderna, documentación automática)
- **Base de Datos**: PostgreSQL (Neon) (escalabilidad, ACID compliance)
- **Migraciones**: Alembic (control de versiones de esquema)
- **Autenticación**: JWT (Access tokens cortos + Refresh tokens rotativos)
- **Despliegue**: Docker + GitHub Actions (CI/CD automatizado)
- **Testing**: pytest + pytest-asyncio (backend), Jest + React Testing Library (frontend)

## Diagrama de Arquitectura de Alto Nivel

```mermaid
graph TB
    U[Usuario/Empleado] -->|HTTPS| F[Frontend React + Tailwind]
    F -->|REST API| B[Backend FastAPI]
    B -->|SQL| DB[(PostgreSQL Neon)]
    B -->|Análisis| AI[Módulo AI/ML]
    B -->|Notificaciones| EMAIL[Servicio Email]
    
    subgraph "Módulos Backend"
        AUTH[Autenticación JWT]
        REQ[Gestión Solicitudes]
        CAL[Calendario Compartido]
        ADMIN[Panel Administrativo]
    end
    
    B --> AUTH
    B --> REQ
    B --> CAL
    B --> ADMIN
```

## Diagrama de Flujo de Solicitud de Vacaciones

```mermaid
sequenceDiagram
    participant E as Empleado
    participant F as Frontend
    participant B as Backend
    participant DB as Database
    participant A as Aprobador
    
    E->>F: Solicita vacaciones (fechas, motivo)
    F->>B: POST /api/v1/requests
    B->>DB: Validar saldo disponible
    B->>DB: Verificar conflictos de calendario
    B->>DB: Crear solicitud (status: pending)
    B->>A: Notificación de aprobación
    A->>B: POST /api/v1/requests/{id}/approve
    B->>DB: Actualizar status a approved
    B->>E: Notificación de aprobación
```

## Módulos y Responsabilidades

### Frontend (`frontend/web/`)
- **Responsabilidades**: Interfaz de usuario, autenticación cliente, consumo de API REST
- **Componentes principales**:
  - `LoginForm`: Autenticación de usuarios
  - `Dashboard`: Panel principal con resumen de saldos
  - `RequestForm`: Formulario para nuevas solicitudes
  - `CalendarView`: Vista de calendario compartido
  - `AdminPanel`: Gestión administrativa (solo RRHH)

### Backend (`backend/app/`)
- **Responsabilidades**: API REST, lógica de negocio, autenticación, integración con BD
- **Módulos principales**:
  - `api/v1/`: Endpoints REST organizados por dominio
  - `core/`: Configuración, seguridad, utilidades
  - `models/`: Modelos SQLAlchemy y Pydantic
  - `db/`: Configuración de base de datos y migraciones

### AI (`ai/`)
- **Responsabilidades**: Análisis predictivo, sugerencias inteligentes
- **Funcionalidades**:
  - Detección de patrones de solicitudes
  - Sugerencias de fechas óptimas
  - Análisis de carga de trabajo por equipos

## Decisiones Arquitectónicas y Justificación

### 1. FastAPI vs Django/Flask
**Decisión**: FastAPI
**Justificación**: 
- Documentación automática (Swagger/OpenAPI)
- Validación automática con Pydantic
- Soporte nativo para async/await
- Mejor rendimiento para APIs REST

### 2. PostgreSQL vs MongoDB
**Decisión**: PostgreSQL (Neon)
**Justificación**:
- Transacciones ACID críticas para solicitudes
- Relaciones complejas entre usuarios, solicitudes y políticas
- Mejor soporte para consultas de calendario y reportes

### 3. JWT vs Sessions
**Decisión**: JWT con refresh tokens
**Justificación**:
- Stateless (escalabilidad horizontal)
- Mejor para SPA (Single Page Applications)
- Tokens de corta duración + refresh para seguridad

### 4. Tailwind vs CSS Modules/Styled Components
**Decisión**: Tailwind CSS
**Justificación**:
- Desarrollo rápido para hackathon
- Consistencia visual automática
- Menor bundle size que frameworks completos

## Paleta de Colores Comfachocó (Verde Minimalista)

```css
:root {
  /* Colores principales */
  --primary-green: #2E7D32;      /* Verde principal Comfachocó */
  --primary-light: #4CAF50;      /* Verde claro para hover */
  --primary-dark: #1B5E20;       /* Verde oscuro para texto */
  
  /* Colores de acento */
  --accent-light: #C8E6C9;       /* Verde muy claro para fondos */
  --accent-mint: #E8F5E8;        /* Verde menta para cards */
  
  /* Colores neutros */
  --background: #FAFAFA;          /* Fondo principal */
  --surface: #FFFFFF;             /* Superficie de cards */
  --text-primary: #212121;        /* Texto principal */
  --text-secondary: #757575;      /* Texto secundario */
  --border: #E0E0E0;             /* Bordes sutiles */
  
  /* Estados */
  --success: #4CAF50;            /* Aprobado */
  --warning: #FF9800;            /* Pendiente */
  --error: #F44336;              /* Rechazado */
  --info: #2196F3;               /* Información */
}
```

## Seguridad y Gestión de Secretos

### Variables de Entorno Requeridas
```bash
# Base de datos
DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=require

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (opcional para MVP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Entorno
ENVIRONMENT=development
DEBUG=false
```

### Medidas de Seguridad Implementadas
- ✅ Validación de entrada con Pydantic
- ✅ Hashing seguro de contraseñas (bcrypt)
- ✅ CORS configurado para dominios específicos
- ✅ Rate limiting en endpoints críticos
- ✅ Sanitización de uploads de archivos
- ✅ Headers de seguridad (HSTS, CSP)
- ✅ Tokens JWT con expiración corta
- ✅ Refresh tokens rotativos

## Plan de Despliegue

### Fase 1: Desarrollo Local
```bash
# Backend
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend  
cd frontend/web && npm run dev -- --host 0.0.0.0 --port 3000
```

### Fase 2: Containerización
```dockerfile
# Dockerfile para backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Fase 3: CI/CD con GitHub Actions
- Tests automatizados en PR
- Build y push de imágenes Docker
- Deploy automático a staging/producción

## Estimación de Fases y Tiempos

### Fase 0: Preparación (1 día)
- ✅ Scaffold del proyecto
- ✅ Documentación de arquitectura
- ✅ Configuración inicial de desarrollo

### Fase 1: MVP Core (3-5 días)
- Autenticación JWT completa
- CRUD de solicitudes de vacaciones
- Calendario básico compartido
- Panel administrativo mínimo
- API documentada con Swagger

### Fase 2: Funcionalidades Avanzadas (5-7 días)
- Módulo AI para sugerencias
- Notificaciones por email
- Reportes y analytics
- Tests E2E completos

### Fase 3: Producción (2-3 días)
- Hardening de seguridad
- Optimización de rendimiento
- CI/CD completo
- Monitoreo y logging

## Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Exposición de tokens en código | Media | Alto | Variables de entorno + .gitignore |
| Problemas de escalabilidad | Baja | Medio | Pool de conexiones + paginación |
| Conflictos de calendario | Alta | Alto | Validaciones estrictas + locks |
| Falta de tiempo para AI | Media | Bajo | Priorizar MVP, AI como bonus |

## Suposiciones del Proyecto

1. **Usuarios**: ~50-200 empleados iniciales
2. **Políticas**: Vacaciones anuales, permisos por horas, licencias médicas
3. **Aprobadores**: Estructura jerárquica simple (jefe directo)
4. **Integración**: No se requiere integración con sistemas legacy inicialmente
5. **Idioma**: Interfaz en español, base de datos en inglés
6. **Zona horaria**: Colombia (UTC-5)

---

*Documento generado para AndesMindHack - Hackathon Comfachocó 2024*