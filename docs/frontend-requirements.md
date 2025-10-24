# Requisitos Frontend — AndesMindHack

## Especificación de Aplicación React

### Tecnologías Base
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite (desarrollo rápido, HMR)
- **Styling**: Tailwind CSS (utilidades, consistencia)
- **Routing**: React Router DOM v6
- **State Management**: React Context + useReducer
- **HTTP Client**: Axios (interceptors, mejor manejo de errores)
- **Forms**: React Hook Form + Zod (validación)
- **Date Handling**: date-fns (ligero, modular)
- **Icons**: Lucide React (consistentes, SVG)

## Estructura de Rutas

### Rutas Públicas
```
/login          - Página de autenticación
/register       - Registro de nuevos empleados (opcional)
/forgot-password - Recuperación de contraseña
```

### Rutas Privadas (Requieren Autenticación)
```
/dashboard      - Panel principal del empleado
/requests       - Lista de mis solicitudes
/requests/new   - Formulario nueva solicitud
/requests/:id   - Detalles de solicitud específica
/calendar       - Calendario compartido del equipo
/profile        - Perfil y configuración personal
```

### Rutas Administrativas (Managers/RRHH)
```
/admin/dashboard    - Panel administrativo
/admin/requests     - Solicitudes pendientes de aprobación
/admin/users        - Gestión de usuarios
/admin/reports      - Reportes y analytics
/admin/policies     - Configuración de políticas
/admin/calendar     - Vista de calendario administrativo
```

## Componentes Principales

### 1. Layout Components

#### `AppLayout.tsx`
Layout principal con navegación y sidebar.

```tsx
interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Header />
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
```

#### `Sidebar.tsx`
Navegación lateral con menú contextual según rol.

```tsx
const navigationItems = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Mis Solicitudes', href: '/requests', icon: DocumentTextIcon },
  { name: 'Nueva Solicitud', href: '/requests/new', icon: PlusIcon },
  { name: 'Calendario', href: '/calendar', icon: CalendarIcon },
  { name: 'Mi Perfil', href: '/profile', icon: UserIcon },
];

const adminNavigationItems = [
  { name: 'Panel Admin', href: '/admin/dashboard', icon: ChartBarIcon },
  { name: 'Aprobaciones', href: '/admin/requests', icon: ClipboardCheckIcon },
  { name: 'Usuarios', href: '/admin/users', icon: UsersIcon },
  { name: 'Reportes', href: '/admin/reports', icon: DocumentChartBarIcon },
];
```

### 2. Authentication Components

#### `LoginForm.tsx`
Formulario de autenticación con validación.

```tsx
interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

const LoginForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormData>();
  const { login } = useAuth();

  const onSubmit = async (data: LoginFormData) => {
    try {
      await login(data.email, data.password, data.rememberMe);
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <img className="mx-auto h-12 w-auto" src="/logo-comfachoco.svg" alt="Comfachocó" />
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Inicia sesión en tu cuenta
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          {/* Form fields */}
        </form>
      </div>
    </div>
  );
};
```

#### `ProtectedRoute.tsx`
Componente para proteger rutas que requieren autenticación.

```tsx
interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'employee' | 'manager' | 'hr_admin';
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole }) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole && user?.role !== requiredRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};
```

### 3. Dashboard Components

#### `Dashboard.tsx`
Panel principal con resumen de información del empleado.

```tsx
const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { data: balance } = useQuery('vacation-balance', fetchVacationBalance);
  const { data: recentRequests } = useQuery('recent-requests', fetchRecentRequests);

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-2xl font-bold leading-6 text-gray-900">
          Bienvenido, {user?.name}
        </h1>
        <p className="mt-2 max-w-4xl text-sm text-gray-500">
          Gestiona tus solicitudes de tiempo libre y consulta tu saldo disponible.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <VacationBalanceCard balance={balance} />
        <PendingRequestsCard requests={recentRequests} />
        <QuickActionsCard />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentRequestsTable requests={recentRequests} />
        <UpcomingAbsencesCard />
      </div>
    </div>
  );
};
```

#### `VacationBalanceCard.tsx`
Tarjeta mostrando saldo de vacaciones disponibles.

```tsx
interface VacationBalance {
  annual_days: number;
  used_days: number;
  remaining_days: number;
  accrual_rate: number;
}

const VacationBalanceCard: React.FC<{ balance: VacationBalance }> = ({ balance }) => {
  const percentage = (balance.used_days / balance.annual_days) * 100;

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <CalendarIcon className="h-6 w-6 text-primary-green" />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">
                Días de Vacaciones
              </dt>
              <dd className="text-lg font-medium text-gray-900">
                {balance.remaining_days} de {balance.annual_days} disponibles
              </dd>
            </dl>
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <span>Usados: {balance.used_days}</span>
            <span>{percentage.toFixed(0)}%</span>
          </div>
          <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-primary-green h-2 rounded-full transition-all duration-300"
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
```

