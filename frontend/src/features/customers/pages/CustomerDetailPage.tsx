import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { apiClient } from '@/lib/api-client'
import { ArrowLeft, Mail, Phone, TrendingUp, ShoppingBag } from 'lucide-react'

export default function CustomerDetailPage() {
  const { id } = useParams()
  
  const { data: customer, isLoading } = useQuery({
    queryKey: ['customer', id],
    queryFn: async () => {
      const response = await apiClient.get(`/customers/${id}`)
      return response.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-8">Loading customer...</div>
  }

  if (!customer) {
    return <div className="text-center py-8">Customer not found</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to="/customers">
          <Button variant="outline" size="sm">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-3xl font-bold">{customer.name}</h1>
          <p className="text-muted-foreground mt-1">{customer.email}</p>
        </div>
        <Button>Edit Customer</Button>
      </div>

      {/* Customer Info Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Spent</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${customer.total_spent?.toFixed(2) || '0.00'}</div>
            <p className="text-xs text-muted-foreground">
              AOV: ${customer.avg_order_value?.toFixed(2) || '0.00'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Purchase Frequency</CardTitle>
            <ShoppingBag className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{customer.purchase_frequency || 0}</div>
            <p className="text-xs text-muted-foreground">Total orders</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">CLV Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${customer.clv_score?.toFixed(2) || '0.00'}</div>
            <p className="text-xs text-muted-foreground">Customer lifetime value</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Churn Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${
              customer.churn_risk === 'high' ? 'text-red-600' :
              customer.churn_risk === 'medium' ? 'text-yellow-600' :
              'text-green-600'
            }`}>
              {customer.churn_risk?.toUpperCase() || 'LOW'}
            </div>
            <p className="text-xs text-muted-foreground">Prediction</p>
          </CardContent>
        </Card>
      </div>

      {/* Details Section */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Customer Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3">
              <Mail className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Email</p>
                <p className="text-sm text-muted-foreground">{customer.email}</p>
              </div>
            </div>
            
            {customer.phone && (
              <div className="flex items-center gap-3">
                <Phone className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Phone</p>
                  <p className="text-sm text-muted-foreground">{customer.phone}</p>
                </div>
              </div>
            )}
            
            <div className="pt-4 border-t">
              <p className="text-sm font-medium mb-2">Segment</p>
              <span className="inline-flex items-center rounded-full px-3 py-1 text-sm font-medium bg-blue-100 text-blue-800">
                {customer.rfm_segment || 'Unknown'}
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Product Preferences</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm font-medium mb-1">Primary Category</p>
              <p className="text-lg font-semibold">{customer.primary_category || 'Not specified'}</p>
            </div>
            
            {customer.secondary_category && (
              <div>
                <p className="text-sm font-medium mb-1">Secondary Category</p>
                <p className="text-lg font-semibold">{customer.secondary_category}</p>
              </div>
            )}
            
            <div className="pt-4 border-t">
              <p className="text-sm font-medium mb-2">Behavioral Traits</p>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">Night Buyer</span>
                  <span className="text-sm font-medium">{customer.is_night_buyer ? 'Yes' : 'No'}</span>
                </div>
                {customer.avg_purchase_hour !== null && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Avg Purchase Hour</span>
                    <span className="text-sm font-medium">{customer.avg_purchase_hour}:00</span>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Activity Section */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-4">
            Purchase history and campaign engagement will appear here
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

