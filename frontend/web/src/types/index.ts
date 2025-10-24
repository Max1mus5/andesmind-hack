// Core types for AndesMindHack Frontend

export interface User {
  id: number
  email: string
  name: string
  employee_id: string
  department?: string
  position?: string
  role: 'employee' | 'manager' | 'hr_admin'
  is_active: boolean
  created_at: string
  vacation_balance?: VacationBalance
  manager?: {
    id: number
    name: string
    email: string
  }
}

export interface VacationBalance {
  annual_days: number
  used_days: number
  remaining_days: number
  accrual_rate: number
}

export interface Policy {
  id: number
  name: string
  type: 'vacation' | 'sick_leave' | 'personal_leave'
  days_allocated: number
  requires_approval: boolean
  advance_notice_days: number
  max_consecutive_days?: number
  is_active: boolean
}

export interface TimeOffRequest {
  id: number
  user_id: number
  policy: Policy
  start_date: string
  end_date: string
  business_days: number
  calendar_days: number
  reason: string
  notes?: string
  status: 'pending' | 'approved' | 'rejected' | 'cancelled'
  half_day: boolean
  created_at: string
  updated_at: string
  approver?: {
    id: number
    name: string
    email?: string
  }
  user?: {
    id: number
    name: string
    employee_id: string
  }
}

export interface CreateRequestData {
  policy_id: number
  start_date: string
  end_date: string
  reason: string
  notes?: string
  half_day: boolean
}

export interface LoginCredentials {
  email: string
  password: string
  rememberMe?: boolean
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface CalendarAbsence {
  user: {
    id: number
    name: string
    department: string
  }
  request_id: number
  start_date: string
  end_date: string
  policy_type: string
  status: string
}

export interface CalendarData {
  period: {
    start_date: string
    end_date: string
  }
  absences: CalendarAbsence[]
  summary: {
    total_absences: number
    by_department: Record<string, number>
    by_status: Record<string, number>
  }
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

export interface ApiError {
  detail: string
  status_code?: number
}

// Form types
export interface LoginFormData {
  email: string
  password: string
  rememberMe: boolean
}

export interface RequestFormData {
  policy_id: number
  start_date: string
  end_date: string
  reason: string
  notes?: string
  half_day: boolean
}

export interface UserProfileFormData {
  name: string
  phone?: string
  emergency_contact?: {
    name: string
    phone: string
    relationship: string
  }
}

// UI Component types
export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  disabled?: boolean
  children: React.ReactNode
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  className?: string
}

export interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

export interface ToastType {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

// Filter types
export interface RequestFilters {
  status?: string
  policy_type?: string
  date_from?: string
  date_to?: string
  page?: number
  limit?: number
}

export interface CalendarFilters {
  start_date?: string
  end_date?: string
  department?: string
  include_pending?: boolean
}

// Chart/Analytics types
export interface DashboardStats {
  total_requests: number
  pending_requests: number
  approved_requests: number
  remaining_vacation_days: number
  used_vacation_days: number
}

export interface ReportData {
  period: {
    type: string
    year: number
    month?: number
  }
  summary: {
    total_requests: number
    approved: number
    rejected: number
    pending: number
    total_days_taken: number
    average_days_per_employee: number
  }
  by_department: Array<{
    department: string
    employees: number
    requests: number
    days_taken: number
    average_per_employee: number
  }>
  by_policy_type: Record<string, number>
}