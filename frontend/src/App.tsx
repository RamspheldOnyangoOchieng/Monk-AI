import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import LiveWorkflowDemo from './components/LiveWorkflowDemo';
import Navigation from './components/Navigation';
import CodeOptimizer from './pages/CodeOptimizer';
import DocGenerator from './pages/DocGenerator';
import Domains from './pages/Domains';
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

import PRReviewer from './pages/PRReviewer';
import SecurityAnalyzer from './pages/SecurityAnalyzer';
import TestGenerator from './pages/TestGenerator';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<LiveWorkflowDemo />} />
            <Route path="/ideation" element={<Ideation />} />
            <Route path="/code-optimizer" element={<CodeOptimizer />} />
            <Route path="/doc-generator" element={<DocGenerator />} />
            <Route path="/security-analyzer" element={<SecurityAnalyzer />} />
            <Route path="/test-generator" element={<TestGenerator />} />
            <Route path="/pr-reviewer" element={<PRReviewer />} />
            <Route path="/domains" element={<Domains />} />
          </Routes>
        </main>
      </div>
    </Router>

  );
}

export default App;
