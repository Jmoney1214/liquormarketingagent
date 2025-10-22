import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Plus, Target, Calendar, TrendingUp, Users } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function CampaignsListPage() {
  // Mock data - will be replaced with real API calls
  const campaigns = [
    {
      id: 1,
      name: 'High Churn Win-back Campaign',
      status: 'active',
      progress: 85,
      sends: 1247,
      opens: 229,
      conversions: 52,
      revenue: 42500,
    },
    {
      id: 2,
      name: 'Weekend Bundle Promotion',
      status: 'active',
      progress: 45,
      sends: 847,
      opens: 187,
      conversions: 58,
      revenue: 38200,
    },
    {
      id: 3,
      name: 'Low-Value Uplift Series',
      status: 'scheduled',
      progress: 0,
      sends: 0,
      opens: 0,
      conversions: 0,
      revenue: 0,
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Campaigns</h1>
          <p className="text-muted-foreground mt-1">
            Create and manage your marketing campaigns
          </p>
        </div>
        <Link to="/campaigns/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Create Campaign
          </Button>
        </Link>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Campaigns</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2</div>
            <p className="text-xs text-muted-foreground">1 scheduled</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Sends</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2,094</div>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5.3%</div>
            <p className="text-xs text-muted-foreground">+0.8% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$80,700</div>
            <p className="text-xs text-muted-foreground">From campaigns</p>
          </CardContent>
        </Card>
      </div>

      {/* Campaign List */}
      <div className="grid gap-4">
        {campaigns.map((campaign) => (
          <Card key={campaign.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <CardTitle>{campaign.name}</CardTitle>
                    <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
                      campaign.status === 'active' ? 'bg-green-100 text-green-800' :
                      campaign.status === 'scheduled' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {campaign.status}
                    </span>
                  </div>
                  <CardDescription className="mt-2">
                    {campaign.status === 'active' && `${campaign.progress}% complete`}
                    {campaign.status === 'scheduled' && 'Starts tomorrow at 6:00 PM'}
                  </CardDescription>
                </div>
                <Link to={`/campaigns/${campaign.id}`}>
                  <Button variant="outline" size="sm">View Details</Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent>
              {campaign.status !== 'scheduled' && (
                <>
                  {/* Progress Bar */}
                  <div className="mb-4">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-primary h-2 rounded-full transition-all" 
                        style={{ width: `${campaign.progress}%` }}
                      />
                    </div>
                  </div>

                  {/* Metrics */}
                  <div className="grid grid-cols-4 gap-4">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Sends</p>
                      <p className="text-2xl font-bold">{campaign.sends.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Opens</p>
                      <p className="text-2xl font-bold">{campaign.opens}</p>
                      <p className="text-xs text-muted-foreground">
                        {((campaign.opens / campaign.sends) * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Conversions</p>
                      <p className="text-2xl font-bold">{campaign.conversions}</p>
                      <p className="text-xs text-muted-foreground">
                        {((campaign.conversions / campaign.sends) * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">Revenue</p>
                      <p className="text-2xl font-bold">${(campaign.revenue / 1000).toFixed(1)}K</p>
                    </div>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State for No Campaigns */}
      {campaigns.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center">
            <Target className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No campaigns yet</h3>
            <p className="text-muted-foreground mb-4">
              Create your first campaign to start engaging with customers
            </p>
            <Link to="/campaigns/new">
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Create Your First Campaign
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

