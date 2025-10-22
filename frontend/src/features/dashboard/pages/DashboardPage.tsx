import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { DollarSign, Users, Target, TrendingUp } from 'lucide-react'

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground mt-1">Welcome to Liquor Marketing Agent</p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$142,500</div>
            <p className="text-xs text-muted-foreground">+12.5% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Customers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2,847</div>
            <p className="text-xs text-muted-foreground">+234 this month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Campaigns</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">2 scheduled</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">18.4%</div>
            <p className="text-xs text-muted-foreground">+2.1% from last week</p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Active Campaigns</CardTitle>
            <CardDescription>Your currently running campaigns</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">High Churn Win-back Campaign</p>
                  <p className="text-sm text-muted-foreground">85% complete</p>
                </div>
                <div className="text-sm font-medium text-green-600">Active</div>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Weekend Bundle Promotion</p>
                  <p className="text-sm text-muted-foreground">Running</p>
                </div>
                <div className="text-sm font-medium text-green-600">Active</div>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Low-Value Uplift Series</p>
                  <p className="text-sm text-muted-foreground">Scheduled for tomorrow</p>
                </div>
                <div className="text-sm font-medium text-yellow-600">Scheduled</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Stats</CardTitle>
            <CardDescription>Last 7 days performance</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium">Messages Sent</p>
                <p className="text-2xl font-bold">2,847</p>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium">Opens</p>
                <p className="text-2xl font-bold">524</p>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium">Clicks</p>
                <p className="text-2xl font-bold">128</p>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium">Conversions</p>
                <p className="text-2xl font-bold">38</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

