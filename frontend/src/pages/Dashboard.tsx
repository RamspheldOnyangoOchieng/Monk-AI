import {
    BugReport as BugReportIcon,
    Code as CodeIcon,
    Description as DescriptionIcon,
    Speed as SpeedIcon,
    Security as SecurityIcon,
    // Science as ScienceIcon,
    LightbulbOutlined as IdeaIcon,
    TrendingUp as TrendingUpIcon,
    AccessTime as TimeIcon,
    CheckCircle as CheckCircleIcon,
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
    LinearProgress,
    Chip,
    Avatar,
} from '@mui/material';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

// Enhanced metrics for impressive demo
const dashboardMetrics = {
  totalProjects: 42,
  codeReviews: 186,
  testsGenerated: 1247,
  securityIssuesFixed: 89,
  timesSaved: "847 hours",
  developersHelped: "12.5k",
};

const features = [
  {
    title: 'Ideation & Planning',
    description: 'AI-powered project scoping and technical specifications',
    icon: <IdeaIcon sx={{ fontSize: 40 }} />,
    path: '/ideation',
    color: '#FF6B6B',
    metric: '42 projects scoped',
  },
  {
    title: 'PR Review',
    description: 'Automatically review pull requests and suggest improvements',
    icon: <CodeIcon sx={{ fontSize: 40 }} />,
    path: '/pr-review',
    color: '#4ECDC4',
    metric: '186 reviews completed',
  },
  {
    title: 'Documentation Generator',
    description: 'Generate comprehensive documentation for your code',
    icon: <DescriptionIcon sx={{ fontSize: 40 }} />,
    path: '/doc-generator',
    color: '#45B7D1',
    metric: '523 docs generated',
  },
  {
    title: 'Test Generator',
    description: 'Create test cases and improve code coverage',
    icon: <BugReportIcon sx={{ fontSize: 40 }} />,
    path: '/test-generator',
    color: '#96CEB4',
    metric: '1247 tests created',
  },
  {
    title: 'Code Optimizer',
    description: 'Optimize code performance and efficiency',
    icon: <SpeedIcon sx={{ fontSize: 40 }} />,
    path: '/code-optimizer',
    color: '#FFEAA7',
    metric: '34% avg improvement',
  },
  {
    title: 'Security Analyzer',
    description: 'Scan for vulnerabilities and security issues',
    icon: <SecurityIcon sx={{ fontSize: 40 }} />,
    path: '/security-analyzer',
    color: '#DDA0DD',
    metric: '89 vulnerabilities fixed',
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      delayChildren: 0.1,
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 100
    }
  }
};

