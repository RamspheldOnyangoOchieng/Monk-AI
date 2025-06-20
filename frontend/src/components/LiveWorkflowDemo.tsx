import {
    CheckCircle,
    Code,
    ExpandMore,
    Lightbulb,
    PlayArrow,
    RocketLaunch,
    Speed,
    WebAsset
} from '@mui/icons-material';
import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Container,
    FormControl,
    Grid,
    InputLabel,
    LinearProgress,
    List,
    ListItem,
    ListItemText,
    MenuItem,
    Paper,
    Select,
    Step,
    StepContent,
    StepLabel,
    Stepper,
    Tab,
    Tabs,
    TextField,
    Typography
} from '@mui/material';
import { styled } from '@mui/material/styles';
import React, { useCallback, useEffect, useState } from 'react';

const API_BASE_URL = 'http://localhost:8000';

interface WorkflowStep {
  step_id: string;
  agent_name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  start_time?: number;
  end_time?: number;
  result?: any;
  error?: string;
}

interface WorkflowStatus {
  workflow_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  current_step: number;
  total_steps: number;
  steps: WorkflowStep[];
  start_time: number;
  end_time?: number;
  results: Record<string, any>;
}

interface AutomatedPipelineStatus {
  pipeline_id: string;
  step: string;
  status: 'running' | 'completed' | 'failed';
  message: string;
  progress: number;
  result?: any;
  app_url?: string;
  app_preview?: string;
}

const StyledCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[8],
  },
}));

const StatusChip = styled(Chip)<{ status: string }>(({ theme, status }) => ({
  fontWeight: 'bold',
  ...(status === 'completed' && {
    backgroundColor: theme.palette.success.main,
    color: theme.palette.success.contrastText,
  }),
  ...(status === 'running' && {
    backgroundColor: theme.palette.warning.main,
    color: theme.palette.warning.contrastText,
  }),
  ...(status === 'failed' && {
    backgroundColor: theme.palette.error.main,
    color: theme.palette.error.contrastText,
  }),
  ...(status === 'pending' && {
    backgroundColor: theme.palette.grey[400],
    color: theme.palette.grey[800],
  }),
}));

const AppPreviewContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  minHeight: '400px',
  border: '2px solid #e0e0e0',
  borderRadius: '10px',
  position: 'relative',
  overflow: 'hidden',
}));

type AgentType = 'Ideation' | 'CodeOptimizer' | 'SecurityAnalyzer' | 'TestGenerator' | 'DocGenerator';
type ColorMap = Record<AgentType, string>;

const agentColors: ColorMap = {
  'Ideation': '#2196F3',
  'CodeOptimizer': '#FF9800',
  'SecurityAnalyzer': '#F44336',
  'TestGenerator': '#4CAF50',
  'DocGenerator': '#9C27B0',
};

