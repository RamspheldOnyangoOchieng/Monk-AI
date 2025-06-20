import {
    BugReport as BugReportIcon,
    Code as CodeIcon,
    Description as DescriptionIcon,
    Speed as SpeedIcon,
    Security as SecurityIcon,
    // Science as ScienceIcon,
    LightbulbOutlined as IdeaIcon,
} from '@mui/icons-material';
import {
    Box,
    Button,
    Card,
    CardActions,
    CardContent,
    Container,
    Grid,
    Typography,
} from '@mui/material';
import React from 'react';
import { useNavigate } from 'react-router-dom';

const features = [
  {
    title: 'PR Review',
    description: 'Automatically review pull requests and suggest improvements',
    icon: <CodeIcon sx={{ fontSize: 40 }} />,
    path: '/pr-review',
  },
  {
    title: 'Documentation Generator',
    description: 'Generate comprehensive documentation for your code',
    icon: <DescriptionIcon sx={{ fontSize: 40 }} />,
    path: '/doc-generator',
  },
  {
    title: 'Test Generator',
    description: 'Create test cases and improve code coverage',
    icon: <BugReportIcon sx={{ fontSize: 40 }} />,
    path: '/test-generator',
  },
  {
    title: 'Code Optimizer',
    description: 'Analyze code for performance and quality improvements',
    icon: <SpeedIcon sx={{ fontSize: 40 }} />,
    path: '/code-optimizer',
  },
  {
    title: 'Security Analyzer',
    description: 'Scan your code for security vulnerabilities and receive detailed remediation steps',
    icon: <SecurityIcon sx={{ fontSize: 40 }} />,
    path: '/security-analyzer',
  },
  {
    title: 'Ideation',
    description: 'Define project scope, generate technical specifications, create user stories, and plan sprints',
    icon: <IdeaIcon sx={{ fontSize: 40 }} />,
    path: '/ideation',
  },
];

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome to TraeDevMate
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" paragraph>
          Your AI-powered development assistant for code review, documentation, and testing.
        </Typography>

        <Grid container spacing={4} sx={{ mt: 2 }}>
          {features.map((feature) => (
            <Grid item xs={12} sm={6} md={4} key={feature.title}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    transition: 'transform 0.2s ease-in-out',
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'center',
                      mb: 2,
                      color: 'primary.main',
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography gutterBottom variant="h5" component="h2" align="center">
                    {feature.title}
                  </Typography>
                  <Typography align="center" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    color="primary"
                    fullWidth
                    onClick={() => navigate(feature.path)}
                  >
                    Get Started
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;