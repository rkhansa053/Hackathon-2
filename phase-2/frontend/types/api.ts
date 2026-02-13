export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface AuthResponse {
  success: boolean;
  user?: import('./user').User;
  token?: string; // For backward compatibility
  access_token?: string; // From backend API
  refresh_token?: string; // From backend API
  token_type?: string; // From backend API
  id?: string; // User ID from backend register API
  email?: string; // Email from backend register API
  created_at?: string; // From backend register API
  updated_at?: string; // From backend register API
  is_active?: boolean; // From backend register API
  error?: string;
}

export interface TaskListResponse {
  success: boolean;
  tasks?: import('./task').Task[];
  pagination?: {
    page: number;
    limit: number;
    total: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
  error?: string;
}

export interface TaskResponse {
  success: boolean;
  task?: import('./task').Task;
  error?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData extends LoginCredentials {}