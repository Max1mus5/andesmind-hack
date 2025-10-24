import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-comfachoco-primary text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold">AndesMindHack</h1>
              <span className="ml-3 text-comfachoco-accent text-sm">Comfachocó</span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-white hover:text-comfachoco-accent transition-colors">Dashboard</a>
              <a href="#" className="text-white hover:text-comfachoco-accent transition-colors">Solicitudes</a>
              <a href="#" className="text-white hover:text-comfachoco-accent transition-colors">Calendario</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Sistema de Autogestión del Empleado
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Gestiona tus vacaciones, permisos y licencias de forma fácil y eficiente
          </p>
          
          {/* Demo Counter */}
          <div className="bg-white rounded-lg shadow-md p-8 max-w-md mx-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Proyecto React Inicializado ✅
            </h3>
            <button 
              onClick={() => setCount((count) => count + 1)}
              className="bg-comfachoco-primary hover:bg-comfachoco-dark text-white font-bold py-2 px-4 rounded transition-colors"
            >
              Contador: {count}
            </button>
            <p className="text-sm text-gray-500 mt-4">
              Frontend creado desde cero con Vite + React + TypeScript + Tailwind CSS
            </p>
          </div>

          {/* Features Grid */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="w-12 h-12 bg-comfachoco-accent rounded-lg mx-auto mb-4 flex items-center justify-center">
                <span className="text-comfachoco-primary font-bold text-xl">📅</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Gestión de Vacaciones</h3>
              <p className="text-gray-600">Solicita y gestiona tus vacaciones de forma intuitiva</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="w-12 h-12 bg-comfachoco-accent rounded-lg mx-auto mb-4 flex items-center justify-center">
                <span className="text-comfachoco-primary font-bold text-xl">📋</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Permisos y Licencias</h3>
              <p className="text-gray-600">Tramita permisos especiales y licencias médicas</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="w-12 h-12 bg-comfachoco-accent rounded-lg mx-auto mb-4 flex items-center justify-center">
                <span className="text-comfachoco-primary font-bold text-xl">👥</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Calendario Compartido</h3>
              <p className="text-gray-600">Visualiza la disponibilidad de tu equipo</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2024 AndesMindHack - Comfachocó. Todos los derechos reservados.</p>
        </div>
      </footer>
    </div>
  )
}

export default App
