#!/usr/bin/env bash

# AndesMindHack - Script de Configuración Automática
# Hackathon Comfachocó 2024

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de configuración
REPO_NAME="andesmind-hack"
GIT_USER_NAME="jeronimo"
GIT_USER_EMAIL="jeronimor.dev@gmail.com"
GITHUB_TOKEN="YOUR_GITHUB_TOKEN_HERE"

# Funciones de utilidad
print_header() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "  AndesMindHack - Setup Script"
    echo "  Comfachocó Hackathon 2024"
    echo "=================================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

check_requirements() {
    print_step "Verificando prerrequisitos..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js no está instalado. Por favor instala Node.js 18+ desde https://nodejs.org/"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js versión 18+ requerida. Versión actual: $(node --version)"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado. Por favor instala Python 3.11+ desde https://python.org/"
        exit 1
    fi
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git no está instalado. Por favor instala Git desde https://git-scm.com/"
        exit 1
    fi
    
    print_success "Todos los prerrequisitos están instalados"
}

setup_git() {
    print_step "Configurando Git..."
    
    # Configurar credenciales de Git
    git config user.name "$GIT_USER_NAME"
    git config user.email "$GIT_USER_EMAIL"
    
    print_success "Git configurado con usuario: $GIT_USER_NAME"
}

setup_backend() {
    print_step "Configurando Backend (FastAPI)..."
    
    cd backend
    
    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        print_step "Creando entorno virtual de Python..."
        python3 -m venv venv
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Actualizar pip
    pip install --upgrade pip
    
    # Instalar dependencias
    print_step "Instalando dependencias de Python..."
    pip install -r requirements.txt
    
    # Crear archivo .env si no existe
    if [ ! -f ".env" ]; then
        print_step "Creando archivo .env para backend..."
        cp .env.example .env
        print_warning "Por favor edita backend/.env con tus credenciales reales"
    fi
    
    cd ..
    print_success "Backend configurado correctamente"
}

setup_frontend() {
    print_step "Configurando Frontend (React + Vite)..."
    
    cd frontend/web
    
    # Instalar dependencias
    print_step "Instalando dependencias de Node.js..."
    npm install
    
    # Crear archivo .env si no existe
    if [ ! -f ".env" ]; then
        print_step "Creando archivo .env para frontend..."
        cp .env.example .env
    fi
    
    cd ../..
    print_success "Frontend configurado correctamente"
}

create_docker_compose() {
    print_step "Creando archivo docker-compose.yml..."
    
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - ENVIRONMENT=development
    volumes:
      - ./backend:/app
    depends_on:
      - db

  frontend:
    build: ./frontend/web
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=andesmind
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
EOF

    print_success "docker-compose.yml creado"
}

create_gitignore() {
    print_step "Creando .gitignore..."
    
    cat > .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
venv/
env/
ENV/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
.DS_Store
*.tsbuildinfo

# Build outputs
/backend/dist/
/frontend/web/dist/
/frontend/web/build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov
.nyc_output

# Database
*.db
*.sqlite

# Docker
.dockerignore

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Temporary files
*.tmp
*.temp
EOF

    print_success ".gitignore creado"
}

setup_github_repo() {
    print_step "Configurando repositorio de GitHub..."
    
    # Inicializar repositorio si no existe
    if [ ! -d ".git" ]; then
        git init
        print_success "Repositorio Git inicializado"
    fi
    
    # Agregar archivos
    git add .
    git commit -m "feat: scaffold inicial del proyecto AndesMindHack

- Estructura modular: backend/, frontend/, ai/, docs/
- Backend: FastAPI + PostgreSQL + JWT auth
- Frontend: React + Vite + Tailwind CSS
- Documentación técnica completa
- Scripts de configuración automatizada
- Docker y docker-compose setup
- Paleta de colores Comfachocó (verde minimalista)"
    
    # Configurar rama principal
    git branch -M main
    
    # Crear repositorio en GitHub usando la API
    print_step "Creando repositorio en GitHub..."
    
    REPO_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "{\"name\":\"$REPO_NAME\",\"description\":\"Sistema de Autogestión de Vacaciones para Comfachocó - Hackathon 2024\",\"private\":false}" \
        https://api.github.com/user/repos)
    
    if echo "$REPO_RESPONSE" | grep -q '"clone_url"'; then
        CLONE_URL=$(echo "$REPO_RESPONSE" | grep '"clone_url"' | cut -d'"' -f4)
        
        # Configurar remote con token
        git remote add origin "https://$GITHUB_TOKEN@github.com/$GIT_USER_NAME/$REPO_NAME.git"
        
        # Push inicial
        print_step "Subiendo código a GitHub..."
        git push -u origin main
        
        print_success "Repositorio creado y código subido exitosamente!"
        echo -e "${BLUE}URL del repositorio: https://github.com/$GIT_USER_NAME/$REPO_NAME${NC}"
    else
        print_warning "No se pudo crear el repositorio automáticamente."
        print_warning "Por favor crea el repositorio manualmente en GitHub y ejecuta:"
        echo "git remote add origin https://github.com/$GIT_USER_NAME/$REPO_NAME.git"
        echo "git push -u origin main"
    fi
}

start_development_servers() {
    print_step "¿Deseas iniciar los servidores de desarrollo? (y/n)"
    read -r START_SERVERS
    
    if [[ $START_SERVERS =~ ^[Yy]$ ]]; then
        print_step "Iniciando servidores de desarrollo..."
        
        # Crear script para iniciar backend
        cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF
        chmod +x start-backend.sh
        
        # Crear script para iniciar frontend
        cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend/web
npm run dev
EOF
        chmod +x start-frontend.sh
        
        print_success "Scripts de inicio creados:"
        echo "  - Backend: ./start-backend.sh"
        echo "  - Frontend: ./start-frontend.sh"
        echo ""
        echo "O usa Docker Compose:"
        echo "  docker-compose up --build"
    fi
}

print_final_instructions() {
    echo ""
    echo -e "${GREEN}=================================================="
    echo "  🎉 ¡Configuración Completada!"
    echo "==================================================${NC}"
    echo ""
    echo -e "${BLUE}Próximos pasos:${NC}"
    echo ""
    echo "1. 📝 Editar archivos de configuración:"
    echo "   - backend/.env (credenciales de base de datos)"
    echo "   - frontend/web/.env (si es necesario)"
    echo ""
    echo "2. 🚀 Iniciar servidores de desarrollo:"
    echo "   - Backend:  ./start-backend.sh"
    echo "   - Frontend: ./start-frontend.sh"
    echo "   - O usar:   docker-compose up --build"
    echo ""
    echo "3. 🌐 URLs de desarrollo:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend:  http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/docs"
    echo ""
    echo "4. 📚 Documentación técnica:"
    echo "   - docs/architecture.md"
    echo "   - docs/backend-requirements.md"
    echo "   - docs/frontend-requirements.md"
    echo ""
    echo -e "${YELLOW}⚠️  Recordatorios importantes:${NC}"
    echo "   - Actualiza las credenciales en los archivos .env"
    echo "   - Revisa la documentación antes de desarrollar"
    echo "   - Usa la paleta de colores de Comfachocó"
    echo ""
    echo -e "${GREEN}¡Feliz desarrollo! 🌿${NC}"
}

# Función principal
main() {
    print_header
    
    check_requirements
    setup_git
    create_gitignore
    create_docker_compose
    setup_backend
    setup_frontend
    setup_github_repo
    start_development_servers
    print_final_instructions
}

# Ejecutar función principal
main "$@"