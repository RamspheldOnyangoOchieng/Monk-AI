import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Button,
  LinearProgress,
  Alert,
  IconButton,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from '@mui/lab';
import {
  Refresh as RefreshIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Speed as SpeedIcon,
  Memory as MemoryIcon,
  Storage as StorageIcon,
  BugReport as BugReportIcon,
  Lightbulb as LightbulbIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';

// Mock data for the demo
const mockLogs = [
  { id: 1, timestamp: '2023-06-15 14:32:45', level: 'INFO', message: 'Application started successfully', source: 'app.core.main' },
  { id: 2, timestamp: '2023-06-15 14:33:12', level: 'INFO', message: 'Connected to database', source: 'app.core.database' },
  { id: 3, timestamp: '2023-06-15 14:35:22', level: 'WARNING', message: 'High memory usage detected', source: 'app.monitoring.system' },
  { id: 4, timestamp: '2023-06-15 14:36:01', level: 'ERROR', message: 'Failed to connect to OpenAI API', source: 'app.core.ai_service' },
  { id: 5, timestamp: '2023-06-15 14:36:45', level: 'INFO', message: 'Retrying connection to OpenAI API', source: 'app.core.ai_service' },
  { id: 6, timestamp: '2023-06-15 14:37:02', level: 'INFO', message: 'Successfully connected to OpenAI API', source: 'app.core.ai_service' },
  { id: 7, timestamp: '2023-06-15 14:38:15', level: 'INFO', message: 'Processing user request', source: 'app.api.routes.agents' },
  { id: 8, timestamp: '2023-06-15 14:39:30', level: 'WARNING', message: 'Slow database query detected', source: 'app.core.database' },
  { id: 9, timestamp: '2023-06-15 14:40:12', level: 'INFO', message: 'User request completed', source: 'app.api.routes.agents' },
  { id: 10, timestamp: '2023-06-15 14:41:05', level: 'ERROR', message: 'Failed to generate response from Gemini API', source: 'app.core.ai_service' },
];

const mockErrors = [
  { id: 1, timestamp: '2023-06-15 14:36:01', message: 'Failed to connect to OpenAI API', count: 1, status: 'resolved', solution: 'API key was refreshed automatically' },
  { id: 2, timestamp: '2023-06-15 14:41:05', message: 'Failed to generate response from Gemini API', count: 3, status: 'active', solution: 'Fallback to OpenAI API implemented' },
  { id: 3, timestamp: '2023-06-15 14:22:18', message: 'Database connection timeout', count: 2, status: 'investigating', solution: 'Checking database server load' },
  { id: 4, timestamp: '2023-06-15 13:15:42', message: 'Memory leak detected in agent orchestrator', count: 1, status: 'resolved', solution: 'Fixed resource cleanup in async handlers' },
];

const mockPerformanceMetrics = {
  responseTime: 245, // ms
  cpuUsage: 42, // %
  memoryUsage: 1.2, // GB
  requestsPerMinute: 28,
  errorRate: 0.8, // %
  uptime: '99.98%',
  coreWebVitals: {
    lcp: 1.8, // Largest Contentful Paint (seconds)
    fid: 42, // First Input Delay (ms)
    cls: 0.05, // Cumulative Layout Shift
  },
};

const mockIncidents = [
  {
    id: 1,
    timestamp: '2023-06-15 14:36:01',
    title: 'OpenAI API Connection Failure',
    description: 'The application failed to connect to the OpenAI API due to an authentication issue.',
    status: 'resolved',
    aiAnalysis: 'The API key was temporarily invalid. The system automatically refreshed the key and restored service.',
    impact: 'Low - 3 user requests affected',
    duration: '61 seconds',
  },
  {
    id: 2,
    timestamp: '2023-06-15 14:41:05',
    title: 'Gemini API Response Generation Failure',
    description: 'Multiple failures when attempting to generate responses using the Gemini API.',
    status: 'active',
    aiAnalysis: 'The Gemini API appears to be experiencing rate limiting. The system has implemented a fallback to OpenAI API to maintain service.',
    impact: 'Medium - 12 user requests affected',
    duration: 'Ongoing (4 minutes)',
  },
];

const Observability: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [logFilter, setLogFilter] = useState('all');
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleRefresh = () => {
    setIsRefreshing(true);
    // Simulate refresh delay
    setTimeout(() => {
      setIsRefreshing(false);
    }, 1000);
  };

  const filteredLogs = logFilter === 'all' 
    ? mockLogs 
    : mockLogs.filter(log => log.level === logFilter.toUpperCase());

  const getLogIcon = (level: string) => {
    switch (level) {
      case 'ERROR':
        return <ErrorIcon color="error" />;
      case 'WARNING':
        return <WarningIcon color="warning" />;
      case 'INFO':
        return <InfoIcon color="info" />;
      default:
        return <InfoIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'resolved':
        return 'success';
      case 'active':
        return 'error';
      case 'investigating':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getPerformanceStatus = (metric: number, thresholds: { good: number, warning: number }) => {
    if (metric <= thresholds.good) return 'success';
    if (metric <= thresholds.warning) return 'warning';
    return 'error';
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          <VisibilityIcon sx={{ mr: 1, verticalAlign: 'middle', color: '#00ff88' }} />
          Observability Dashboard
        </Typography>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={handleRefresh}
          disabled={isRefreshing}
        >
          Refresh Data
        </Button>
      </Box>

      {isRefreshing && <LinearProgress sx={{ mb: 2 }} />}

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{
            '& .MuiTab-root': {
              textTransform: 'none',
              fontWeight: 500,
            },
            '& .Mui-selected': {
              color: '#00ff88',
            },
            '& .MuiTabs-indicator': {
              backgroundColor: '#00ff88',
            },
          }}
        >
          <Tab label="Application Logs" icon={<InfoIcon />} iconPosition="start" />
          <Tab label="Error Reporting" icon={<BugReportIcon />} iconPosition="start" />
          <Tab label="Performance Metrics" icon={<SpeedIcon />} iconPosition="start" />
          <Tab label="Incident Management" icon={<WarningIcon />} iconPosition="start" />
        </Tabs>
      </Paper>

      {/* Application Logs Tab */}
      {activeTab === 0 && (
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">Real-time Application Logs</Typography>
            <FormControl variant="outlined" size="small" sx={{ minWidth: 150 }}>
              <InputLabel>Log Level</InputLabel>
              <Select
                value={logFilter}
                onChange={(e) => setLogFilter(e.target.value as string)}
                label="Log Level"
              >
                <MenuItem value="all">All Levels</MenuItem>
                <MenuItem value="info">Info</MenuItem>
                <MenuItem value="warning">Warning</MenuItem>
                <MenuItem value="error">Error</MenuItem>
              </Select>
            </FormControl>
          </Box>
          <Divider sx={{ mb: 2 }} />
          <List>
            {filteredLogs.map((log) => (
              <ListItem key={log.id} divider>
                <ListItemIcon>
                  {getLogIcon(log.level)}
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip
                        label={log.level}
                        size="small"
                        color={
                          log.level === 'ERROR' ? 'error' :
                          log.level === 'WARNING' ? 'warning' : 'info'
                        }
                        sx={{ fontWeight: 'bold' }}
                      />
                      <Typography variant="body1">{log.message}</Typography>
                    </Box>
                  }
                  secondary={
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 0.5 }}>
                      <Typography variant="caption" color="text.secondary">{log.source}</Typography>
                      <Typography variant="caption" color="text.secondary">{log.timestamp}</Typography>
                    </Box>
                  }
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {/* Error Reporting Tab */}
      {activeTab === 1 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Error Diagnostics</Typography>
          <Divider sx={{ mb: 2 }} />
          <Grid container spacing={3}>
            {mockErrors.map((error) => (
              <Grid item xs={12} key={error.id}>
                <Card variant="outlined" sx={{ borderColor: error.status === 'resolved' ? '#4caf50' : '#f44336' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <Box>
                        <Typography variant="h6" color="error">{error.message}</Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          First occurred: {error.timestamp} | Occurrences: {error.count}
                        </Typography>
                      </Box>
                      <Chip
                        label={error.status}
                        color={getStatusColor(error.status)}
                        sx={{ textTransform: 'capitalize' }}
                      />
                    </Box>
                    <Box sx={{ mt: 2, p: 2, bgcolor: 'rgba(0,0,0,0.1)', borderRadius: 1 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        <LightbulbIcon sx={{ fontSize: 16, mr: 0.5, color: '#00ff88', verticalAlign: 'text-bottom' }} />
                        AI-Generated Solution:
                      </Typography>
                      <Typography variant="body2">{error.solution}</Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}

      {/* Performance Metrics Tab */}
      {activeTab === 2 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Performance Monitoring</Typography>
          <Divider sx={{ mb: 3 }} />
          <Grid container spacing={3}>
            {/* Response Time */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>Average Response Time</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'baseline' }}>
                    <Typography variant="h4" component="div">
                      {mockPerformanceMetrics.responseTime}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>ms</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={(mockPerformanceMetrics.responseTime / 500) * 100}
                    color={getPerformanceStatus(mockPerformanceMetrics.responseTime, { good: 200, warning: 400 })}
                    sx={{ mt: 2, height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            </Grid>
            
            {/* CPU Usage */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>CPU Usage</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'baseline' }}>
                    <Typography variant="h4" component="div">
                      {mockPerformanceMetrics.cpuUsage}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={mockPerformanceMetrics.cpuUsage}
                    color={getPerformanceStatus(mockPerformanceMetrics.cpuUsage, { good: 50, warning: 80 })}
                    sx={{ mt: 2, height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            </Grid>
            
            {/* Memory Usage */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>Memory Usage</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'baseline' }}>
                    <Typography variant="h4" component="div">
                      {mockPerformanceMetrics.memoryUsage}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>GB</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={(mockPerformanceMetrics.memoryUsage / 2) * 100}
                    color={getPerformanceStatus(mockPerformanceMetrics.memoryUsage, { good: 1, warning: 1.5 })}
                    sx={{ mt: 2, height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            </Grid>
            
            {/* Core Web Vitals */}
            <Grid item xs={12}>
              <Card>
                <CardHeader title="Core Web Vitals" />
                <CardContent>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle1">Largest Contentful Paint (LCP)</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <Typography variant="h5">{mockPerformanceMetrics.coreWebVitals.lcp}s</Typography>
                        <Chip 
                          label={mockPerformanceMetrics.coreWebVitals.lcp < 2.5 ? "Good" : "Needs Improvement"}
                          color={mockPerformanceMetrics.coreWebVitals.lcp < 2.5 ? "success" : "warning"}
                          size="small"
                          sx={{ ml: 1 }}
                        />
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle1">First Input Delay (FID)</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <Typography variant="h5">{mockPerformanceMetrics.coreWebVitals.fid}ms</Typography>
                        <Chip 
                          label={mockPerformanceMetrics.coreWebVitals.fid < 100 ? "Good" : "Needs Improvement"}
                          color={mockPerformanceMetrics.coreWebVitals.fid < 100 ? "success" : "warning"}
                          size="small"
                          sx={{ ml: 1 }}
                        />
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle1">Cumulative Layout Shift (CLS)</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <Typography variant="h5">{mockPerformanceMetrics.coreWebVitals.cls}</Typography>
                        <Chip 
                          label={mockPerformanceMetrics.coreWebVitals.cls < 0.1 ? "Good" : "Needs Improvement"}
                          color={mockPerformanceMetrics.coreWebVitals.cls < 0.1 ? "success" : "warning"}
                          size="small"
                          sx={{ ml: 1 }}
                        />
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Incident Management Tab */}
      {activeTab === 3 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>AI-Generated Incident Summaries</Typography>
          <Divider sx={{ mb: 3 }} />
          <Timeline position="alternate">
            {mockIncidents.map((incident) => (
              <TimelineItem key={incident.id}>
                <TimelineSeparator>
                  <TimelineDot color={incident.status === 'resolved' ? 'success' : 'error'} />
                  <TimelineConnector />
                </TimelineSeparator>
                <TimelineContent>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                        <Typography variant="h6" component="div">{incident.title}</Typography>
                        <Chip
                          label={incident.status}
                          color={incident.status === 'resolved' ? 'success' : 'error'}
                          size="small"
                          sx={{ textTransform: 'capitalize' }}
                        />
                      </Box>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {incident.timestamp} | Duration: {incident.duration}
                      </Typography>
                      <Typography variant="body2" sx={{ mt: 1 }}>{incident.description}</Typography>
                      <Box sx={{ mt: 2, p: 2, bgcolor: 'rgba(0,255,136,0.05)', borderRadius: 1, border: '1px solid rgba(0,255,136,0.2)' }}>
                        <Typography variant="subtitle2" gutterBottom>
                          <LightbulbIcon sx={{ fontSize: 16, mr: 0.5, color: '#00ff88', verticalAlign: 'text-bottom' }} />
                          AI Analysis:
                        </Typography>
                        <Typography variant="body2">{incident.aiAnalysis}</Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Impact: {incident.impact}
                      </Typography>
                    </CardContent>
                  </Card>
                </TimelineContent>
              </TimelineItem>
            ))}
          </Timeline>
        </Paper>
      )}
    </Container>
  );
};

export default Observability;