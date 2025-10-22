import { apiClient } from '../lib/api-client'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: {
    id: string
    email: string
    full_name?: string
    role: string
  }
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/login', credentials)
    return response.data
  },

  async register(data: RegisterData): Promise<any> {
    const response = await apiClient.post('/auth/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<any> {
    const response = await apiClient.get('/users/me')
    return response.data
  },
}