### 4. Request Management Components

#### `RequestForm.tsx`
Formulario para crear nuevas solicitudes.

```tsx
interface RequestFormData {
  policy_id: number;
  start_date: string;
  end_date: string;
  reason: string;
  notes?: string;
  half_day: boolean;
}

const RequestForm: React.FC = () => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm<RequestFormData>();
  const { data: policies } = useQuery('policies', fetchPolicies);
  const createRequestMutation = useMutation(createRequest);

  const startDate = watch('start_date');
  const endDate = watch('end_date');
  const businessDays = calculateBusinessDays(startDate, endDate);

  const onSubmit = async (data: RequestFormData) => {
    try {
      await createRequestMutation.mutateAsync(data);
      // Redirect to requests list
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Nueva Solicitud de Tiempo Libre
          </h3>
          <div className="mt-2 max-w-xl text-sm text-gray-500">
            <p>Completa el formulario para solicitar días de vacaciones, permisos o licencias.</p>
          </div>
          
          <form onSubmit={handleSubmit(onSubmit)} className="mt-5 space-y-6">
            <PolicySelector policies={policies} register={register} errors={errors} />
            <DateRangePicker register={register} errors={errors} />
            <BusinessDaysPreview days={businessDays} />
            <ReasonTextArea register={register} errors={errors} />
            <NotesTextArea register={register} />
            <HalfDayToggle register={register} />
            <AttachmentUpload />
            
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={createRequestMutation.isLoading}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-green hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-green disabled:opacity-50"
              >
                {createRequestMutation.isLoading ? 'Enviando...' : 'Enviar Solicitud'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
```

#### `RequestsList.tsx`
Lista de solicitudes del usuario con filtros.

```tsx
const RequestsList: React.FC = () => {
  const [filters, setFilters] = useState({
    status: '',
    policy_type: '',
    date_from: '',
    date_to: ''
  });

  const { data: requests, isLoading } = useQuery(
    ['requests', filters], 
    () => fetchRequests(filters)
  );

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-xl font-semibold text-gray-900">Mis Solicitudes</h1>
          <p className="mt-2 text-sm text-gray-700">
            Historial completo de tus solicitudes de tiempo libre.
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <Link
            to="/requests/new"
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-primary-green px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-dark"
          >
            Nueva Solicitud
          </Link>
        </div>
      </div>

      <RequestsFilters filters={filters} onFiltersChange={setFilters} />

      {isLoading ? (
        <RequestsTableSkeleton />
      ) : (
        <RequestsTable requests={requests} />
      )}
    </div>
  );
};
```

#### `RequestDetails.tsx`
Vista detallada de una solicitud específica.

```tsx
const RequestDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { data: request, isLoading } = useQuery(['request', id], () => fetchRequest(id!));

  if (isLoading) return <RequestDetailsSkeleton />;
  if (!request) return <NotFound />;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Solicitud #{request.id}
              </h3>
              <p className="mt-1 max-w-2xl text-sm text-gray-500">
                {request.policy.name} • {formatDateRange(request.start_date, request.end_date)}
              </p>
            </div>
            <RequestStatusBadge status={request.status} />
          </div>
        </div>
        
        <div className="border-t border-gray-200">
          <dl>
            <RequestDetailRow label="Empleado" value={request.user.name} />
            <RequestDetailRow label="Tipo de Solicitud" value={request.policy.name} />
            <RequestDetailRow label="Fechas" value={formatDateRange(request.start_date, request.end_date)} />
            <RequestDetailRow label="Días Hábiles" value={request.business_days} />
            <RequestDetailRow label="Motivo" value={request.reason} />
            {request.notes && <RequestDetailRow label="Notas" value={request.notes} />}
            <RequestDetailRow label="Estado" value={<RequestStatusBadge status={request.status} />} />
            <RequestDetailRow label="Fecha de Solicitud" value={formatDateTime(request.created_at)} />
            {request.approver && (
              <RequestDetailRow label="Aprobador" value={request.approver.name} />
            )}
          </dl>
        </div>

        {request.approval_history && (
          <ApprovalHistory history={request.approval_history} />
        )}

        {request.attachments && request.attachments.length > 0 && (
          <AttachmentsList attachments={request.attachments} />
        )}

        {request.status === 'pending' && (
          <RequestActions request={request} />
        )}
      </div>
    </div>
  );
};
```

