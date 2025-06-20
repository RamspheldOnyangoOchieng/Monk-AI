import {
    Alert,
    Box,
    Button,
    Checkbox,
    Chip,
    CircularProgress,
    Container,
    Divider,
    FormControl,
    FormControlLabel,
    FormGroup,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    TextField,
    Typography,
} from '@mui/material';
import axios from 'axios';
import React, { useState } from 'react';

interface Vulnerability {
  title: string;
  category: string;
  vulnerable_code: string;
  severity: string;
  impact: string;
  remediation: string[];
  secure_code: string;
  line_numbers: number[];
}

interface SecurityAnalysisResult {
  summary: string;
  vulnerabilities: Vulnerability[];
  total_issues: number;
  severity_counts: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    info: number;
  };
}

const languages = [
  'python',
  'javascript',
  'typescript',
  'java',
  'csharp',
  'go',
  'rust',
  'php',
];

const securityCategories = [
  { value: 'injection', label: 'Injection Vulnerabilities' },
  { value: 'authentication', label: 'Authentication Issues' },
  { value: 'data_exposure', label: 'Sensitive Data Exposure' },
  { value: 'xxe', label: 'XML External Entities (XXE)' },
  { value: 'access_control', label: 'Broken Access Control' },
  { value: 'security_misconfig', label: 'Security Misconfiguration' },
  { value: 'xss', label: 'Cross-Site Scripting (XSS)' },
  { value: 'insecure_deserialization', label: 'Insecure Deserialization' },
  { value: 'vulnerable_components', label: 'Vulnerable Components' },
  { value: 'insufficient_logging', label: 'Insufficient Logging & Monitoring' },
];

const SecurityAnalyzer = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [focusAreas, setFocusAreas] = useState<string[]>(['injection', 'authentication', 'data_exposure']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SecurityAnalysisResult | null>(null);

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
      const response = await axios.post('http://localhost:8000/api/analyze-security', {
        code,
        language,
        focus_areas: focusAreas,
      });

      setResult(response.data.security_analysis);
    } catch (err) {
      setError('Failed to analyze code for security vulnerabilities. Please try again.');
      console.error('Error analyzing code security:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Security Analyzer
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" paragraph>
          Analyze your code for security vulnerabilities and get remediation suggestions.
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
                Security Focus Areas
              </Typography>
              <FormGroup row>
                {securityCategories.map((category) => (
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
              {loading ? <CircularProgress size={24} /> : 'Analyze Security'}
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
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" gutterBottom>
                Security Analysis Results
              </Typography>
              <Box>
                <Chip 
                  label={`Total Issues: ${result.total_issues}`} 
                  color="primary" 
                  sx={{ mr: 1 }} 
                />
                {result.severity_counts.critical > 0 && (
                  <Chip 
                    label={`Critical: ${result.severity_counts.critical}`} 
                    color="error" 
                    sx={{ mr: 1 }} 
                  />
                )}
                {result.severity_counts.high > 0 && (
                  <Chip 
                    label={`High: ${result.severity_counts.high}`} 
                    color="error" 
                    variant="outlined"
                    sx={{ mr: 1 }} 
                  />
                )}
                {result.severity_counts.medium > 0 && (
                  <Chip 
                    label={`Medium: ${result.severity_counts.medium}`} 
                    color="warning" 
                    sx={{ mr: 1 }} 
                  />
                )}
              </Box>
            </Box>
            
            <Typography paragraph>{result.summary}</Typography>

            <Divider sx={{ my: 2 }} />

            {result.vulnerabilities.length > 0 ? (
              result.vulnerabilities.map((vulnerability, index) => (
                <VulnerabilityCard key={index} vulnerability={vulnerability} />
              ))
            ) : (
              <Alert severity="success">
                No security vulnerabilities were found in the analyzed code.
              </Alert>
            )}
          </Paper>
        )}
      </Box>
    </Container>
  );
};

// Component to display a vulnerability
const VulnerabilityCard = ({ vulnerability }: { vulnerability: Vulnerability }) => {
  return (
    <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1, border: 1, borderColor: 'divider' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Typography variant="subtitle1" fontWeight="bold">
          {vulnerability.title}
        </Typography>
        <Chip 
          label={vulnerability.severity.toUpperCase()} 
          color={getSeverityColor(vulnerability.severity as SeverityType) as any}
          size="small"
        />
      </Box>
      
      <Typography variant="caption" color="text.secondary" sx={{ mb: 2, display: 'block' }}>
        Category: {vulnerability.category}
        {vulnerability.line_numbers.length > 0 && (
          <> • Line{vulnerability.line_numbers.length > 1 ? 's' : ''}: {vulnerability.line_numbers.join(', ')}</>
        )}
      </Typography>

      <Typography variant="subtitle2" gutterBottom>Impact:</Typography>
      <Typography paragraph>{vulnerability.impact}</Typography>

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
          <Typography variant="caption" sx={{ position: 'absolute', top: 5, right: 10, color: 'error.main' }}>
            Vulnerable Code
          </Typography>
          <Typography component="pre" sx={{ m: 0, mt: 3, whiteSpace: 'pre-wrap' }}>
            {vulnerability.vulnerable_code}
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
            Secure Code
          </Typography>
          <Typography component="pre" sx={{ m: 0, mt: 3, whiteSpace: 'pre-wrap' }}>
            {vulnerability.secure_code}
          </Typography>
        </Paper>
      </Box>

      <Typography variant="subtitle2" gutterBottom>Remediation Steps:</Typography>
      <ul style={{ margin: 0, paddingLeft: '1.5rem' }}>
        {vulnerability.remediation.map((step, index) => (
          <li key={index}>
            <Typography>{step}</Typography>
          </li>
        ))}
      </ul>
    </Box>
  );
};

type SeverityType = 'critical' | 'high' | 'medium' | 'low' | 'default';
type ColorType = 'error' | 'warning' | 'info' | 'default';

const getSeverityColor = (severity: SeverityType): ColorType => {
  switch (severity.toLowerCase()) {
    case 'critical': return 'error';
    case 'high': return 'error';
    case 'medium': return 'warning';
    case 'low': return 'info';
    default: return 'default';
  }
};

export default SecurityAnalyzer;