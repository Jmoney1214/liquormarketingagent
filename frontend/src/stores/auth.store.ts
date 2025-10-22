import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  full_name?: string
  role: string
}

interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  
  setAuth: (user: User, token: string, refreshToken: string) => void
  clearAuth: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      
      setAuth: (user, token, refreshToken) => {
        localStorage.setItem('access_token', token)
        localStorage.setItem('refresh_token', refreshToken)
        set({ user, token, refreshToken, isAuthenticated: true })
      },
      
      clearAuth: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ user: null, token: null, refreshToken: null, isAuthenticated: false })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)