### 5. Calendar Components

#### `CalendarView.tsx`
Vista de calendario compartido del equipo.

```tsx
const CalendarView: React.FC = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [viewType, setViewType] = useState<'month' | 'week'>('month');
  
  const { data: absences } = useQuery(
    ['calendar', format(currentDate, 'yyyy-MM')],
    () => fetchCalendarAbsences(currentDate)
  );

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Calendario del Equipo</h1>
          <p className="mt-2 text-sm text-gray-700">
            Vista de ausencias programadas y solicitudes pendientes.
          </p>
        </div>
        
        <div className="mt-4 sm:mt-0 flex items-center space-x-4">
          <CalendarViewToggle viewType={viewType} onViewTypeChange={setViewType} />
          <CalendarNavigation 
            currentDate={currentDate} 
            onDateChange={setCurrentDate}
            viewType={viewType}
          />
        </div>
      </div>

      <CalendarFilters />

      <div className="bg-white shadow rounded-lg overflow-hidden">
        {viewType === 'month' ? (
          <MonthCalendar 
            currentDate={currentDate}
            absences={absences}
            onDateClick={handleDateClick}
          />
        ) : (
          <WeekCalendar 
            currentDate={currentDate}
            absences={absences}
            onDateClick={handleDateClick}
          />
        )}
      </div>

      <CalendarLegend />
    </div>
  );
};
```

### 6. Admin Components

#### `AdminDashboard.tsx`
Panel administrativo para managers y RRHH.

```tsx
const AdminDashboard: React.FC = () => {
  const { data: stats } = useQuery('admin-stats', fetchAdminStats);
  const { data: pendingRequests } = useQuery('pending-requests', fetchPendingRequests);

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-2xl font-bold leading-6 text-gray-900">
          Panel Administrativo
        </h1>
        <p className="mt-2 max-w-4xl text-sm text-gray-500">
          Gestión de solicitudes, usuarios y reportes del sistema.
        </p>
      </div>

      <AdminStatsGrid stats={stats} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PendingApprovalsCard requests={pendingRequests} />
        <RecentActivityCard />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <DepartmentSummaryCard />
        <PolicyUsageCard />
        <UpcomingAbsencesCard />
      </div>
    </div>
  );
};
```

#### `PendingApprovals.tsx`
Lista de solicitudes pendientes de aprobación.

```tsx
const PendingApprovals: React.FC = () => {
  const { data: requests, isLoading } = useQuery('pending-approvals', fetchPendingApprovals);
  const approveMutation = useMutation(approveRequest);
  const rejectMutation = useMutation(rejectRequest);

  const handleApprove = async (requestId: number, notes?: string) => {
    try {
      await approveMutation.mutateAsync({ requestId, notes });
      // Refresh data
    } catch (error) {
      // Handle error
    }
  };

  const handleReject = async (requestId: number, reason: string, notes?: string) => {
    try {
      await rejectMutation.mutateAsync({ requestId, reason, notes });
      // Refresh data
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-xl font-semibold text-gray-900">Solicitudes Pendientes</h1>
          <p className="mt-2 text-sm text-gray-700">
            Revisa y aprueba las solicitudes de tu equipo.
          </p>
        </div>
      </div>

      {isLoading ? (
        <PendingApprovalsTableSkeleton />
      ) : (
        <PendingApprovalsTable 
          requests={requests}
          onApprove={handleApprove}
          onReject={handleReject}
          isApproving={approveMutation.isLoading}
          isRejecting={rejectMutation.isLoading}
        />
      )}
    </div>
  );
};
```

## State Management

