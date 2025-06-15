import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import LiveWorkflowDemo from './components/LiveWorkflowDemo';
import Navigation from './components/Navigation';
import CodeOptimizer from './pages/CodeOptimizer';
import DocGenerator from './pages/DocGenerator';
import Domains from './pages/Domains';
import Ideation from './pages/Ideation';
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
