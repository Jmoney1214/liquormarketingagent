import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './stores/auth.store'
import LoginPage from './features/auth/pages/LoginPage'
import RegisterPage from './features/auth/pages/RegisterPage'
import DashboardPage from './features/dashboard/pages/DashboardPage'
import CustomersListPage from './features/customers/pages/CustomersListPage'
import CustomerDetailPage from './features/customers/pages/CustomerDetailPage'
import CampaignsListPage from './features/campaigns/pages/CampaignsListPage'
import AnalyticsPage from './features/analytics/pages/AnalyticsPage'
import SettingsPage from './features/settings/pages/SettingsPage'
import AppLayout from './components/layout/AppLayout'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/customers" element={<CustomersListPage />} />
            <Route path="/customers/:id" element={<CustomerDetailPage />} />
            <Route path="/campaigns" element={<CampaignsListPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

// Protected route wrapper
function ProtectedRoute() {
  const { isAuthenticated } = useAuthStore()
  const token = useAuthStore((state) => state.token)
  
  if (!isAuthenticated && !token) {
    return <Navigate to="/login" replace />
  }
  
  return <AppLayout />
}

export default App

