import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Box, 
  Tabs, 
  Tab, 
  Paper,
  Chip
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Psychology as PsychologyIcon,
  Code as CodeIcon,
  Description as DescriptionIcon,
  BugReport as BugReportIcon,
  Tune as TuneIcon,
  Security as SecurityIcon,
  RateReview as ReviewIcon,
  AutoAwesome as AutoAwesomeIcon,
  Group as GroupIcon,
  Visibility as VisibilityIcon
} from '@mui/icons-material';

interface NavigationItem {
  path: string;
  label: string;
  icon: React.ReactElement;
  color: string;
}

const navigationItems: NavigationItem[] = [
  {
    path: '/dashboard',
    label: 'Dashboard',
    icon: <DashboardIcon />,
    color: '#2196f3'
  },
  {
    path: '/orchestrator',
    label: 'Multi-Agent',
    icon: <AutoAwesomeIcon />,
    color: '#00ff88'
  },
  {
    path: '/ideation',
    label: 'Ideation',
    icon: <PsychologyIcon />,
    color: '#ff6b35'
  },
  {
    path: '/code-optimizer',
    label: 'Code Optimizer',
    icon: <TuneIcon />,
    color: '#3f51b5'
  },
  {
    path: '/test-generator',
    label: 'Test Generator',
    icon: <BugReportIcon />,
    color: '#f44336'
  },
  {
    path: '/security-analyzer',
    label: 'Security',
    icon: <SecurityIcon />,
    color: '#ff9800'
  },
  {
    path: '/doc-generator',
    label: 'Documentation',
    icon: <DescriptionIcon />,
    color: '#4caf50'
  },
  {
    path: '/pr-reviewer',
    label: 'PR Reviewer',
    icon: <ReviewIcon />,
    color: '#9c27b0'
  },
  {
    path: '/collaboration',
    label: 'Collaboration',
    icon: <GroupIcon />,
    color: '#2196f3'
  },
  {
    path: '/observability',
    label: 'Observability',
    icon: <VisibilityIcon />,
    color: '#e91e63'
  }
];

const Navigation: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
    navigate(newValue);
  };

  return (
    <Paper 
      elevation={0} 
      sx={{ 
        backgroundColor: '#1a1a1a', 
        borderBottom: '1px solid #333',
        px: 2
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 1 }}>
        <Chip 
          label="HACKATHON MODE" 
          size="small" 
          sx={{ 
            backgroundColor: '#00ff88', 
            color: '#000',
            fontWeight: 600,
            fontSize: '0.7rem'
          }} 
        />
        <Tabs
          value={location.pathname}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{
            flex: 1,
            '& .MuiTab-root': {
              textTransform: 'none',
              fontWeight: 500,
              minHeight: '48px',
              '&.Mui-selected': {
                color: '#00ff88',
              }
            },
            '& .MuiTabs-indicator': {
              backgroundColor: '#00ff88',
            }
          }}
        >
          {navigationItems.map((item) => (
            <Tab
              key={item.path}
              value={item.path}
              label={item.label}
              icon={item.icon}
              iconPosition="start"
              sx={{
                '& .MuiSvgIcon-root': {
                  color: item.color,
                  fontSize: '1.2rem'
                }
              }}
            />
          ))}
        </Tabs>
      </Box>
    </Paper>
  );
};

export default Navigation;