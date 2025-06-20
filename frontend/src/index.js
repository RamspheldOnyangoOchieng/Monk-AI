import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App.tsx';

// Create a stunning hackathon-ready theme
const theme = createTheme({
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
      default: 'transparent', // We'll use CSS for animated background
      paper: 'rgba(26, 26, 26, 0.85)',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b3b3b3',
    },
  },
  typography: {
    fontFamily: '"Inter", "JetBrains Mono", "Roboto", "Helvetica", sans-serif',
    h1: { fontWeight: 700, letterSpacing: '-0.02em' },
    h2: { fontWeight: 700, letterSpacing: '-0.02em' },
    h3: { fontWeight: 600, letterSpacing: '-0.01em' },
    h4: { fontWeight: 600, letterSpacing: '-0.01em' },
    h5: { fontWeight: 500 },
    h6: { fontWeight: 500 },
  },
  shape: {
    borderRadius: 16,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          background: `
            radial-gradient(circle at 20% 50%, rgba(0, 255, 136, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 107, 53, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
            linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)
          `,
          backgroundAttachment: 'fixed',
          minHeight: '100vh',
          '@keyframes pulse': {
            '0%': {
              transform: 'translate(-50%, -50%) scale(1)',
              opacity: 0.05,
            },
            '50%': {
              transform: 'translate(-50%, -50%) scale(1.05)',
              opacity: 0.08,
            },
            '100%': {
              transform: 'translate(-50%, -50%) scale(1)',
              opacity: 0.05,
            },
          },
          '@keyframes float': {
            '0%': { transform: 'translateY(0px)' },
            '50%': { transform: 'translateY(-10px)' },
            '100%': { transform: 'translateY(0px)' },
          },
          '@keyframes glow': {
            '0%': { boxShadow: '0 0 20px rgba(0, 255, 136, 0.2)' },
            '50%': { boxShadow: '0 0 40px rgba(0, 255, 136, 0.4)' },
            '100%': { boxShadow: '0 0 20px rgba(0, 255, 136, 0.2)' },
          },
          '&::before': {
            content: '""',
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: `
              radial-gradient(circle at 50% 50%, transparent 0%, rgba(0, 0, 0, 0.4) 100%),
              url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")
            `,
            pointerEvents: 'none',
            zIndex: -1,
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'rgba(26, 26, 26, 0.85)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)',
            border: '1px solid rgba(0, 255, 136, 0.3)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          background: 'rgba(26, 26, 26, 0.85)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: 16,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 12,
          padding: '10px 24px',
          fontSize: '0.95rem',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        },
        contained: {
          background: 'linear-gradient(135deg, #00ff88 0%, #00cc66 100%)',
          color: '#000000 !important', // Force dark text for better contrast
          boxShadow: '0 4px 20px rgba(0, 255, 136, 0.3)',
          '&:hover': {
            background: 'linear-gradient(135deg, #66ffaa 0%, #00ff88 100%)',
            color: '#000000 !important', // Force dark text on hover
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 30px rgba(0, 255, 136, 0.4)',
          },
          '&:disabled': {
            background: 'linear-gradient(135deg, #666666 0%, #444444 100%)',
            color: '#cccccc !important', // Light text for disabled state
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
          backdropFilter: 'blur(10px)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'rgba(26, 26, 26, 0.9)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
        },
        bar: {
          background: 'linear-gradient(90deg, #00ff88 0%, #66ffaa 100%)',
        },
      },
    },
  },
});

const root = ReactDOM.createRoot(
  document.getElementById('root')
);

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
); 