const LiveWorkflowDemo: React.FC = () => {
  const [workflowStatus, setWorkflowStatus] = useState<WorkflowStatus | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState(0);
  
  // Automated Pipeline State
  const [pipelineStatus, setPipelineStatus] = useState<AutomatedPipelineStatus | null>(null);
  const [isPipelineRunning, setIsPipelineRunning] = useState(false);
  const [pipelineId, setPipelineId] = useState<string | null>(null);
  const [userIdea, setUserIdea] = useState('A task management app with user authentication and real-time updates');
  const [targetFramework, setTargetFramework] = useState('flask');
  const [showAppPreview, setShowAppPreview] = useState(false);
  
  // Form state
  const [projectDescription, setProjectDescription] = useState(
    'Build a complete task management application with user authentication, CRUD operations, and real-time updates'
  );
  const [programmingLanguage, setProgrammingLanguage] = useState('Python');
  const [workflowType, setWorkflowType] = useState('full_development');
  const [codeSample, setCodeSample] = useState(`def process_data(data_list):
    """Process a list of data items"""
    for item in data_list:
        # Process each item
        result = item * 2
        print(f"Processed: {result}")
    return result`);


  const agentIcons: Record<string, string> = {
    'IdeationAgent': '💡',
    'CodeOptimizer': '⚡',
    'SecurityAnalyzer': '🔒',
    'TestGenerator': '🧪',
    'DocGenerator': '📝',
    'CodeReviewer': '👀'
  };

  const pipelineSteps = {
    'ideation': { icon: <Lightbulb />, color: '#2196F3', name: 'AI Ideation' },
    'code_generation': { icon: <Code />, color: '#FF9800', name: 'Code Generation' },
    'optimization': { icon: <Speed />, color: '#9C27B0', name: 'Optimization' },
    'execution': { icon: <RocketLaunch />, color: '#4CAF50', name: 'App Execution' },
  };

  const startAutomatedPipeline = async () => {
    try {
      setIsPipelineRunning(true);
      setPipelineStatus(null);
      setShowAppPreview(false);
      
      const response = await fetch(`${API_BASE_URL}/api/workflow/automated-pipeline`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_idea: userIdea,
          target_framework: targetFramework,
          deployment_type: 'local',
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setPipelineId(result.pipeline_id);
      
      // Start streaming
      streamAutomatedPipeline(result.pipeline_id);
      
    } catch (error) {
      console.error('Error starting automated pipeline:', error);
      setIsPipelineRunning(false);
    }
  };

  const streamAutomatedPipeline = (pipelineId: string) => {
    const eventSource = new EventSource(`${API_BASE_URL}/api/workflow/automated-stream/${pipelineId}`);
    
    eventSource.onopen = () => {
      console.log('SSE connection opened');
    };
    
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('SSE message received:', data);
        setPipelineStatus(data);
        
        if (data.event === 'pipeline_complete' || data.status === 'completed') {
          setIsPipelineRunning(false);
          setShowAppPreview(true);
          setTimeout(() => eventSource.close(), 1000);
        }
      } catch (error) {
        console.error('Error parsing SSE data:', error);
      }
    };
    
    eventSource.addEventListener('pipeline_update', (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Pipeline update:', data);
        setPipelineStatus(data);
      } catch (error) {
        console.error('Error parsing pipeline_update:', error);
      }
    });
    
    eventSource.addEventListener('step_complete', (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Step complete:', data);
        setPipelineStatus(data);
      } catch (error) {
        console.error('Error parsing step_complete:', error);
      }
    });
    
    eventSource.addEventListener('pipeline_complete', (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Pipeline complete:', data);
        setPipelineStatus(data);
        setIsPipelineRunning(false);
        setShowAppPreview(true);
        setTimeout(() => eventSource.close(), 1000);
      } catch (error) {
        console.error('Error parsing pipeline_complete:', error);
      }
    });
    
    eventSource.onerror = (error) => {
      console.error('SSE connection error:', error);
      // Don't immediately close on error - the connection might recover
      if (eventSource.readyState === EventSource.CLOSED) {
        console.log('SSE connection closed');
        setIsPipelineRunning(false);
      }
    };

    // Clean up function
    return () => {
      if (eventSource.readyState !== EventSource.CLOSED) {
        eventSource.close();
      }
    };
  };

  const startWorkflow = async () => {
    try {
      setIsRunning(true);
      setWorkflowStatus(null);
      
      const response = await fetch(`${API_BASE_URL}/api/workflow/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          project_description: projectDescription,
          programming_language: programmingLanguage,
          workflow_type: workflowType,
          code_sample: codeSample,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setWorkflowId(result.workflow_id);
    } catch (error) {
      console.error('Error starting workflow:', error);
      setIsRunning(false);
    }
  };

  const pollWorkflowStatus = useCallback(async () => {
    if (!workflowId) return;

    try {
      const response = await fetch(`${API_BASE_URL}/api/workflow/status/${workflowId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const status: WorkflowStatus = await response.json();
      setWorkflowStatus(status);

      if (status.status === 'completed' || status.status === 'failed') {
        setIsRunning(false);
      }
    } catch (error) {
      console.error('Error polling workflow status:', error);
      setIsRunning(false);
    }
  }, [workflowId]);

  useEffect(() => {
    if (isRunning && workflowId) {
      const interval = setInterval(pollWorkflowStatus, 1000);
      return () => clearInterval(interval);
    }
  }, [isRunning, workflowId, pollWorkflowStatus]);

  const formatDuration = (startTime?: number, endTime?: number) => {
    if (!startTime) return '--';
    const end = endTime || Date.now() / 1000;
    const duration = end - startTime;
    return `${Math.round(duration)}s`;
  };

  const renderStepIcon = (step: WorkflowStep) => {
    const agentKey = step.agent_name.replace(/\s+/g, '') as AgentType;
    const icon = (agentIcons as any)[agentKey] || '🔄';
    const color = agentColors[agentKey] || '#757575';
    
    return (
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        width: 32,
        height: 32,
        borderRadius: '50%',
        backgroundColor: color,
        color: 'white'
      }}>
        {icon}
      </Box>
    );
  };



  const renderAutomatedPipelineTab = () => (
    <Container maxWidth="lg" sx={{ py: 3 }}>
      <Grid container spacing={3}>
        {/* Input Form */}
        <Grid item xs={12} md={4}>
          <StyledCard>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <RocketLaunch /> Automated Pipeline
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Enter your idea and watch AI create a complete working application!
              </Typography>
              
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Your App Idea"
                value={userIdea}
                onChange={(e) => setUserIdea(e.target.value)}
                sx={{ mb: 2 }}
                placeholder="Describe what kind of app you want to build..."
              />
              
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>Framework</InputLabel>
                <Select
                  value={targetFramework}
                  onChange={(e) => setTargetFramework(e.target.value)}
                  label="Framework"
                >
                  <MenuItem value="flask">Flask (Python)</MenuItem>
                  <MenuItem value="fastapi">FastAPI (Python)</MenuItem>
                  <MenuItem value="react">React (JavaScript)</MenuItem>
                  <MenuItem value="express">Express (Node.js)</MenuItem>
                </Select>
              </FormControl>
              
              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={startAutomatedPipeline}
                disabled={isPipelineRunning}
                startIcon={isPipelineRunning ? <CircularProgress size={20} /> : <PlayArrow />}
                sx={{ mb: 2 }}
              >
                {isPipelineRunning ? 'Building Your App...' : 'Start Automated Pipeline'}
              </Button>
              
              {isPipelineRunning && (
                <Alert severity="info" sx={{ mt: 2 }}>
                  🤖 AI is working on your app! This takes 2-3 minutes.
                </Alert>
              )}
            </CardContent>
          </StyledCard>
        </Grid>
        
        {/* Pipeline Progress */}
        <Grid item xs={12} md={8}>
      <StyledCard>
        <CardContent>
              <Typography variant="h6" gutterBottom>
                Pipeline Progress
              </Typography>
              
              {pipelineStatus && (
                <>
                  <Box sx={{ mb: 2 }}>
                    <LinearProgress 
                      variant="determinate" 
                      value={pipelineStatus.progress} 
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                      {pipelineStatus.progress}% Complete
            </Typography>
          </Box>

                  <Alert 
                    severity={pipelineStatus.status === 'completed' ? 'success' : 'info'}
                    sx={{ mb: 2 }}
                  >
                    {pipelineStatus.message}
                  </Alert>
                  
                  {/* Step Details */}
                  {pipelineStatus.result && (
                    <Paper sx={{ p: 2, mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                        Step: {pipelineSteps[pipelineStatus.step as keyof typeof pipelineSteps]?.name}
                  </Typography>
                      <pre style={{ fontSize: '12px', whiteSpace: 'pre-wrap', maxHeight: '200px', overflow: 'auto' }}>
                        {JSON.stringify(pipelineStatus.result, null, 2)}
                      </pre>
                </Paper>
                  )}
                </>
              )}
              
              {!pipelineStatus && !isPipelineRunning && (
                <Alert severity="info">
                  Enter your app idea above and click "Start Automated Pipeline" to begin!
                </Alert>
              )}
            </CardContent>
          </StyledCard>
              </Grid>
        
        {/* App Preview */}
        {showAppPreview && pipelineStatus?.app_preview && (
          <Grid item xs={12}>
            <StyledCard>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <WebAsset /> Your Generated App
                  </Typography>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  🎉 Your app is ready! Here's a preview of what was generated:
                  </Typography>
                
                {pipelineStatus.app_url && (
                  <Alert severity="success" sx={{ mb: 2 }}>
                    App URL: <strong>{pipelineStatus.app_url}</strong>
                  </Alert>
                )}
                
                <AppPreviewContainer>
                  <div
                    dangerouslySetInnerHTML={{ __html: pipelineStatus.app_preview }}
                    style={{ width: '100%', height: '100%' }}
                  />
                </AppPreviewContainer>
                
                {pipelineStatus.result?.features && (
                  <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                      Generated Features:
                  </Typography>
                  <List dense>
                      {pipelineStatus.result.features.map((feature: string, index: number) => (
                        <ListItem key={index} sx={{ py: 0 }}>
                          <ListItemText primary={feature} />
                      </ListItem>
                    ))}
                  </List>
                  </Box>
                )}
              </CardContent>
            </StyledCard>
            </Grid>
          )}
              </Grid>
    </Container>
  );

  const renderWorkflowTab = () => (
    <Container maxWidth="lg" sx={{ py: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
      <StyledCard>
        <CardContent>
              <Typography variant="h6" gutterBottom>
                Workflow Configuration
          </Typography>
          
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Project Description"
                value={projectDescription}
                onChange={(e) => setProjectDescription(e.target.value)}
                sx={{ mb: 2 }}
              />
            
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Programming Language</InputLabel>
                <Select
                  value={programmingLanguage}
                  onChange={(e) => setProgrammingLanguage(e.target.value)}
                  label="Programming Language"
                >
                  <MenuItem value="Python">Python</MenuItem>
                  <MenuItem value="JavaScript">JavaScript</MenuItem>
                  <MenuItem value="TypeScript">TypeScript</MenuItem>
                  <MenuItem value="Java">Java</MenuItem>
                  <MenuItem value="Go">Go</MenuItem>
                </Select>
              </FormControl>
            
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Workflow Type</InputLabel>
                <Select
                  value={workflowType}
                  onChange={(e) => setWorkflowType(e.target.value)}
                  label="Workflow Type"
                >
                  <MenuItem value="full_development">Full Development</MenuItem>
                  <MenuItem value="code_improvement">Code Improvement</MenuItem>
                  <MenuItem value="security_focused">Security Focused</MenuItem>
                  <MenuItem value="documentation_focused">Documentation</MenuItem>
                </Select>
              </FormControl>
            
              <TextField
                fullWidth
                multiline
                rows={6}
                label="Code Sample (Optional)"
                value={codeSample}
                onChange={(e) => setCodeSample(e.target.value)}
                sx={{ mb: 2, fontFamily: 'monospace' }}
              />

            <Button
                fullWidth
              variant="contained"
              size="large"
              onClick={startWorkflow}
              disabled={isRunning}
                startIcon={isRunning ? <CircularProgress size={20} /> : <PlayArrow />}
            >
                {isRunning ? 'Running Workflow...' : 'Start Workflow'}
            </Button>
        </CardContent>
      </StyledCard>
        </Grid>

        <Grid item xs={12} md={8}>
        <StyledCard>
          <CardContent>
              <Typography variant="h6" gutterBottom>
                Workflow Execution
              </Typography>

              {workflowStatus && (
                <>
                  <Box sx={{ mb: 3 }}>
            <LinearProgress
              variant="determinate"
              value={(workflowStatus.current_step / workflowStatus.total_steps) * 100}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                      Step {workflowStatus.current_step} of {workflowStatus.total_steps}
            </Typography>
                  </Box>

            <Stepper orientation="vertical">
              {workflowStatus.steps.map((step, index) => (
                <Step key={step.step_id} active={step.status === 'running'} completed={step.status === 'completed'}>
                  <StepLabel
                    error={step.status === 'failed'}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {renderStepIcon(step)}
                      <Typography variant="body2">
                        {step.agent_name}
                      </Typography>
                      {step.status === 'completed' && (
                        <Chip 
                          label={`${formatDuration(step.start_time, step.end_time)}`} 
                          size="small" 
                          color="success"
                        />
                      )}
                    </Box>
                  </StepLabel>
                  {step.status === 'completed' && step.result && (
                    <StepContent>
                      <Paper sx={{ p: 2, mt: 1, bgcolor: 'grey.50' }}>
                        <Typography variant="caption" color="text.secondary" gutterBottom>
                          Step Result:
                        </Typography>
                        <pre style={{ 
                          fontSize: '11px', 
                          whiteSpace: 'pre-wrap',
                          margin: 0,
                          fontFamily: 'monospace',
                          maxHeight: '150px',
                          overflow: 'auto'
                        }}>
                          {typeof step.result === 'string' 
                            ? step.result 
                            : JSON.stringify(step.result, null, 2)
                          }
                        </pre>
                      </Paper>
                    </StepContent>
                  )}
                </Step>
              ))}
            </Stepper>
                </>
              )}
              
              {workflowStatus && workflowStatus.status === 'completed' && (
                <Paper sx={{ p: 3, mt: 3, bgcolor: 'success.light', color: 'success.contrastText' }}>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CheckCircle />
                    Workflow Completed Successfully!
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    All {workflowStatus.total_steps} agents have completed their tasks in {formatDuration(workflowStatus.start_time, workflowStatus.end_time)}.
                  </Typography>
                  {Object.keys(workflowStatus.results || {}).length > 0 && (
                    <Accordion sx={{ mt: 2 }}>
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Typography variant="subtitle2">
                          View Final Results
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Paper sx={{ p: 2, bgcolor: 'grey.50', maxHeight: '300px', overflow: 'auto' }}>
                          <pre style={{ 
                            fontSize: '12px', 
                            whiteSpace: 'pre-wrap',
                            margin: 0,
                            fontFamily: 'monospace'
                          }}>
                            {JSON.stringify(workflowStatus.results, null, 2)}
                          </pre>
                        </Paper>
                      </AccordionDetails>
                    </Accordion>
                  )}
                </Paper>
              )}
              
              {!workflowStatus && !isRunning && (
                <Alert severity="info">
                  Configure your workflow settings and click "Start Workflow" to begin the multi-agent process.
                </Alert>
              )}
          </CardContent>
        </StyledCard>
              </Grid>
            </Grid>
    </Container>
  );

  return (
    <Box sx={{ width: '100%' }}>
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={selectedTab}
          onChange={(_, newValue) => setSelectedTab(newValue)}
          variant="fullWidth"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab
            label={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <RocketLaunch />
                Automated Pipeline
              </Box>
            }
          />
          <Tab
            label={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Speed />
                Manual Workflow
              </Box>
            }
          />
        </Tabs>
      </Paper>
      
      {selectedTab === 0 && renderAutomatedPipelineTab()}
      {selectedTab === 1 && renderWorkflowTab()}
    </Box>
  );
};

export default LiveWorkflowDemo;