import {
    Alert,
    Box,
    Button,
    CircularProgress,
    Container,
    Divider,
    FormControl,
    FormGroup,
    FormControlLabel,
    Checkbox,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    TextField,
    Typography,
} from '@mui/material';
import axios from 'axios';
import React, { useState } from 'react';

interface OptimizationItem {
  title: string;
  description: string;
  original_code: string;
  optimized_code: string;
  benefit: string;
  category: string;
}

interface OptimizationResult {
  summary: string;
  performance: OptimizationItem[];
  memory_usage: OptimizationItem[];
  code_quality: OptimizationItem[];
  algorithm_complexity: OptimizationItem[];
  resource_utilization: OptimizationItem[];
}

const languages = [
  'python',
  'javascript',
  'typescript',
  'java',
  'csharp',
  'go',
  'rust',
];

const optimizationCategories = [
  { value: 'performance', label: 'Performance' },
  { value: 'memory_usage', label: 'Memory Usage' },
  { value: 'code_quality', label: 'Code Quality' },
  { value: 'algorithm_complexity', label: 'Algorithm Complexity' },
  { value: 'resource_utilization', label: 'Resource Utilization' },
];

const CodeOptimizer = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [focusAreas, setFocusAreas] = useState<string[]>(['performance', 'code_quality']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<OptimizationResult | null>(null);

  const handleFocusAreaChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    if (event.target.checked) {
      setFocusAreas([...focusAreas, value]);
    } else {
      setFocusAreas(focusAreas.filter(area => area !== value));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/optimize-code', {
        code,
        language,
        focus_areas: focusAreas,
      });

      setResult(response.data.optimizations);
    } catch (err) {
      setError('Failed to analyze code for optimizations. Please try again.');
      console.error('Error analyzing code:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Code Optimizer
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" paragraph>
          Analyze your code for optimization opportunities and get actionable suggestions.
        </Typography>

        <Paper sx={{ p: 3, mb: 4 }}>
          <form onSubmit={handleSubmit}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Programming Language</InputLabel>
              <Select
                value={language}
                label="Programming Language"
                onChange={(e) => setLanguage(e.target.value)}
              >
                {languages.map((lang) => (
                  <MenuItem key={lang} value={lang}>
                    {lang.charAt(0).toUpperCase() + lang.slice(1)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl component="fieldset" fullWidth margin="normal">
              <Typography variant="subtitle2" gutterBottom>
                Optimization Focus Areas
              </Typography>
              <FormGroup row>
                {optimizationCategories.map((category) => (
                  <FormControlLabel
                    key={category.value}
                    control={
                      <Checkbox
                        checked={focusAreas.includes(category.value)}
                        onChange={handleFocusAreaChange}
                        value={category.value}
                      />
                    }
                    label={category.label}
                  />
                ))}
              </FormGroup>
            </FormControl>

            <TextField
              fullWidth
              label="Code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              margin="normal"
              required
              multiline
              rows={10}
              placeholder="Paste your code here..."
            />

            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              sx={{ mt: 2 }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Analyze Code'}
            </Button>
          </form>
        </Paper>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Optimization Summary
            </Typography>
            <Typography paragraph>{result.summary}</Typography>

            {/* Performance Optimizations */}
            {result.performance && result.performance.length > 0 && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom color="primary">
                  Performance Optimizations
                </Typography>
                {result.performance.map((optimization, index) => (
                  <OptimizationCard key={index} optimization={optimization} />
                ))}
              </>
            )}

            {/* Memory Optimizations */}
            {result.memory_usage && result.memory_usage.length > 0 && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom color="primary">
                  Memory Usage Optimizations
                </Typography>
                {result.memory_usage.map((optimization, index) => (
                  <OptimizationCard key={index} optimization={optimization} />
                ))}
              </>
            )}

            {/* Code Quality Improvements */}
            {result.code_quality && result.code_quality.length > 0 && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom color="primary">
                  Code Quality Improvements
                </Typography>
                {result.code_quality.map((optimization, index) => (
                  <OptimizationCard key={index} optimization={optimization} />
                ))}
              </>
            )}

            {/* Algorithm Improvements */}
            {result.algorithm_complexity && result.algorithm_complexity.length > 0 && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom color="primary">
                  Algorithm Complexity Improvements
                </Typography>
                {result.algorithm_complexity.map((optimization, index) => (
                  <OptimizationCard key={index} optimization={optimization} />
                ))}
              </>
            )}

            {/* Resource Optimizations */}
            {result.resource_utilization && result.resource_utilization.length > 0 && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom color="primary">
                  Resource Utilization Optimizations
                </Typography>
                {result.resource_utilization.map((optimization, index) => (
                  <OptimizationCard key={index} optimization={optimization} />
                ))}
              </>
            )}
          </Paper>
        )}
      </Box>
    </Container>
  );
};

// Component to display an optimization suggestion
const OptimizationCard = ({ optimization }: { optimization: OptimizationItem }) => {
  return (
    <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
      <Typography variant="subtitle1" fontWeight="bold">
        {optimization.title}
      </Typography>
      <Typography paragraph>{optimization.description}</Typography>

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
        <Paper
          sx={{
            p: 2,
            flex: 1,
            bgcolor: 'grey.900',
            fontFamily: 'monospace',
            position: 'relative',
          }}
        >
          <Typography variant="caption" sx={{ position: 'absolute', top: 5, right: 10, color: 'text.secondary' }}>
            Original Code
          </Typography>
          <Typography component="pre" sx={{ m: 0, mt: 3, whiteSpace: 'pre-wrap' }}>
            {optimization.original_code}
          </Typography>
        </Paper>

        <Paper
          sx={{
            p: 2,
            flex: 1,
            bgcolor: 'grey.900',
            fontFamily: 'monospace',
            position: 'relative',
          }}
        >
          <Typography variant="caption" sx={{ position: 'absolute', top: 5, right: 10, color: 'success.main' }}>
            Optimized Code
          </Typography>
          <Typography component="pre" sx={{ m: 0, mt: 3, whiteSpace: 'pre-wrap' }}>
            {optimization.optimized_code}
          </Typography>
        </Paper>
      </Box>

      <Typography variant="subtitle2">Benefit:</Typography>
      <Typography paragraph>{optimization.benefit}</Typography>
    </Box>
  );
};

export default CodeOptimizer;