# AndesMindHack 🌿

Sistema de Autogestión de Vacaciones para **Comfachocó** - Desarrollado para el Hackathon 2024

## 🎯 Descripción del Proyecto

AndesMindHack es una aplicación web moderna que permite a los empleados de Comfachocó gestionar sus solicitudes de tiempo libre de manera eficiente y transparente. El sistema incluye funcionalidades para solicitar vacaciones, permisos y licencias, con un flujo de aprobación automatizado y un calendario compartido para evitar conflictos.

## ✨ Características Principales

- 🔐 **Autenticación segura** con JWT y refresh tokens
- 📝 **Gestión de solicitudes** de vacaciones, permisos y licencias
- 📅 **Calendario compartido** del equipo
- 👥 **Panel administrativo** para managers y RRHH
- 📊 **Reportes y analytics** de uso
- 🤖 **Sugerencias inteligentes** con IA (módulo opcional)
- 📱 **Diseño responsive** con paleta verde minimalista de Comfachocó
- 🚀 **API REST completa** con documentación automática

## 🏗️ Arquitectura Técnica

### Backend
- **Framework**: FastAPI + Python 3.11+
- **Base de Datos**: PostgreSQL (Neon)
- **Autenticación**: JWT con refresh tokens
- **Documentación**: Swagger/OpenAPI automática
- **Migraciones**: Alembic

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Estilos**: Tailwind CSS
- **Estado**: React Context + React Query
- **Routing**: React Router DOM v6

### Infraestructura
- **Containerización**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Despliegue**: Railway/Heroku (recomendado)

## 🚀 Inicio Rápido

### Prerrequisitos
- Node.js 18+ y npm 9+
- Python 3.11+
- Docker y Docker Compose (opcional)
- Git

### Instalación Automática

```bash
# Clonar el repositorio
git clone https://github.com/jeronimo/andesmind-hack.git
cd andesmind-hack

# Ejecutar script de configuración
chmod +x setup.sh
./setup.sh
```

### Instalación Manual

#### 1. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar migraciones (cuando estén configuradas)
# alembic upgrade head

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Configurar Frontend

```bash
cd frontend/web

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env si es necesario

# Iniciar servidor de desarrollo
npm run dev
```

### Usando Docker Compose

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Solo en modo desarrollo
docker-compose -f docker-compose.dev.yml up
```

## 📖 Documentación

### Documentación Técnica
- [Arquitectura del Sistema](docs/architecture.md)
- [Requisitos del Backend](docs/backend-requirements.md)
- [Requisitos del Frontend](docs/frontend-requirements.md)

### API Documentation
Una vez que el backend esté ejecutándose, puedes acceder a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### URLs de Desarrollo
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 🎨 Paleta de Colores Comfachocó

```css
:root {
  --primary-green: #2E7D32;    /* Verde principal */
  --primary-light: #4CAF50;    /* Verde claro */
  --primary-dark: #1B5E20;     /* Verde oscuro */
  --accent-light: #C8E6C9;     /* Verde muy claro */
  --accent-mint: #E8F5E8;      /* Verde menta */
  --success: #4CAF50;          /* Éxito */
  --warning: #FF9800;          /* Advertencia */
  --error: #F44336;            /* Error */
  --info: #2196F3;             /* Información */
}
```

## 🔧 Scripts Disponibles

### Backend
```bash
# Desarrollo
uvicorn app.main:app --reload

# Tests
pytest
pytest --cov=app --cov-report=html

# Linting
black app/
isort app/
flake8 app/

# Migraciones
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Frontend
```bash
# Desarrollo
npm run dev

# Build de producción
npm run build

# Preview del build
npm run preview

# Tests
npm run test
npm run test:coverage

# Linting
npm run lint
npm run lint:fix

# Type checking
npm run type-check
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
pytest --cov=app --cov-report=html tests/
```

### Frontend Testing
```bash
cd frontend/web
npm run test
npm run test:coverage
npm run e2e  # Cypress E2E tests
```

## 📦 Estructura del Proyecto

```
andesmind-hack/
├── backend/                 # API Backend (FastAPI)
│   ├── app/
│   │   ├── api/v1/         # Endpoints REST
│   │   ├── core/           # Configuración y seguridad
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── db/             # Base de datos y migraciones
│   │   └── main.py         # Aplicación principal
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/web/           # Frontend React
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── pages/          # Páginas de la aplicación
│   │   ├── hooks/          # Custom hooks
│   │   ├── utils/          # Utilidades
│   │   ├── types/          # Tipos TypeScript
│   │   └── api/            # Cliente API
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── ai/                     # Módulo de IA (opcional)
│   ├── notebooks/          # Jupyter notebooks
│   └── services/           # Servicios de ML
├── docs/                   # Documentación técnica
│   ├── architecture.md
│   ├── backend-requirements.md
│   └── frontend-requirements.md
├── docker-compose.yml      # Orquestación de contenedores
├── setup.sh               # Script de configuración
└── README.md              # Este archivo
```

## 🔐 Seguridad

### Medidas Implementadas
- ✅ Autenticación JWT con tokens de corta duración
- ✅ Refresh tokens rotativos
- ✅ Validación de entrada con Pydantic
- ✅ Hashing seguro de contraseñas (bcrypt)
- ✅ CORS configurado
- ✅ Rate limiting en endpoints críticos
- ✅ Headers de seguridad (HSTS, CSP, etc.)
- ✅ Sanitización de uploads

### Variables de Entorno Críticas
```bash
# Backend
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256

# Frontend
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

**⚠️ IMPORTANTE**: Nunca subas archivos `.env` al repositorio. Usa `.env.example` como plantilla.

## 🚀 Despliegue

### Desarrollo Local
```bash
# Backend
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend/web && npm run dev
```

### Producción con Docker
```bash
# Build y deploy
docker-compose -f docker-compose.prod.yml up --build -d

# Ver logs
docker-compose logs -f
```

### Despliegue en Railway
1. Conecta tu repositorio de GitHub
2. Configura las variables de entorno
3. Railway detectará automáticamente los Dockerfiles
4. Deploy automático en cada push a main

## 📊 Roadmap de Desarrollo

### Fase 1: MVP Core (Semana 1)
- [x] Scaffold del proyecto
- [x] Documentación técnica
- [x] Autenticación básica
- [ ] CRUD de solicitudes
- [ ] Calendario básico
- [ ] Panel administrativo mínimo

### Fase 2: Funcionalidades Avanzadas (Semana 2)
- [ ] Módulo de IA para sugerencias
- [ ] Notificaciones por email
- [ ] Reportes y analytics
- [ ] Tests E2E completos
- [ ] Optimización de rendimiento

### Fase 3: Producción (Semana 3)
- [ ] Hardening de seguridad
- [ ] CI/CD completo
- [ ] Monitoreo y logging
- [ ] Documentación de usuario
- [ ] Capacitación del equipo

## 🤝 Contribución

### Flujo de Desarrollo
1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Add: nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Convenciones de Código
- **Backend**: Black + isort + flake8
- **Frontend**: ESLint + Prettier
- **Commits**: Conventional Commits
- **Branches**: feature/, bugfix/, hotfix/

## 📄 Licencia

Este proyecto está desarrollado para el Hackathon Comfachocó 2024. Todos los derechos reservados.

## 👥 Equipo de Desarrollo

- **Arquitecto de Software**: Responsable del diseño y planificación técnica
- **Backend Developer**: Implementación de API y lógica de negocio
- **Frontend Developer**: Interfaz de usuario y experiencia
- **DevOps Engineer**: Infraestructura y despliegue