function Dashboard() {
  const navigate = useNavigate();
  const [animatedMetrics, setAnimatedMetrics] = useState({
    projects: 0,
    reviews: 0,
    tests: 0,
    security: 0,
  });

  // Animate counter numbers for impact
  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedMetrics({
        projects: dashboardMetrics.totalProjects,
        reviews: dashboardMetrics.codeReviews,
        tests: dashboardMetrics.testsGenerated,
        security: dashboardMetrics.securityIssuesFixed,
      });
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  const handleFeatureClick = (path: string) => {
    navigate(path);
  };

  return (
    <Container maxWidth="lg">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Hero Section */}
        <motion.div variants={itemVariants}>
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography 
              variant="h2" 
              component="h1" 
              gutterBottom
              sx={{ 
                fontWeight: 'bold',
                background: 'linear-gradient(45deg, #FF6B6B, #4ECDC4)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 2
              }}
            >
              Monk AI Platform
            </Typography>
            <Typography variant="h5" color="text.secondary" sx={{ mb: 4 }}>
              Single-Screen Development • AI-Powered • Production-Ready
            </Typography>
            
            {/* Real-time Impact Metrics */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} sm={6} md={3}>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.5, type: "spring" }}
                >
                  <Card sx={{ textAlign: 'center', bgcolor: 'rgba(255, 107, 107, 0.1)' }}>
                    <CardContent>
                      <TrendingUpIcon sx={{ fontSize: 40, color: '#FF6B6B', mb: 1 }} />
                      <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                        {animatedMetrics.projects}
                      </Typography>
                      <Typography color="text.secondary">Projects Scoped</Typography>
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.7, type: "spring" }}
                >
                  <Card sx={{ textAlign: 'center', bgcolor: 'rgba(78, 205, 196, 0.1)' }}>
                    <CardContent>
                      <CheckCircleIcon sx={{ fontSize: 40, color: '#4ECDC4', mb: 1 }} />
                      <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                        {animatedMetrics.reviews}
                      </Typography>
                      <Typography color="text.secondary">Code Reviews</Typography>
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.9, type: "spring" }}
                >
                  <Card sx={{ textAlign: 'center', bgcolor: 'rgba(150, 206, 180, 0.1)' }}>
                    <CardContent>
                      <ScienceIcon sx={{ fontSize: 40, color: '#96CEB4', mb: 1 }} />
                      <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                        {animatedMetrics.tests}
                      </Typography>
                      <Typography color="text.secondary">Tests Generated</Typography>
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 1.1, type: "spring" }}
                >
                  <Card sx={{ textAlign: 'center', bgcolor: 'rgba(221, 160, 221, 0.1)' }}>
                    <CardContent>
                      <SecurityIcon sx={{ fontSize: 40, color: '#DDA0DD', mb: 1 }} />
                      <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                        {animatedMetrics.security}
                      </Typography>
                      <Typography color="text.secondary">Security Issues Fixed</Typography>
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
            </Grid>

            {/* Time Saved Banner */}
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 1.3 }}
            >
              <Card sx={{ 
                bgcolor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                mb: 4,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
              }}>
                <CardContent sx={{ textAlign: 'center', py: 3 }}>
                  <Typography variant="h3" component="div" sx={{ fontWeight: 'bold', mb: 1 }}>
                    {dashboardMetrics.timesSaved}
                  </Typography>
                  <Typography variant="h6">
                    Development Time Saved • {dashboardMetrics.developersHelped} Developers Empowered
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          </Box>
        </motion.div>

        {/* AI Agents Grid */}
        <motion.div variants={itemVariants}>
          <Typography variant="h3" component="h2" gutterBottom sx={{ mb: 4, textAlign: 'center' }}>
            AI Development Agents
          </Typography>
        </motion.div>

        <Grid container spacing={3}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={feature.title}>
              <motion.div
                variants={itemVariants}
                whileHover={{ 
                  scale: 1.05,
                  transition: { type: "spring", stiffness: 300 }
                }}
                whileTap={{ scale: 0.95 }}
              >
                <Card 
                  sx={{ 
                    height: '100%',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease-in-out',
                    border: `2px solid transparent`,
                    '&:hover': {
                      border: `2px solid ${feature.color}`,
                      boxShadow: `0 8px 32px rgba(0,0,0,0.12)`,
                    }
                  }}
                  onClick={() => handleFeatureClick(feature.path)}
                >
                  <CardContent sx={{ textAlign: 'center', pt: 3 }}>
                    <Avatar
                      sx={{
                        bgcolor: feature.color,
                        width: 80,
                        height: 80,
                        margin: '0 auto',
                        mb: 2,
                      }}
                    >
                      {feature.icon}
                    </Avatar>
                    <Typography variant="h5" component="h3" gutterBottom sx={{ fontWeight: 'bold' }}>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {feature.description}
                    </Typography>
                    <Chip 
                      label={feature.metric}
                      size="small"
                      sx={{ 
                        bgcolor: `${feature.color}20`,
                        color: feature.color,
                        fontWeight: 'bold'
                      }}
                    />
                  </CardContent>
                  <CardActions sx={{ justifyContent: 'center', pb: 3 }}>
                    <Button 
                      variant="contained" 
                      sx={{ 
                        bgcolor: feature.color,
                        '&:hover': {
                          bgcolor: feature.color,
                          filter: 'brightness(1.1)',
                        }
                      }}
                    >
                      Launch Agent
                    </Button>
                  </CardActions>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>

        {/* Call to Action */}
        <motion.div
          variants={itemVariants}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2 }}
        >
          <Box sx={{ textAlign: 'center', mt: 6, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
              Ready to Transform Your Development Workflow?
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              Join thousands of developers who've eliminated tool chaos and 10x'd their productivity
            </Typography>
            <Button 
              variant="contained" 
              size="large"
              sx={{ 
                bgcolor: '#FF6B6B',
                px: 4,
                py: 1.5,
                fontSize: '1.1rem',
                '&:hover': {
                  bgcolor: '#FF5252',
                }
              }}
              onClick={() => navigate('/ideation')}
            >
              Start Your First Project
            </Button>
          </Box>
        </motion.div>
      </motion.div>
    </Container>
  );
}

export default Dashboard;