### Auth Context
```tsx
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  const login = async (email: string, password: string, rememberMe = false) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const response = await authAPI.login(email, password);
      const { access_token, refresh_token, user } = response.data;
      
      // Store tokens
      tokenStorage.setAccessToken(access_token);
      tokenStorage.setRefreshToken(refresh_token, rememberMe);
      
      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'LOGIN_ERROR', payload: error.message });
      throw error;
    }
  };

  const logout = () => {
    tokenStorage.clearTokens();
    dispatch({ type: 'LOGOUT' });
  };

  // Auto-refresh token logic
  useEffect(() => {
    const token = tokenStorage.getAccessToken();
    if (token && !isTokenExpired(token)) {
      // Validate token and set user
      validateToken(token);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ ...state, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### API Client Configuration
```tsx
// api/client.ts
import axios from 'axios';
import { tokenStorage } from '../utils/tokenStorage';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = tokenStorage.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = tokenStorage.getRefreshToken();
        if (refreshToken) {
          const response = await axios.post('/auth/refresh', { refresh_token: refreshToken });
          const { access_token } = response.data;
          
          tokenStorage.setAccessToken(access_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        tokenStorage.clearTokens();
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
```

## Paleta de Colores y Estilos

### Configuración Tailwind CSS
```js
// tailwind.config.js
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          green: '#2E7D32',
          light: '#4CAF50',
          dark: '#1B5E20',
        },
        accent: {
          light: '#C8E6C9',
          mint: '#E8F5E8',
        },
        gray: {
          50: '#FAFAFA',
          100: '#F5F5F5',
          200: '#EEEEEE',
          300: '#E0E0E0',
          400: '#BDBDBD',
          500: '#9E9E9E',
          600: '#757575',
          700: '#616161',
          800: '#424242',
          900: '#212121',
        },
        success: '#4CAF50',
        warning: '#FF9800',
        error: '#F44336',
        info: '#2196F3',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

### Componentes de Estilo Reutilizables
```tsx
// components/ui/Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

const Button: React.FC<ButtonProps> = ({ 
  variant = 'primary', 
  size = 'md', 
  isLoading = false,
  children,
  className,
  disabled,
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors duration-200';
  
  const variantClasses = {
    primary: 'bg-primary-green text-white hover:bg-primary-dark focus:ring-primary-green',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    outline: 'border border-primary-green text-primary-green hover:bg-primary-green hover:text-white focus:ring-primary-green',
    ghost: 'text-primary-green hover:bg-accent-light focus:ring-primary-green',
  };
  
  const sizeClasses = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className} ${
        (disabled || isLoading) ? 'opacity-50 cursor-not-allowed' : ''
      }`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && <LoadingSpinner className="mr-2 h-4 w-4" />}
      {children}
    </button>
  );
};
```

## Utilidades y Helpers

### Date Utilities
```tsx
// utils/dateUtils.ts
import { format, parseISO, differenceInBusinessDays, isWeekend } from 'date-fns';
import { es } from 'date-fns/locale';

export const formatDate = (date: string | Date): string => {
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  return format(dateObj, 'dd/MM/yyyy', { locale: es });
};

export const formatDateTime = (date: string | Date): string => {
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  return format(dateObj, 'dd/MM/yyyy HH:mm', { locale: es });
};

export const formatDateRange = (startDate: string, endDate: string): string => {
  return `${formatDate(startDate)} - ${formatDate(endDate)}`;
};

export const calculateBusinessDays = (startDate: string, endDate: string): number => {
  if (!startDate || !endDate) return 0;
  return differenceInBusinessDays(parseISO(endDate), parseISO(startDate)) + 1;
};

export const isHoliday = (date: Date): boolean => {
  // Colombian holidays logic
  const holidays = [
    '2024-01-01', // Año Nuevo
    '2024-01-08', // Reyes Magos
    '2024-03-25', // San José
    '2024-03-28', // Jueves Santo
    '2024-03-29', // Viernes Santo
    '2024-05-01', // Día del Trabajo
    '2024-05-13', // Ascensión
    '2024-06-03', // Corpus Christi
    '2024-06-10', // Sagrado Corazón
    '2024-07-01', // San Pedro y San Pablo
    '2024-07-20', // Independencia
    '2024-08-07', // Batalla de Boyacá
    '2024-08-19', // Asunción
    '2024-10-14', // Día de la Raza
    '2024-11-04', // Todos los Santos
    '2024-11-11', // Independencia de Cartagena
    '2024-12-08', // Inmaculada Concepción
    '2024-12-25', // Navidad
  ];
  
  const dateString = format(date, 'yyyy-MM-dd');
  return holidays.includes(dateString);
};
```

### Form Validation Schemas
```tsx
// utils/validationSchemas.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(1, 'Contraseña requerida'),
  rememberMe: z.boolean().optional(),
});

export const requestSchema = z.object({
  policy_id: z.number().min(1, 'Selecciona un tipo de solicitud'),
  start_date: z.string().min(1, 'Fecha de inicio requerida'),
  end_date: z.string().min(1, 'Fecha de fin requerida'),
  reason: z.string().min(10, 'El motivo debe tener al menos 10 caracteres'),
  notes: z.string().optional(),
  half_day: z.boolean().optional(),
}).refine((data) => {
  return new Date(data.end_date) >= new Date(data.start_date);
}, {
  message: 'La fecha de fin debe ser posterior a la fecha de inicio',
  path: ['end_date'],
});

