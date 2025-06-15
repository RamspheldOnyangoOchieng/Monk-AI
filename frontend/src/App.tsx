import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Box,
} from '@mui/material';

// Import all components
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import MultiAgentOrchestrator from './pages/MultiAgentOrchestrator';
import Ideation from './pages/Ideation';
import CodeOptimizer from './pages/CodeOptimizer';
import TestGenerator from './pages/TestGenerator';
import SecurityAnalyzer from './pages/SecurityAnalyzer';
import DocGenerator from './pages/DocGenerator';
import PRReviewer from './pages/PRReviewer';
import LiveWorkflowDemo from './components/LiveWorkflowDemo';
import Collaboration from './pages/Collaboration';
import Observability from './pages/Observability';

// Create stunning hackathon-ready theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00ff88',
      light: '#66ffaa',
      dark: '#00cc66',
    },
    secondary: {
      main: '#ff6b35',
      light: '#ff8c61',
      dark: '#e55a2b',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1a1a1a',
    },
    text: {
      primary: '#ffffff',
      secondary: '#cccccc',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h3: {
      fontWeight: 700,
      letterSpacing: '-0.02em',
    },
    h4: {
      fontWeight: 600,
      letterSpacing: '-0.01em',
    },
    h5: {
      fontWeight: 500,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#1a1a1a',
          border: '1px solid #333',
          borderRadius: 12,
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            borderColor: '#00ff88',
            boxShadow: '0 8px 32px rgba(0, 255, 136, 0.1)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
        contained: {
          boxShadow: '0 4px 16px rgba(0, 255, 136, 0.3)',
          '&:hover': {
            boxShadow: '0 6px 24px rgba(0, 255, 136, 0.4)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#0a0a0a',
          borderBottom: '1px solid #333',
        },
      },
    },
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        {/* Header */}
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <Typography 
              variant="h6" 
              component="div" 
              sx={{ 
                flexGrow: 1,
                background: 'linear-gradient(45deg, #00ff88, #66ffaa)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontWeight: 700,
              }}
            >
              🧙‍♂️ Monk-AI TraeDevMate
            </Typography>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
              AI-Powered Multi-Agent Developer Productivity System
            </Typography>
          </Toolbar>
        </AppBar>

        {/* Navigation Tabs */}
        <Navigation />

        {/* Main Content */}
        <Box component="main" sx={{ flex: 1, backgroundColor: 'background.default', p: 0 }}>
          <Routes>
            {/* Default route redirects to dashboard */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            
            {/* Dashboard - Home page */}
            <Route path="/dashboard" element={<Dashboard />} />
            
            {/* Multi-Agent Orchestrator */}
            <Route path="/orchestrator" element={<MultiAgentOrchestrator />} />
            
            {/* Individual AI Agents */}
            <Route path="/ideation" element={<Ideation />} />
            <Route path="/code-optimizer" element={<CodeOptimizer />} />
            <Route path="/test-generator" element={<TestGenerator />} />
            <Route path="/security-analyzer" element={<SecurityAnalyzer />} />
            <Route path="/doc-generator" element={<DocGenerator />} />
            <Route path="/pr-reviewer" element={<PRReviewer />} />
            
            {/* Collaboration */}
            <Route path="/collaboration" element={<Collaboration />} />
            
            {/* Observability */}
            <Route path="/observability" element={<Observability />} />
            
            {/* Live Demo */}
            <Route path="/live-demo" element={<LiveWorkflowDemo />} />
            
            {/* Catch all route - redirect to dashboard */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;