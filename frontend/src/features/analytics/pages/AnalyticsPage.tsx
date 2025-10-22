import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { TrendingUp, Users, DollarSign, Target, Download } from 'lucide-react'

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Analytics</h1>
          <p className="text-muted-foreground mt-1">
            Track performance and insights across all campaigns
          </p>
        </div>
        <Button variant="outline">
          <Download className="mr-2 h-4 w-4" />
          Export Report
        </Button>
      </div>

      {/* KPIs */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$142,500</div>
            <p className="text-xs text-muted-foreground">+12.5% from last month</p>
            <div className="mt-3 h-2 w-full bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-green-500" style={{ width: '75%' }} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Sends</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2,847</div>
            <p className="text-xs text-muted-foreground">Across all campaigns</p>
            <div className="mt-3 h-2 w-full bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500" style={{ width: '82%' }} />
            </div>
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
            <div className="mt-3 h-2 w-full bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-purple-500" style={{ width: '62%' }} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Order Value</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$50.08</div>
            <p className="text-xs text-muted-foreground">+$3.20 from last month</p>
            <div className="mt-3 h-2 w-full bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-orange-500" style={{ width: '68%' }} />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Revenue Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-end justify-around gap-2">
              {[65, 78, 82, 71, 88, 95, 87].map((height, i) => (
                <div key={i} className="flex-1 flex flex-col items-center">
                  <div 
                    className="w-full bg-primary rounded-t transition-all hover:bg-primary/80"
                    style={{ height: `${height}%` }}
                  />
                  <span className="text-xs text-muted-foreground mt-2">
                    {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i]}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Segment Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { name: 'High Value Frequent', revenue: 45000, percentage: 32 },
                { name: 'Low Value Frequent', revenue: 28000, percentage: 20 },
                { name: 'High Churn Risk', revenue: 35000, percentage: 25 },
                { name: 'New Customers', revenue: 34500, percentage: 23 },
              ].map((segment, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium">{segment.name}</span>
                    <span className="text-sm text-muted-foreground">
                      ${(segment.revenue / 1000).toFixed(1)}K ({segment.percentage}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full"
                      style={{ width: `${segment.percentage * 3}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Campaign Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Campaign Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4">Campaign</th>
                  <th className="text-left py-3 px-4">Sends</th>
                  <th className="text-left py-3 px-4">Opens</th>
                  <th className="text-left py-3 px-4">Clicks</th>
                  <th className="text-left py-3 px-4">Conversions</th>
                  <th className="text-left py-3 px-4">Revenue</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { name: 'High Churn Win-back', sends: 1247, opens: 229, clicks: 87, conversions: 52, revenue: 42500 },
                  { name: 'Weekend Bundle Promotion', sends: 847, opens: 187, clicks: 65, conversions: 58, revenue: 38200 },
                  { name: 'Low-Value Uplift Series', sends: 753, opens: 142, clicks: 48, conversions: 31, revenue: 26800 },
                ].map((campaign, i) => (
                  <tr key={i} className="border-b hover:bg-muted/50">
                    <td className="py-3 px-4 font-medium">{campaign.name}</td>
                    <td className="py-3 px-4">{campaign.sends.toLocaleString()}</td>
                    <td className="py-3 px-4">
                      {campaign.opens}
                      <span className="text-xs text-muted-foreground ml-1">
                        ({((campaign.opens / campaign.sends) * 100).toFixed(1)}%)
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      {campaign.clicks}
                      <span className="text-xs text-muted-foreground ml-1">
                        ({((campaign.clicks / campaign.opens) * 100).toFixed(1)}%)
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      {campaign.conversions}
                      <span className="text-xs text-muted-foreground ml-1">
                        ({((campaign.conversions / campaign.sends) * 100).toFixed(1)}%)
                      </span>
                    </td>
                    <td className="py-3 px-4 font-semibold">
                      ${(campaign.revenue / 1000).toFixed(1)}K
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