export const userProfileSchema = z.object({
  name: z.string().min(2, 'Nombre debe tener al menos 2 caracteres'),
  phone: z.string().optional(),
  emergency_contact: z.object({
    name: z.string().min(2, 'Nombre del contacto requerido'),
    phone: z.string().min(10, 'Teléfono del contacto requerido'),
    relationship: z.string().min(1, 'Relación requerida'),
  }).optional(),
});
```

## Testing Strategy

### Component Testing
```tsx
// __tests__/components/LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import LoginForm from '../components/LoginForm';

const renderWithProviders = (component: React.ReactElement) => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {component}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('LoginForm', () => {
  test('renders login form correctly', () => {
    renderWithProviders(<LoginForm />);
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /iniciar sesión/i })).toBeInTheDocument();
  });

  test('shows validation errors for empty fields', async () => {
    renderWithProviders(<LoginForm />);
    
    const submitButton = screen.getByRole('button', { name: /iniciar sesión/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/email inválido/i)).toBeInTheDocument();
      expect(screen.getByText(/contraseña requerida/i)).toBeInTheDocument();
    });
  });

  test('submits form with valid data', async () => {
    const mockLogin = jest.fn();
    renderWithProviders(<LoginForm />);
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@comfachoco.com' }
    });
    fireEvent.change(screen.getByLabelText(/contraseña/i), {
      target: { value: 'password123' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /iniciar sesión/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@comfachoco.com', 'password123', false);
    });
  });
});
```

### E2E Testing Setup
```tsx
// cypress/e2e/auth.cy.ts
describe('Authentication Flow', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login successfully with valid credentials', () => {
    cy.get('[data-testid="email-input"]').type('admin@comfachoco.com');
    cy.get('[data-testid="password-input"]').type('password123');
    cy.get('[data-testid="login-button"]').click();

    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="user-menu"]').should('contain', 'Admin User');
  });

  it('should show error message with invalid credentials', () => {
    cy.get('[data-testid="email-input"]').type('invalid@email.com');
    cy.get('[data-testid="password-input"]').type('wrongpassword');
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="error-message"]').should('be.visible');
    cy.url().should('include', '/login');
  });
});

describe('Request Management', () => {
  beforeEach(() => {
    cy.login('employee@comfachoco.com', 'password123');
    cy.visit('/requests/new');
  });

  it('should create a new vacation request', () => {
    cy.get('[data-testid="policy-select"]').select('Vacaciones Anuales');
    cy.get('[data-testid="start-date"]').type('2024-12-15');
    cy.get('[data-testid="end-date"]').type('2024-12-20');
    cy.get('[data-testid="reason-textarea"]').type('Vacaciones familiares');
    cy.get('[data-testid="submit-button"]').click();

    cy.url().should('include', '/requests');
    cy.get('[data-testid="success-message"]').should('be.visible');
  });
});
```

## Performance Optimization

### Code Splitting
```tsx
// Lazy loading for routes
const Dashboard = lazy(() => import('../pages/Dashboard'));
const RequestsList = lazy(() => import('../pages/RequestsList'));
const RequestForm = lazy(() => import('../pages/RequestForm'));
const CalendarView = lazy(() => import('../pages/CalendarView'));
const AdminDashboard = lazy(() => import('../pages/AdminDashboard'));

// Route configuration with Suspense
const AppRoutes = () => (
  <Routes>
    <Route path="/login" element={<LoginForm />} />
    <Route path="/" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
      <Route index element={
        <Suspense fallback={<PageSkeleton />}>
          <Dashboard />
        </Suspense>
      } />
      <Route path="requests" element={
        <Suspense fallback={<PageSkeleton />}>
          <RequestsList />
        </Suspense>
      } />
      {/* More routes... */}
    </Route>
  </Routes>
);
```

### Bundle Optimization
```js
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@headlessui/react', 'lucide-react'],
          utils: ['date-fns', 'axios', 'react-query'],
        },
      },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
  },
});
```

## Deployment Configuration

### Environment Variables
```bash
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=AndesMindHack
VITE_ENVIRONMENT=development

# .env.production
VITE_API_BASE_URL=https://andesmind-hack-api.railway.app/api/v1
VITE_APP_NAME=AndesMindHack
VITE_ENVIRONMENT=production
```

### Build Scripts
```json
{
  "scripts": {
    "dev": "vite --host 0.0.0.0 --port 3000",
    "build": "tsc && vite build",
    "preview": "vite preview --host 0.0.0.0 --port 3000",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "e2e": "cypress run",
    "e2e:open": "cypress open",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint src --ext ts,tsx --fix"
  }
}
```

---

*Documento técnico para AndesMindHack Frontend - Comfachocó 2024*