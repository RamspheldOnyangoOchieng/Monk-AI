import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Dashboard from './pages/Dashboard';
import PRReview from './pages/PRReview';
import DocGenerator from './pages/DocGenerator';
import TestGenerator from './pages/TestGenerator';
import CodeOptimizer from './pages/CodeOptimizer';
import SecurityAnalyzer from './pages/SecurityAnalyzer';
import Ideation from './pages/Ideation';
import Code from './components/codeEditor';
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                TraeDevMate
              </Typography>
              <Button color="inherit" component={Link} href="/">
                Dashboard
              </Button>
              <Button color="inherit" component={Link} href="/pr-review">
                PR Review
              </Button>
              <Button color="inherit" component={Link} href="/doc-generator">
                Doc Generator
              </Button>
              <Button color="inherit" component={Link} href="/test-generator">
                Test Generator
              </Button>
              <Button color="inherit" component={Link} href="/code-optimizer">
                Code Optimizer
              </Button>
              <Button color="inherit" component={Link} href="/security-analyzer">
                Security Analyzer
              </Button>
              <Button color="inherit" component={Link} href="/ideation">
                Ideation
              </Button>
              <Button color="inherit" component={Link} href="/ide">
                Code Editor
              </Button>
            </Toolbar>
          </AppBar>

          <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/pr-review" element={<PRReview />} />
              <Route path="/doc-generator" element={<DocGenerator />} />
              <Route path="/test-generator" element={<TestGenerator />} />
              <Route path="/code-optimizer" element={<CodeOptimizer />} />
              <Route path="/security-analyzer" element={<SecurityAnalyzer />} />
              <Route path="/ideation" element={<Ideation />} />
              <Route path="/ide" element={<Code />} />
            </Routes>
          </Container>

          <Box component="footer" sx={{ py: 3, px: 2, mt: 'auto', backgroundColor: (theme) => theme.palette.grey[900] }}>
            <Container maxWidth="sm">
              <Typography variant="body2" color="text.secondary" align="center">
                {'© '}
                <Link color="inherit" href="https://traedevmate.com">
                  TraeDevMate
                </Link>{' '}
                {new Date().getFullYear()}
              </Typography>
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;