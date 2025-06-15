import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Alert,
  Paper,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  CircularProgress,
  Divider,
  LinearProgress
} from '@mui/material';
import {
  RateReview as ReviewIcon,
  BugReport as IssueIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  GitHub as GitHubIcon
} from '@mui/icons-material';
import axios from 'axios';

interface PRReviewResult {
  review_summary: {
    overall_rating: number;
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  };
  detailed_analysis: {
    code_quality: {
      score: number;
      issues: Array<{
        type: string;
        severity: string;
        description: string;
        line_number?: number;
        file_path?: string;
      }>;
    };
    security_concerns: Array<{
      type: string;
      severity: string;
      description: string;
      recommendation: string;
    }>;
    performance_issues: Array<{
      type: string;
      impact: string;
      description: string;
      suggestion: string;
    }>;
  };
  suggestions: Array<{
    type: string;
    priority: string;
    description: string;
    implementation: string;
  }>;
}

const PRReviewer: React.FC = () => {
  const [prUrl, setPrUrl] = useState('');
  const [repository, setRepository] = useState('');
  const [branch, setBranch] = useState('main');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PRReviewResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prUrl.trim() || !repository.trim()) {
      setError('Please provide both PR URL and repository name');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/review-pr', {
        pr_url: prUrl,
        repository: repository,
        branch: branch
      });

      setResult(response.data);
    } catch (error) {
      console.error('PR Review failed:', error);
      setError(error instanceof Error ? error.message : 'Failed to review PR');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'info';
      default: return 'default';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high': return <ErrorIcon color="error" />;
      case 'medium': return <WarningIcon color="warning" />;
      case 'low': return <IssueIcon color="info" />;
      default: return <CheckIcon color="success" />;
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ color: '#9c27b0', fontWeight: 600 }}>
          🔍 PR Reviewer
        </Typography>
        <Typography variant="body1" sx={{ color: '#ccc', mb: 2 }}>
          AI-powered pull request analysis with code quality, security, and performance insights
        </Typography>
      </Box>

      {/* Input Form */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ color: '#9c27b0' }}>
            Pull Request Details
          </Typography>
          
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="PR URL"
              value={prUrl}
              onChange={(e) => setPrUrl(e.target.value)}
              placeholder="https://github.com/owner/repo/pull/123"
              sx={{ mb: 2 }}
              disabled={loading}
              required
            />

            <TextField
              fullWidth
              label="Repository"
              value={repository}
              onChange={(e) => setRepository(e.target.value)}
              placeholder="owner/repository-name"
              sx={{ mb: 2 }}
              disabled={loading}
              required
            />

            <TextField
              fullWidth
              label="Branch (optional)"
              value={branch}
              onChange={(e) => setBranch(e.target.value)}
              placeholder="main"
              sx={{ mb: 3 }}
              disabled={loading}
            />

            <Button
              type="submit"
              variant="contained"
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <ReviewIcon />}
              disabled={loading || !prUrl.trim() || !repository.trim()}
              sx={{ 
                backgroundColor: '#9c27b0',
                '&:hover': { backgroundColor: '#7b1fa2' }
              }}
            >
              {loading ? 'Analyzing PR...' : 'Review Pull Request'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Loading Progress */}
      {loading && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Analyzing Pull Request...
            </Typography>
            <LinearProgress sx={{ mb: 2 }} />
            <Typography variant="body2" sx={{ color: '#ccc' }}>
              Reviewing code quality, security vulnerabilities, and performance issues...
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      {/* Results */}
      {result && (
        <Box>
          {/* Review Summary */}
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ color: '#9c27b0' }}>
                📊 Review Summary
              </Typography>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <Typography variant="h4" sx={{ color: '#00ff88', fontWeight: 600 }}>
                  {result.review_summary.overall_rating}/10
                </Typography>
                <Typography variant="body1" sx={{ color: '#ccc' }}>
                  Overall Rating
                </Typography>
              </Box>

              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
                {/* Strengths */}
                <Box>
                  <Typography variant="subtitle1" sx={{ color: '#4caf50', mb: 1, fontWeight: 600 }}>
                    ✅ Strengths
                  </Typography>
                  <List dense>
                    {result.review_summary.strengths.map((strength, index) => (
                      <ListItem key={index}>
                        <ListItemIcon sx={{ minWidth: 24 }}>
                          <CheckIcon sx={{ fontSize: 16, color: '#4caf50' }} />
                        </ListItemIcon>
                        <ListItemText primary={strength} />
                      </ListItem>
                    ))}
                  </List>
                </Box>

                {/* Weaknesses */}
                <Box>
                  <Typography variant="subtitle1" sx={{ color: '#ff9800', mb: 1, fontWeight: 600 }}>
                    ⚠️ Weaknesses
                  </Typography>
                  <List dense>
                    {result.review_summary.weaknesses.map((weakness, index) => (
                      <ListItem key={index}>
                        <ListItemIcon sx={{ minWidth: 24 }}>
                          <WarningIcon sx={{ fontSize: 16, color: '#ff9800' }} />
                        </ListItemIcon>
                        <ListItemText primary={weakness} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              </Box>

              {/* Recommendations */}
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle1" sx={{ color: '#2196f3', mb: 1, fontWeight: 600 }}>
                  💡 Recommendations
                </Typography>
                <List dense>
                  {result.review_summary.recommendations.map((recommendation, index) => (
                    <ListItem key={index}>
                      <ListItemIcon sx={{ minWidth: 24 }}>
                        <CheckIcon sx={{ fontSize: 16, color: '#2196f3' }} />
                      </ListItemIcon>
                      <ListItemText primary={recommendation} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            </CardContent>
          </Card>

          {/* Code Quality Issues */}
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ color: '#9c27b0' }}>
                🔧 Code Quality Analysis
              </Typography>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <Typography variant="h5" sx={{ color: '#00ff88', fontWeight: 600 }}>
                  {result.detailed_analysis.code_quality.score}/100
                </Typography>
                <Typography variant="body1" sx={{ color: '#ccc' }}>
                  Quality Score
                </Typography>
              </Box>

              {result.detailed_analysis.code_quality.issues.map((issue, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Paper sx={{ p: 2, backgroundColor: '#2d2d2d' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                      {getSeverityIcon(issue.severity)}
                      <Chip 
                        label={issue.severity}
                        color={getSeverityColor(issue.severity) as any}
                        size="small"
                      />
                      <Chip 
                        label={issue.type}
                        variant="outlined"
                        size="small"
                      />
                      {issue.file_path && (
                        <Typography variant="caption" sx={{ color: '#666' }}>
                          {issue.file_path}:{issue.line_number}
                        </Typography>
                      )}
                    </Box>
                    <Typography variant="body2">
                      {issue.description}
                    </Typography>
                  </Paper>
                </Box>
              ))}
            </CardContent>
          </Card>

          {/* Security Concerns */}
          {result.detailed_analysis.security_concerns.length > 0 && (
            <Card sx={{ mb: 4 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ color: '#9c27b0' }}>
                  🔒 Security Analysis
                </Typography>
                
                {result.detailed_analysis.security_concerns.map((concern, index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Paper sx={{ p: 2, backgroundColor: '#2d2d2d' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                        {getSeverityIcon(concern.severity)}
                        <Chip 
                          label={concern.severity}
                          color={getSeverityColor(concern.severity) as any}
                          size="small"
                        />
                        <Chip 
                          label={concern.type}
                          variant="outlined"
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        {concern.description}
                      </Typography>
                      <Typography variant="body2" sx={{ color: '#4caf50', fontStyle: 'italic' }}>
                        💡 {concern.recommendation}
                      </Typography>
                    </Paper>
                  </Box>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Performance Issues */}
          {result.detailed_analysis.performance_issues.length > 0 && (
            <Card sx={{ mb: 4 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ color: '#9c27b0' }}>
                  ⚡ Performance Analysis
                </Typography>
                
                {result.detailed_analysis.performance_issues.map((issue, index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Paper sx={{ p: 2, backgroundColor: '#2d2d2d' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                        <WarningIcon color="warning" />
                        <Chip 
                          label={issue.impact}
                          color="warning"
                          size="small"
                        />
                        <Chip 
                          label={issue.type}
                          variant="outlined"
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        {issue.description}
                      </Typography>
                      <Typography variant="body2" sx={{ color: '#4caf50', fontStyle: 'italic' }}>
                        💡 {issue.suggestion}
                      </Typography>
                    </Paper>
                  </Box>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Suggestions */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ color: '#9c27b0' }}>
                🚀 Improvement Suggestions
              </Typography>
              
              {result.suggestions.map((suggestion, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Paper sx={{ p: 2, backgroundColor: '#2d2d2d' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                      <CheckIcon color="success" />
                      <Chip 
                        label={suggestion.priority}
                        color={suggestion.priority === 'High' ? 'error' : suggestion.priority === 'Medium' ? 'warning' : 'info'}
                        size="small"
                      />
                      <Chip 
                        label={suggestion.type}
                        variant="outlined"
                        size="small"
                      />
                    </Box>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      {suggestion.description}
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#2196f3', fontStyle: 'italic' }}>
                      🛠️ {suggestion.implementation}
                    </Typography>
                  </Paper>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Box>
      )}
    </Box>
  );
};

export default PRReviewer; 