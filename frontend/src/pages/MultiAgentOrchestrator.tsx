import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  TextField,
  Typography,
  Alert,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Chip,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip,
  Stack,
  FormControlLabel,
  Switch,
} from '@mui/material';
import {
  PlayArrow,
  CheckCircle,
  Error as ErrorIcon,
  ExpandMore,
  AutoAwesome,
  Speed,
  Security,
  Code,
  Description,
  Science,
  LightbulbOutlined,
  Stop,
  Psychology,
  BugReport,
  RateReview,
  Pending,
  Visibility,
  Download,
  Warning,
  Refresh,
  Delete,
} from '@mui/icons-material';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import CodePreview from '../components/CodePreview';

const API_BASE_URL = 'http://localhost:8000';

// Simple debounce implementation
function debounce<T extends (...args: any[]) => any>(func: T, wait: number): T {
  let timeout: NodeJS.Timeout;
  return ((...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  }) as T;
}

// Custom TabPanel component for Material-UI
interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

interface WorkflowResult {
  steps: Record<string, any>;
  timeline: Array<{
    step: string;
    duration: number;
    timestamp: number;
    success: boolean;
  }>;
  success: boolean;
  error_message?: string;
  total_time: number;
  summary: {
    completed_steps: number;
    total_steps: number;
    success_rate: number;
    fastest_step: string;
    slowest_step: string;
  };
}

interface DemoScenario {
  id: string;
  title: string;
  description: string;
  expected_duration: string;
  features: string[];
}

interface LiveMetrics {
  live_stats: {
    agents_active: number;
    workflows_completed: number;
    lines_of_code_generated: number;
    security_vulnerabilities_prevented: number;
    tests_generated: number;
    documentation_pages_created: number;
    developer_time_saved_hours: number;
  };
  real_time_activity: string[];
  performance_metrics: {
    average_response_time: string;
    success_rate: string;
    agent_utilization: string;
    queue_length: number;
  };
  total_agents: number;
  active_workflows: number;
  completed_tasks: number;
  avg_response_time: number;
  uptime_hours: number;
}

interface WorkflowStep {
  step_id: string;
  agent_name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  start_time?: number;
  end_time?: number;
  progress?: number;
}

interface WorkflowStatus {
  workflow_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  current_step: number;
  total_steps: number;
  steps: WorkflowStep[];
  results: Record<string, any>;
  start_time?: number;
  end_time?: number;
  error?: string;
  progress: number;
}

interface RealTimeUpdate {
  type: 'workflow_status' | 'step_update' | 'step_complete' | 'workflow_complete' | 'error';
  workflow_id: string;
  data: any;
  timestamp: string;
  message: string;
  event_type?: string;
  step_name?: string;
  step_result?: any;
  progress?: number;
}

const workflowSteps = [
  { key: 'ideation', label: 'Ideation & Planning', icon: <LightbulbOutlined />, color: '#FF6B6B' },
  { key: 'code_generation', label: 'Code Generation', icon: <Code />, color: '#4ECDC4' },
  { key: 'security_analysis', label: 'Security Analysis', icon: <Security />, color: '#DDA0DD' },
  { key: 'test_generation', label: 'Test Generation', icon: <Science />, color: '#96CEB4' },
  { key: 'documentation', label: 'Documentation', icon: <Description />, color: '#45B7D1' },
  { key: 'code_review', label: 'Code Review', icon: <CheckCircle />, color: '#FFEAA7' },
];

const workflowTypes = [
  { value: 'full_development', label: 'Full Development Cycle' },
  { value: 'code_improvement', label: 'Code Improvement' },
  { value: 'security_focused', label: 'Security Analysis' },
  { value: 'documentation_focused', label: 'Documentation Focus' }
];

const languages = [
  'none', // For novice users who don't know programming languages
  'python', 
  'javascript', 
  'typescript', 
  'java', 
  'csharp', 
  'cpp', 
  'go', 
  'rust',
  'php',
  'ruby',
  'swift',
  'kotlin'
];

const MultiAgentOrchestrator = () => {
  const [description, setDescription] = useState('');
  const [language, setLanguage] = useState('none');
  const [workflowType, setWorkflowType] = useState('full_development');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<WorkflowResult | null>(null);
  const [activeStep, setActiveStep] = useState(0);
  const [scenarios, setScenarios] = useState<DemoScenario[]>([]);
  const [liveMetrics, setLiveMetrics] = useState<LiveMetrics | null>(null);
  const [currentActivity, setCurrentActivity] = useState<string[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [workflowStatus, setWorkflowStatus] = useState<WorkflowStatus | null>(null);
  const [steps, setSteps] = useState<WorkflowStep[]>([]);
  const [eventSource, setEventSource] = useState<EventSource | null>(null);
  const [workflowProgress, setWorkflowProgress] = useState(0);
  const [currentStepProgress, setCurrentStepProgress] = useState(0);
  const [realTimeUpdates, setRealTimeUpdates] = useState<RealTimeUpdate[]>([]);
  
  // Enhanced output rendering state
  const [outputTab, setOutputTab] = useState(0);
  const [generatedCode, setGeneratedCode] = useState<Record<string, string>>({});
  const [documentation, setDocumentation] = useState<string>('');
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [analyticsData, setAnalyticsData] = useState<Record<string, any>>({});

  // New state for workflow control and self-improvement
  const [canStop, setCanStop] = useState(false);
  const [isTerminating, setIsTerminating] = useState(false);
  const [autoCorrect, setAutoCorrect] = useState(true);
  const [maxRetries, setMaxRetries] = useState(3);
  const [currentRetry, setCurrentRetry] = useState(0);
  const [completedResults, setCompletedResults] = useState<Record<string, any>>({});
  const [showResultsDialog, setShowResultsDialog] = useState(false);
  const [selectedResult, setSelectedResult] = useState<any>(null);
  const [workflowId, setWorkflowId] = useState<string | null>(null);

  // Debug functionality state
  const [debugMode, setDebugMode] = useState(false);
  const [rawJsonOutputs, setRawJsonOutputs] = useState<Record<string, any>>({});
  const [aiProviderResponses, setAiProviderResponses] = useState<Array<{
    id: string;
    timestamp: string;
    provider: string;
    model: string;
    prompt: string;
    response: any;
    success: boolean;
    error?: string;
  }>>([]);
  const [showDebugDialog, setShowDebugDialog] = useState(false);
  const [selectedDebugResponse, setSelectedDebugResponse] = useState<any>(null);

  // Debounced update handler to prevent performance violations
  const debouncedUpdateHandler = useMemo(
    () => debounce((update: any) => {
      handleRealTimeUpdateInternal(update);
    }, 50), // 50ms debounce to prevent overwhelming the UI
    []
  );

  // Load demo scenarios and live metrics on component mount
  useEffect(() => {
    loadDemoScenarios();
    loadLiveMetrics();
  }, []); // Only run once on mount, no dependencies

  // Set up activity simulation only after metrics are loaded
  useEffect(() => {
    if (!liveMetrics) return;
    
    // Set initial activity
    setCurrentActivity(liveMetrics.real_time_activity.slice(0, 5));
    
    // Optional: Very slow updates (30 seconds) - can be removed entirely
    const activityInterval = setInterval(() => {
      const activities = liveMetrics.real_time_activity;
      const randomActivity = activities[Math.floor(Math.random() * activities.length)];
      setCurrentActivity(prev => [randomActivity, ...prev.slice(0, 4)]);
    }, 30000); // 30 seconds

    return () => clearInterval(activityInterval);
  }, [liveMetrics]);

  const loadDemoScenarios = async () => {
    try {
              const response = await axios.get('http://localhost:8000/api/workflow/demo/scenarios');
      setScenarios(response.data.scenarios);
    } catch (err) {
      console.error('Failed to load demo scenarios:', err);
      // Set mock data for demo purposes
      setScenarios([
        {
          id: '1',
          title: '🎯 Task Management App',
          description: 'Build a complete task management application with user authentication, CRUD operations, and real-time updates',
          expected_duration: '3 minutes',
          features: ['Authentication', 'CRUD Operations', 'Real-time Updates']
        },
        {
          id: '2',
          title: '🛒 E-commerce Platform',
          description: 'Create a full-featured e-commerce platform with product catalog, shopping cart, and payment integration',
          expected_duration: '4 minutes',
          features: ['Product Catalog', 'Shopping Cart', 'Payment Integration']
        },
        {
          id: '3',
          title: '💬 Real-time Chat Application',
          description: 'Develop a real-time chat application with WebSocket support, user presence, and message history',
          expected_duration: '3.5 minutes',
          features: ['WebSocket Support', 'User Presence', 'Message History']
        },
        {
          id: '4',
          title: '🔧 REST API Service',
          description: 'Build a robust REST API service with authentication, rate limiting, and comprehensive documentation',
          expected_duration: '2.5 minutes',
          features: ['Authentication', 'Rate Limiting', 'API Documentation']
        }
      ]);
    }
  };

  const loadLiveMetrics = async () => {
    try {
              const response = await axios.get('http://localhost:8000/api/workflow/demo/live-metrics');
      setLiveMetrics(response.data);
    } catch (err) {
      console.error('Failed to load live metrics:', err);
      // Set mock data for demo purposes
      setLiveMetrics({
        live_stats: {
          agents_active: 6,
          workflows_completed: 193,
          lines_of_code_generated: 68651,
          security_vulnerabilities_prevented: 346,
          tests_generated: 1247,
          documentation_pages_created: 89,
          developer_time_saved_hours: 1027
        },
        real_time_activity: [
          '✅ TestGenerator: Created 47 unit tests with 96% coverage',
          '🔒 SecurityAnalyzer: Detected and fixed SQL injection vulnerability',
          '📝 DocGenerator: Generated user guide for e-commerce module - Quality Score: A+',
          '⚡ CodeOptimizer: Improved database query performance by 340%',
          '🤖 IdeationAgent: Proposed microservices architecture for scalability'
        ],
        performance_metrics: {
          average_response_time: '1.2s',
          success_rate: '99.7%',
          agent_utilization: '87%',
          queue_length: 3
        },
        total_agents: 6,
        active_workflows: 12,
        completed_tasks: 193,
        avg_response_time: 1.2,
        uptime_hours: 1027
      });
    }
  };

  const handleScenarioSelect = (scenario: DemoScenario) => {
    setDescription(scenario.description);
    setWorkflowType('full_development');
  };

  const handleRealTimeUpdateInternal = useCallback((update: any) => {
    console.log('Real-time update:', update);
    
    setLoading(false);
    
    // Debug Mode: Capture all raw JSON outputs
    if (debugMode && update) {
      const debugEntry = {
        id: `debug_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp: new Date().toISOString(),
        type: update.type || update.event || 'unknown',
        rawData: JSON.parse(JSON.stringify(update)), // Deep clone
        workflow_id: update.workflow_id || workflowId || 'unknown'
      };
      
      setRawJsonOutputs(prev => ({
        ...prev,
        [debugEntry.id]: debugEntry
      }));

      // If this update contains AI provider response data, capture it
      if (update.ai_response || (update.data && update.data.ai_response)) {
        const aiResponse = update.ai_response || update.data.ai_response;
        const aiDebugEntry = {
          id: debugEntry.id,
          timestamp: debugEntry.timestamp,
          provider: aiResponse.provider || 'unknown',
          model: aiResponse.model || 'unknown',
          prompt: aiResponse.prompt || 'N/A',
          response: aiResponse.response || aiResponse,
          success: aiResponse.success !== false,
          error: aiResponse.error || null
        };
        
        setAiProviderResponses(prev => [aiDebugEntry, ...prev.slice(0, 49)]); // Keep last 50
      }
    }
    
    // Ensure update has proper structure and prevent undefined displays
    if (!update || typeof update !== 'object') {
      console.warn('Invalid update received:', update);
      return;
    }
    
    switch (update.type || update.event) {
      case 'workflow_status':
      case 'workflow_update':
        const status: WorkflowStatus = update.data || update;
        setWorkflowStatus(status);
        setSteps(status.steps?.filter(step => step !== null) || []);
        setActiveStep(status.current_step || 0);
        setWorkflowProgress(status.progress || 0);
        
        // Fix undefined display by ensuring proper message formatting
        const activityMessage = update.message || 
          (status.status ? `🔄 Workflow: ${status.status} - Step ${status.current_step}/${status.total_steps}` : 'Workflow status update');
        
        const activityUpdate: RealTimeUpdate = {
          type: 'workflow_status',
          workflow_id: status.workflow_id || workflowId || 'workflow',
          data: status,
          timestamp: new Date().toISOString(),
          message: activityMessage
        };
        setRealTimeUpdates(prev => [activityUpdate, ...prev.slice(0, 4)]);
        break;
        
      case 'step_update':
        const stepUpdate = update.data || update;
        setCurrentStepProgress(stepUpdate.progress || 0);
        
        const stepId = stepUpdate.step || stepUpdate.step_id || `step_${Date.now()}`;
        const agentName = stepUpdate.step || stepUpdate.agent_name || 'AI Agent';
        
        const newStep: WorkflowStep = {
          step_id: stepId,
          agent_name: agentName,
          status: 'running',
          progress: stepUpdate.progress || 0,
          start_time: Date.now()
        };
        
        setSteps(prev => {
          const existing = prev.find(s => s && s.step_id === stepId);
          if (existing) {
            return prev.map(step => 
              (step && step.step_id === stepId) ? { ...step, ...newStep } : step
            ).filter(step => step !== null);
          } else {
            return [...prev, newStep];
          }
        });
        
        const stepMessage = update.message || `⚡ ${agentName}: ${stepUpdate.progress || 0}%`;
        const stepUpdateMsg: RealTimeUpdate = {
          type: 'step_update',
          workflow_id: update.workflow_id || workflowId || 'workflow',
          data: stepUpdate,
          timestamp: new Date().toISOString(),
          message: stepMessage
        };
        setRealTimeUpdates(prev => [stepUpdateMsg, ...prev.slice(0, 4)]);
        break;
        
      case 'step_complete':
        const completedStep = update.data || update;
        const completeStepId = completedStep.step || completedStep.step_id || `completed_${Date.now()}`;
        const completedAgentName = completedStep.step || completedStep.agent_name || 'AI Agent';
        
        // Store completed result for immediate access
        if (completedStep.result) {
          const resultData = {
            agent_name: completedAgentName,
            result: completedStep.result,
            timestamp: new Date().toISOString(),
            duration: completedStep.duration || 0
          };
          
          setCompletedResults(prev => ({
            ...prev,
            [completeStepId]: resultData
          }));

          // Extract and process different types of outputs
          const result = completedStep.result;
          if (result) {
            // Extract generated code
            if (result.generated_code || result.full_code || result.files || result.generated_files) {
              const code = result.full_code || result.generated_code;
              const files = result.files || result.generated_files || {};
              if (code) {
                files['main.py'] = code;
              }
              if (Object.keys(files).length > 0) {
                setGeneratedCode(prev => ({ ...prev, ...files }));
              }
            }
            
            // Extract documentation
            if (result.documentation) {
              setDocumentation(result.documentation);
            }
            
            // Extract preview URL or deployment info
            if (result.preview_url || result.deployment_url) {
              setPreviewUrl(result.preview_url || result.deployment_url);
            }
            
            // Extract analytics/metrics data
            if (result.metrics || result.analysis) {
              setAnalyticsData(prev => ({
                ...prev,
                [completeStepId]: result.metrics || result.analysis
              }));
            }
          }
        }
        
        setSteps(prev => prev.map(step => 
          (step && step.step_id === completeStepId) ? { 
            ...step, 
            status: 'completed' as const, 
            end_time: Date.now(),
            result: completedStep.result || 'Completed successfully',
            progress: 100,
          } : step
        ).filter(step => step !== null));
        
        const completeMessage = update.message || `✅ ${completedAgentName}: Completed successfully`;
        const completeUpdate: RealTimeUpdate = {
          type: 'step_complete',
          workflow_id: update.workflow_id || workflowId || 'workflow',
          data: completedStep,
          timestamp: new Date().toISOString(),
          message: completeMessage
        };
        setRealTimeUpdates(prev => [completeUpdate, ...prev.slice(0, 4)]);
        setCurrentStepProgress(0);
        break;
        
      case 'workflow_complete':
        const finalData = update.data || update;
        setIsRunning(false);
        setCanStop(false);
        setWorkflowProgress(100);
        
        // Extract all generated files from the final workflow results
        if (finalData.results) {
          const allGeneratedFiles: Record<string, string> = {};
          
          // Iterate through all step results to collect generated files
          Object.values(finalData.results).forEach((stepResult: any) => {
            if (stepResult && typeof stepResult === 'object') {
              // Extract files from various possible locations
              const files = stepResult.files || stepResult.generated_files || {};
              const code = stepResult.full_code || stepResult.generated_code;
              
              // Add individual code to files if available
              if (code && typeof code === 'string') {
                const filename = stepResult.filename || 'main.py';
                allGeneratedFiles[filename] = code;
              }
              
              // Add all files from this step
              if (files && typeof files === 'object') {
                Object.assign(allGeneratedFiles, files);
              }
            }
          });
          
          // Also check if there are generated_files at the top level
          if (finalData.generated_files) {
            Object.assign(allGeneratedFiles, finalData.generated_files);
          }
          
          // Update the generated code state with all collected files
          if (Object.keys(allGeneratedFiles).length > 0) {
            setGeneratedCode(prev => ({ ...prev, ...allGeneratedFiles }));
          }
        }
        
        const workflowResult: WorkflowResult = {
          steps: finalData.results || {},
          timeline: [],
          success: true,
          total_time: finalData.total_time || 0,
          summary: {
            completed_steps: steps.filter(s => s && s.status === 'completed').length,
            total_steps: steps.length,
            success_rate: 100,
            fastest_step: 'ideation',
            slowest_step: 'documentation'
          }
        };
        setResult(workflowResult);
        
        const finalMessage = update.message || '🎉 Workflow completed successfully!';
        const finalUpdate: RealTimeUpdate = {
          type: 'workflow_complete',
          workflow_id: update.workflow_id || workflowId || 'workflow',
          data: finalData,
          timestamp: new Date().toISOString(),
          message: finalMessage
        };
        setRealTimeUpdates(prev => [finalUpdate, ...prev.slice(0, 4)]);
        
        if (eventSource) {
          eventSource.close();
          setEventSource(null);
        }
        break;
        
      case 'error':
        const errorMessage = update.message || update.data?.message || 'Workflow execution failed';
        
        // Auto-correction mechanism
        if (autoCorrect && currentRetry < maxRetries) {
          setCurrentRetry(prev => prev + 1);
          console.log(`Auto-retry attempt ${currentRetry + 1}/${maxRetries}`);
          
          const retryUpdate: RealTimeUpdate = {
            type: 'error',
            workflow_id: update.workflow_id || workflowId || 'workflow',
            data: update,
            timestamp: new Date().toISOString(),
            message: `⚠️ Error occurred, auto-retrying (${currentRetry + 1}/${maxRetries}): ${errorMessage}`
          };
          setRealTimeUpdates(prev => [retryUpdate, ...prev.slice(0, 4)]);
          
          // Retry after a delay
          setTimeout(() => {
            executeWorkflow(new Event('submit') as any);
          }, 2000);
        } else {
          setError(errorMessage);
          setIsRunning(false);
          setCanStop(false);
          setLoading(false);
          
          if (eventSource) {
            eventSource.close();
            setEventSource(null);
          }
        }
        break;
        
      default:
        if (update.message) {
          const genericUpdate: RealTimeUpdate = {
            type: 'workflow_status',
            workflow_id: update.workflow_id || workflowId || 'workflow',
            data: update,
            timestamp: new Date().toISOString(),
            message: update.message
          };
          setRealTimeUpdates(prev => [genericUpdate, ...prev.slice(0, 4)]);
        }
        break;
    }
  }, [eventSource, steps, currentRetry, maxRetries, autoCorrect, workflowId]);

  const executeWorkflow = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (isRunning) {
      return;
    }

    // Reset retry counter for new workflow
    setCurrentRetry(0);
    setCompletedResults({});
    setError('');
    setResult(null);
    setSteps([]);
    setGeneratedCode({});
    setDocumentation('');
    setPreviewUrl('');
    setAnalyticsData({});
    setRealTimeUpdates([]);
    setWorkflowProgress(0);
    setCurrentStepProgress(0);
    setActiveStep(0);
    
    try {
      setLoading(true);
      setIsRunning(true);
      setCanStop(true);

      // Handle 'none' language option for novice users
      const effectiveLanguage = language === 'none' ? 'python' : language;

      const response = await fetch(`${API_BASE_URL}/api/workflow/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          project_description: description,
          programming_language: effectiveLanguage,
          workflow_type: workflowType,
          code_sample: '', // Optional
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Workflow started:', data);
      
      setWorkflowId(data.workflow_id);

      // Start SSE connection for real-time updates
      const eventSourceUrl = `${API_BASE_URL}/api/workflow/stream/${data.workflow_id}`;
      const newEventSource = new EventSource(eventSourceUrl);
      setEventSource(newEventSource);

      newEventSource.onopen = () => {
        console.log('SSE connection opened');
      };

      newEventSource.onmessage = (event) => {
        try {
          const update = JSON.parse(event.data);
          debouncedUpdateHandler(update);
        } catch (err) {
          console.error('Failed to parse SSE message:', err);
        }
      };

      newEventSource.onerror = (error) => {
        console.error('SSE connection error:', error);
        
        // Only attempt recovery if still running and not terminating
        if (newEventSource.readyState === EventSource.OPEN && !isTerminating) {
          console.log('SSE connection error, but still open - attempting to recover');
          return;
        }
        
        if (newEventSource.readyState === EventSource.CLOSED) {
          console.log('SSE connection closed');
          setEventSource(null);
          
          if (isRunning && !isTerminating) {
            setError('Connection lost. Please try again.');
            setIsRunning(false);
            setCanStop(false);
          }
        }
      };
      
    } catch (err: any) {
      console.error('Workflow execution failed:', err);
      setError(err.response?.data?.detail || 'Failed to execute workflow');
      setLoading(false);
      setIsRunning(false);
      setCanStop(false);
    }
  };

  const stopWorkflow = async () => {
    setIsTerminating(true);
    setCanStop(false);
    
    try {
      if (workflowId) {
        await fetch(`${API_BASE_URL}/api/workflow/stop/${workflowId}`, {
          method: 'POST'
        });
      }
    } catch (err) {
      console.error('Failed to stop workflow:', err);
    }
    
    setIsRunning(false);
    setError('Workflow stopped by user');
    
    if (eventSource) {
      eventSource.close();
      setEventSource(null);
    }
    
    const stopUpdate: RealTimeUpdate = {
      type: 'workflow_status',
      workflow_id: workflowId || 'workflow',
      data: {},
      timestamp: new Date().toISOString(),
      message: '🛑 Workflow stopped by user'
    };
    setRealTimeUpdates(prev => [stopUpdate, ...prev.slice(0, 4)]);
    
    setIsTerminating(false);
  };

  const viewCompletedResult = (stepId: string) => {
    const result = completedResults[stepId];
    if (result) {
      setSelectedResult(result);
      setShowResultsDialog(true);
    }
  };

  const getStepIcon = (status: string, agent: string) => {
    const iconProps = { fontSize: 'small' as const };
    
    // Map agent names to icons
    const agentIconMap: Record<string, JSX.Element> = {
      'IdeationAgent': <Psychology {...iconProps} />,
      'CodeOptimizer': <Code {...iconProps} />,
      'SecurityAnalyzer': <Security {...iconProps} />,
      'TestGenerator': <BugReport {...iconProps} />,
      'DocGenerator': <Description {...iconProps} />,
      'CodeReviewer': <RateReview {...iconProps} />,
      // Legacy mappings
      'ideation': <Psychology {...iconProps} />,
      'code_generation': <Code {...iconProps} />,
      'security_analysis': <Security {...iconProps} />,
      'test_generation': <BugReport {...iconProps} />,
      'documentation': <Description {...iconProps} />,
      'code_review': <RateReview {...iconProps} />,
    };
    
    return agentIconMap[agent] || <Code {...iconProps} />;
  };

  const formatDuration = (start?: number, end?: number) => {
    if (!start || !end) return '0.0s';
    const duration = (end - start) / 1000;
    return `${duration.toFixed(1)}s`;
  };

  const getStepStatus = (step: WorkflowStep | null | undefined) => {
    if (!step || !step.status) {
      return { color: '#9e9e9e', icon: <Pending /> };
    }
    switch (step.status) {
      case 'completed': return { color: '#4caf50', icon: <CheckCircle /> };
      case 'running': return { color: '#ff9800', icon: <CircularProgress size={16} /> };
      case 'failed': return { color: '#f44336', icon: <ErrorIcon /> };
      default: return { color: '#9e9e9e', icon: <Pending /> };
    }
  };

  const renderRealTimeActivity = () => (
    <Card sx={{ height: '400px', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h6" gutterBottom>
          ⚡ Real-time Activity
        </Typography>
        
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {realTimeUpdates.length === 0 ? (
            <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
              No activity yet. Start a workflow to see real-time updates.
            </Typography>
          ) : (
            <List dense>
              {realTimeUpdates.map((update, index) => (
                <ListItem key={index} sx={{ py: 0.5 }}>
                  <Box sx={{ width: '100%' }}>
                    <Typography variant="body2" sx={{ fontSize: '0.9rem' }}>
                      {update.message || 'Update received'}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(update.timestamp).toLocaleTimeString()}
                    </Typography>
                  </Box>
                </ListItem>
              ))}
            </List>
          )}
        </Box>
      </CardContent>
    </Card>
  );

  const renderCompletedResults = () => (
    <Card sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          📋 Completed Results ({Object.keys(completedResults).length})
        </Typography>
        
        {Object.keys(completedResults).length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            No completed results yet.
          </Typography>
        ) : (
          <Stack spacing={1}>
            {Object.entries(completedResults).map(([stepId, result]) => (
              <Paper key={stepId} sx={{ p: 2, bgcolor: 'success.light', color: 'success.contrastText' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="subtitle2">
                      ✅ {result.agent_name}
                    </Typography>
                    <Typography variant="caption">
                      Completed in {result.duration}s at {new Date(result.timestamp).toLocaleTimeString()}
                    </Typography>
                  </Box>
                  <Button
                    size="small"
                    variant="outlined"
                    startIcon={<Visibility />}
                    onClick={() => viewCompletedResult(stepId)}
                    sx={{ color: 'inherit', borderColor: 'inherit' }}
                  >
                    View
                  </Button>
                </Box>
              </Paper>
            ))}
          </Stack>
        )}
      </CardContent>
    </Card>
  );

  const renderWorkflowControls = () => (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <FormControlLabel
            control={
              <Switch
                checked={autoCorrect}
                onChange={(e) => setAutoCorrect(e.target.checked)}
                disabled={isRunning}
              />
            }
            label="Auto-retry on errors"
          />
          <TextField
            label="Max Retries"
            type="number"
            value={maxRetries}
            onChange={(e) => setMaxRetries(Math.max(1, Math.min(5, parseInt(e.target.value) || 3)))}
            disabled={isRunning}
            size="small"
            sx={{ width: 120 }}
            inputProps={{ min: 1, max: 5 }}
          />
          {currentRetry > 0 && (
            <Chip
              icon={<Refresh />}
              label={`Retry ${currentRetry}/${maxRetries}`}
              color="warning"
              size="small"
            />
          )}
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            type="submit"
            variant="contained"
            startIcon={isRunning ? <CircularProgress size={20} /> : <PlayArrow />}
            disabled={isRunning || !description.trim()}
            sx={{ flex: 1 }}
          >
            {isRunning ? 'Running...' : 'Execute Multi-Agent Workflow'}
          </Button>
          
          {canStop && (
            <Button
              variant="outlined"
              color="error"
              startIcon={isTerminating ? <CircularProgress size={20} /> : <Stop />}
              onClick={stopWorkflow}
              disabled={isTerminating}
            >
              {isTerminating ? 'Stopping...' : 'Stop'}
            </Button>
          )}
        </Box>
      </CardContent>
    </Card>
  );

  // Results Dialog Component
  const renderResultsDialog = () => (
    <Dialog
      open={showResultsDialog}
      onClose={() => setShowResultsDialog(false)}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
        Agent Result: {selectedResult?.agent_name}
      </DialogTitle>
      <DialogContent>
        {selectedResult?.result && (
          <Box>
            {selectedResult.result.display_content && (
              <Paper sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}>
                <Typography variant="h6" gutterBottom>
                  📊 Formatted Output
                </Typography>
                <Typography component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '0.85rem' }}>
                  {selectedResult.result.display_content}
                </Typography>
              </Paper>
            )}
            
            {selectedResult.result.generated_files && (
              <Paper sx={{ p: 2, mb: 2 }}>
                <Typography variant="h6" gutterBottom>
                  📁 Generated Files
                </Typography>
                {Object.entries(selectedResult.result.generated_files).map(([filename, content]) => (
                  <Accordion key={filename}>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Typography variant="subtitle2">{filename}</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '0.8rem' }}>
                        {typeof content === 'string' ? content : JSON.stringify(content, null, 2)}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                ))}
              </Paper>
            )}
            
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                🔍 Raw Result Data
              </Typography>
              <Typography component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '0.8rem' }}>
                {JSON.stringify(selectedResult.result, null, 2)}
              </Typography>
            </Paper>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setShowResultsDialog(false)}>Close</Button>
      </DialogActions>
    </Dialog>
  );

  // Debug helper functions
  const parseOutputToContainer = (debugEntry: any) => {
    try {
      // Extract meaningful data for the frontend container
      const parsedData = {
        timestamp: debugEntry.timestamp,
        type: debugEntry.type,
        data: debugEntry.rawData,
        // Try to extract AI response details
        aiProvider: debugEntry.rawData?.ai_response?.provider || 'unknown',
        aiModel: debugEntry.rawData?.ai_response?.model || 'unknown',
        success: debugEntry.rawData?.ai_response?.success || true,
      };

      // Update the current workflow with parsed data
      if (debugEntry.rawData?.data) {
        // Process step results
        if (debugEntry.type === 'step_complete' && debugEntry.rawData.data.result) {
          const result = debugEntry.rawData.data.result;
          
          // Extract code files
          if (result.generated_files || result.files) {
            setGeneratedCode(prev => ({ 
              ...prev, 
              ...result.generated_files,
              ...result.files 
            }));
          }
          
          // Extract documentation
          if (result.documentation) {
            setDocumentation(result.documentation);
          }
        }
      }

      // Show success message
      console.log('✅ Parsed debug output to frontend container:', parsedData);
      return parsedData;
    } catch (error) {
      console.error('❌ Failed to parse debug output:', error);
      return null;
    }
  };

  const viewDebugResponse = (response: any) => {
    setSelectedDebugResponse(response);
    setShowDebugDialog(true);
  };

  const clearDebugData = () => {
    setRawJsonOutputs({});
    setAiProviderResponses([]);
  };

  // Debug Toggle Card Component
  const renderDebugToggleCard = () => (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.3 }}
    >
      <Paper sx={{ p: 3, mb: 4, bgcolor: 'rgba(255, 165, 0, 0.05)', border: '1px solid rgba(255, 165, 0, 0.2)' }}>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <BugReport color="warning" />
          Debug Mode - Raw JSON Output Viewer
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <FormControlLabel
            control={
              <Switch
                checked={debugMode}
                onChange={(e) => setDebugMode(e.target.checked)}
                color="warning"
              />
            }
            label="Enable Debug Mode"
          />
          
          <Chip 
            label={`${Object.keys(rawJsonOutputs).length} Captured Outputs`}
            color={debugMode ? "warning" : "default"}
            variant="outlined"
          />
          
          <Chip 
            label={`${aiProviderResponses.length} AI Responses`}
            color={debugMode ? "success" : "default"}
            variant="outlined"
          />
          
          <Button
            size="small"
            onClick={clearDebugData}
            disabled={Object.keys(rawJsonOutputs).length === 0}
            startIcon={<Delete />}
          >
            Clear Debug Data
          </Button>
        </Box>

        {debugMode && (
          <Box>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Debug mode captures all raw JSON outputs from AI providers and workflow events.
              Use this to verify schema definitions match Google Gemini outputs.
            </Typography>
            
            {Object.keys(rawJsonOutputs).length > 0 && (
              <Paper sx={{ p: 2, bgcolor: 'rgba(0,0,0,0.02)', mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  📋 Recent Debug Outputs:
                </Typography>
                <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
                  {Object.entries(rawJsonOutputs).slice(-10).map(([id, entry]) => (
                    <Box key={id} sx={{ mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip 
                        label={entry.type}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                      <Typography variant="caption" sx={{ flex: 1 }}>
                        {entry.timestamp}
                      </Typography>
                      <Button
                        size="small"
                        onClick={() => parseOutputToContainer(entry)}
                        startIcon={<PlayArrow />}
                      >
                        Parse to Container
                      </Button>
                      <Button
                        size="small"
                        onClick={() => {
                          setSelectedDebugResponse(entry);
                          setShowDebugDialog(true);
                        }}
                        startIcon={<Visibility />}
                      >
                        View JSON
                      </Button>
                    </Box>
                  ))}
                </Box>
              </Paper>
            )}

            {aiProviderResponses.length > 0 && (
              <Paper sx={{ p: 2, bgcolor: 'rgba(0,128,0,0.02)' }}>
                <Typography variant="subtitle2" gutterBottom>
                  🤖 AI Provider Responses:
                </Typography>
                <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
                  {aiProviderResponses.slice(0, 5).map((response) => (
                    <Box key={response.id} sx={{ mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip 
                        label={response.provider}
                        size="small"
                        color={response.success ? "success" : "error"}
                        variant="outlined"
                      />
                      <Chip 
                        label={response.model}
                        size="small"
                        color="info"
                        variant="outlined"
                      />
                      <Typography variant="caption" sx={{ flex: 1 }}>
                        {response.timestamp}
                      </Typography>
                      <Button
                        size="small"
                        onClick={() => viewDebugResponse(response)}
                        startIcon={<Code />}
                      >
                        View Response
                      </Button>
                    </Box>
                  ))}
                </Box>
              </Paper>
            )}
          </Box>
        )}
      </Paper>
    </motion.div>
  );

  // Debug Dialog Component
  const renderDebugDialog = () => (
    <Dialog
      open={showDebugDialog}
      onClose={() => setShowDebugDialog(false)}
      maxWidth="lg"
      fullWidth
    >
      <DialogTitle>
        🔍 Debug Output Viewer
        {selectedDebugResponse && (
          <Typography variant="subtitle2" color="text.secondary">
            {selectedDebugResponse.provider ? 
              `AI Provider: ${selectedDebugResponse.provider} (${selectedDebugResponse.model})` :
              `Event Type: ${selectedDebugResponse.type}`
            }
          </Typography>
        )}
      </DialogTitle>
      <DialogContent>
        {selectedDebugResponse && (
          <Box>
            <Tabs value={0}>
              <Tab label="Formatted JSON" />
              <Tab label="Raw Data" />
              <Tab label="Schema Analysis" />
            </Tabs>
            
            <Paper sx={{ p: 2, mt: 2, bgcolor: 'grey.50' }}>
              <Typography variant="h6" gutterBottom>
                📋 Formatted Output
              </Typography>
              <Typography 
                component="pre" 
                sx={{ 
                  whiteSpace: 'pre-wrap', 
                  fontFamily: 'monospace', 
                  fontSize: '0.8rem',
                  maxHeight: 400,
                  overflow: 'auto',
                  bgcolor: '#1e1e1e',
                  color: '#d4d4d4',
                  p: 2,
                  borderRadius: 1
                }}
              >
                {JSON.stringify(selectedDebugResponse.rawData || selectedDebugResponse, null, 2)}
              </Typography>
            </Paper>

            {selectedDebugResponse.provider && (
              <Paper sx={{ p: 2, mt: 2 }}>
                <Typography variant="h6" gutterBottom>
                  🔍 Schema Validation
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="subtitle2">Provider:</Typography>
                    <Chip label={selectedDebugResponse.provider} color="primary" />
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="subtitle2">Model:</Typography>
                    <Chip label={selectedDebugResponse.model} color="info" />
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="subtitle2">Success:</Typography>
                    <Chip 
                      label={selectedDebugResponse.success ? "True" : "False"} 
                      color={selectedDebugResponse.success ? "success" : "error"} 
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="subtitle2">Timestamp:</Typography>
                    <Typography variant="body2">{selectedDebugResponse.timestamp}</Typography>
                  </Grid>
                </Grid>
              </Paper>
            )}
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setShowDebugDialog(false)}>Close</Button>
        {selectedDebugResponse && (
          <Button
            onClick={() => parseOutputToContainer(selectedDebugResponse)}
            variant="contained"
            startIcon={<PlayArrow />}
          >
            Parse to Frontend
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );

  return (
    <Container maxWidth="xl">
      <Box sx={{ mt: 4, mb: 4 }}>
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <Box sx={{ textAlign: 'center', mb: 6, position: 'relative' }}>
            <Box
              sx={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '600px',
                height: '600px',
                background: 'radial-gradient(circle, rgba(0, 255, 136, 0.1) 0%, transparent 70%)',
                borderRadius: '50%',
                zIndex: -1,
                animation: 'pulse 4s ease-in-out infinite',
              }}
            />
            <Typography 
              variant="h2" 
              component="h1" 
              gutterBottom
              sx={{ 
                fontWeight: 800,
                background: 'linear-gradient(135deg, #00ff88 0%, #66ffaa 50%, #ff6b35 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 3,
                textShadow: '0 0 30px rgba(0, 255, 136, 0.3)',
                letterSpacing: '-0.02em',
                fontSize: { xs: '2.5rem', md: '3.5rem' },
              }}
            >
              🚀 Multi-Agent Orchestrator
            </Typography>
            <Typography 
              variant="h5" 
              sx={{ 
                mb: 4,
                color: 'rgba(255, 255, 255, 0.9)',
                fontWeight: 400,
                textShadow: '0 2px 10px rgba(0, 0, 0, 0.3)',
              }}
            >
              Execute complete workflows with all AI agents working together seamlessly
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
              {['⚡ Real-time', '🤖 6 AI Agents', '🔄 Auto-orchestrated', '📊 Live Analytics'].map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                >
                  <Chip
                    label={feature}
                    sx={{
                      background: 'rgba(0, 255, 136, 0.2)',
                      color: '#ffffff',
                      border: '1px solid rgba(0, 255, 136, 0.5)',
                      fontWeight: 600,
                      fontSize: '0.9rem',
                      px: 2,
                      backdropFilter: 'blur(10px)',
                    }}
                  />
                </motion.div>
              ))}
            </Box>
          </Box>
        </motion.div>

        {/* Live Metrics Dashboard */}
        {liveMetrics && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Paper sx={{ p: 3, mb: 4, bgcolor: 'rgba(0,0,0,0.02)' }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <AutoAwesome color="primary" />
                Live Platform Statistics
              </Typography>
              
              <Grid container spacing={3} sx={{ mb: 4 }}>
                                <Grid item xs={12} sm={6} md={3}>
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5, delay: 0 * 0.1 }}
                  >
                    <Card sx={{ 
                      textAlign: 'center', 
                      height: '140px',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      position: 'relative',
                      overflow: 'hidden',
                      '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        height: '3px',
                        background: 'linear-gradient(90deg, #FF6B6B 0%, #ff8c61 100%)',
                      },
                    }}>
                      <CardContent sx={{ py: 3 }}>
                        <Typography 
                          variant="h3" 
                          sx={{ 
                            fontWeight: 800, 
                            background: 'linear-gradient(135deg, #FF6B6B 0%, #ff8c61 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            mb: 1,
                            textShadow: '0 0 20px rgba(255, 107, 107, 0.3)',
                          }}
                        >
                          {liveMetrics.live_stats.workflows_completed.toLocaleString()}
                        </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 500, color: 'rgba(255, 255, 255, 0.8)' }}>
                          Workflows Completed
                        </Typography>
                      </CardContent>
                    </Card>
                  </motion.div>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <motion.div
                    whileHover={{ scale: 1.05, y: -4 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Card sx={{ 
                      textAlign: 'center', 
                      height: '140px',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      position: 'relative',
                      overflow: 'hidden',
                      '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        height: '3px',
                        background: 'linear-gradient(90deg, #4ECDC4 0%, #6ee8e0 100%)',
                      },
                    }}>
                      <CardContent sx={{ py: 3 }}>
                        <Typography 
                          variant="h3" 
                          sx={{ 
                            fontWeight: 800, 
                            background: 'linear-gradient(135deg, #4ECDC4 0%, #6ee8e0 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            mb: 1,
                            textShadow: '0 0 20px rgba(78, 205, 196, 0.3)',
                          }}
                        >
                        {liveMetrics.live_stats.lines_of_code_generated.toLocaleString()}
                      </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 500, color: 'rgba(255, 255, 255, 0.8)' }}>
                          Lines of Code Generated
                        </Typography>
                    </CardContent>
                  </Card>
                  </motion.div>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <motion.div
                    whileHover={{ scale: 1.05, y: -4 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Card sx={{ 
                      textAlign: 'center', 
                      height: '140px',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      position: 'relative',
                      overflow: 'hidden',
                      '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        height: '3px',
                        background: 'linear-gradient(90deg, #DDA0DD 0%, #e8b3e8 100%)',
                      },
                    }}>
                      <CardContent sx={{ py: 3 }}>
                        <Typography 
                          variant="h3" 
                          sx={{ 
                            fontWeight: 800, 
                            background: 'linear-gradient(135deg, #DDA0DD 0%, #e8b3e8 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            mb: 1,
                            textShadow: '0 0 20px rgba(221, 160, 221, 0.3)',
                          }}
                        >
                        {liveMetrics.live_stats.security_vulnerabilities_prevented.toLocaleString()}
                      </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 500, color: 'rgba(255, 255, 255, 0.8)' }}>
                          Security Issues Prevented
                        </Typography>
                    </CardContent>
                  </Card>
                  </motion.div>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <motion.div
                    whileHover={{ scale: 1.05, y: -4 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Card sx={{ 
                      textAlign: 'center', 
                      height: '140px',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      position: 'relative',
                      overflow: 'hidden',
                      '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        height: '3px',
                        background: 'linear-gradient(90deg, #FFEAA7 0%, #fff4c7 100%)',
                      },
                    }}>
                      <CardContent sx={{ py: 3 }}>
                        <Typography 
                          variant="h3" 
                          sx={{ 
                            fontWeight: 800, 
                            background: 'linear-gradient(135deg, #FFEAA7 0%, #fff4c7 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            mb: 1,
                            textShadow: '0 0 20px rgba(255, 234, 167, 0.3)',
                          }}
                        >
                        {liveMetrics.live_stats.developer_time_saved_hours.toLocaleString()}h
                      </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 500, color: 'rgba(255, 255, 255, 0.8)' }}>
                          Developer Time Saved
                        </Typography>
                    </CardContent>
                  </Card>
                  </motion.div>
                </Grid>
              </Grid>

              {/* Real-time Activity Feed */}
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>Real-time Activity:</Typography>
                <Box sx={{ maxHeight: 100, overflow: 'hidden' }}>
                  <AnimatePresence>
                    {currentActivity.map((activity, index) => (
                      <motion.div
                        key={`${activity}-${index}`}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1 - (index * 0.2), x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <Typography 
                          variant="caption" 
                          sx={{ 
                            display: 'block', 
                            opacity: 1 - (index * 0.2),
                            fontSize: index === 0 ? '0.875rem' : '0.75rem'
                          }}
                        >
                          {activity}
                        </Typography>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </Box>
              </Box>
            </Paper>
          </motion.div>
        )}

        {/* Debug Toggle Card */}
        {renderDebugToggleCard()}

        <Grid container spacing={4}>
          {/* Left Column - Input Form */}
          <Grid item xs={12} md={6}>
            {/* Demo Scenarios */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  🎯 Demo Scenarios
                </Typography>
                <Grid container spacing={2}>
                  {scenarios.map((scenario) => (
                    <Grid item xs={12} sm={6} key={scenario.id}>
                      <Card 
                        sx={{ 
                          cursor: 'pointer',
                          transition: 'all 0.2s',
                          '&:hover': { 
                            transform: 'translateY(-2px)',
                            boxShadow: 3 
                          }
                        }}
                        onClick={() => handleScenarioSelect(scenario)}
                      >
                        <CardContent sx={{ p: 2 }}>
                          <Typography variant="subtitle2" gutterBottom>
                            {scenario.title}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {scenario.expected_duration}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </motion.div>

            {/* Workflow Configuration */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  ⚙️ Configure Workflow
                </Typography>
                
                <form onSubmit={executeWorkflow}>
                  <TextField
                    fullWidth
                    label="Project Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    margin="normal"
                    required
                    multiline
                    rows={4}
                    placeholder="Describe your project in detail..."
                  />

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

                  <FormControl fullWidth margin="normal">
                    <InputLabel>Workflow Type</InputLabel>
                    <Select
                      value={workflowType}
                      label="Workflow Type"
                      onChange={(e) => setWorkflowType(e.target.value)}
                    >
                      {workflowTypes.map((type) => (
                        <MenuItem key={type.value} value={type.value}>
                          {type.label}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>

                  {renderWorkflowControls()}
                </form>
              </Paper>
            </motion.div>
          </Grid>

          {/* Right Column - Workflow Progress & Results */}
          <Grid item xs={12} md={6}>
            {/* Workflow Progress */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  🔄 Workflow Progress
                </Typography>
                
                {error && (
                  <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                  </Alert>
                )}

                {workflowStatus && (
                  <Box sx={{ mb: 2 }}>
                    <Chip 
                      label={`Workflow ID: ${workflowStatus.workflow_id}`} 
                      size="small" 
                      sx={{ mr: 2 }}
                    />
                    <Chip 
                      label={workflowStatus.status} 
                      color={workflowStatus.status === 'completed' ? 'success' : 
                             workflowStatus.status === 'failed' ? 'error' : 'primary'} 
                      size="small" 
                    />
                    {workflowProgress > 0 && (
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="caption" color="text.secondary">
                          Overall Progress: {Math.round(workflowProgress)}%
                        </Typography>
                        <LinearProgress 
                          variant="determinate" 
                          value={workflowProgress} 
                          sx={{ mt: 0.5, height: 6, borderRadius: 3 }}
                        />
                      </Box>
                    )}
                  </Box>
                )}

                <Stepper activeStep={activeStep} orientation="vertical">
                  {workflowStatus?.steps?.filter(step => step && step.status)?.map((step, index) => {
                    if (!step || !step.status) return null;
                    const stepStatus = getStepStatus(step);
                    return (
                      <Step key={step.step_id || index}>
                        <StepLabel
                          icon={stepStatus.icon}
                          error={step.status === 'failed'}
                        >
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                            <Typography variant="subtitle2">
                              {step.agent_name || 'Unknown Agent'}
                            </Typography>
                            {step.start_time && step.end_time && (
                              <Chip 
                                label={formatDuration(step.start_time, step.end_time)} 
                                size="small" 
                                variant="outlined"
                              />
                            )}
                            {step.status === 'running' && step.progress !== undefined && (
                              <Chip 
                                label={`${Math.round(step.progress)}%`}
                                size="small" 
                                color="primary"
                                variant="outlined"
                              />
                            )}
                          </Box>
                        </StepLabel>
                        <StepContent>
                          {step.status === 'running' && step.progress !== undefined && (
                            <Box sx={{ mb: 2 }}>
                              <Typography variant="caption" color="text.secondary">
                                Step Progress: {Math.round(step.progress)}%
                              </Typography>
                              <LinearProgress 
                                variant="determinate" 
                                value={step.progress} 
                                sx={{ mt: 0.5, height: 4, borderRadius: 2 }}
                              />
                            </Box>
                          )}
                          {step.error && (
                            <Alert severity="error" sx={{ mb: 1 }}>
                              {step.error}
                            </Alert>
                          )}
                          {step.result && (
                            <Box sx={{ mt: 2 }}>
                              {/* Display formatted content if available */}
                              {step.result.display_content ? (
                                <Paper sx={{ p: 3, backgroundColor: 'rgba(0,0,0,0.02)', border: '1px solid rgba(0,0,0,0.1)' }}>
                                  <Typography variant="body2" component="pre" sx={{ 
                                    fontSize: '0.875rem', 
                                    margin: 0, 
                                    whiteSpace: 'pre-wrap',
                                    fontFamily: 'monospace',
                                    lineHeight: 1.6,
                                    color: 'text.primary'
                                  }}>
                                    {step.result.display_content}
                                  </Typography>
                                </Paper>
                              ) : step.result.formatted_output ? (
                                <Paper sx={{ p: 3, backgroundColor: 'rgba(0,0,0,0.02)', border: '1px solid rgba(0,0,0,0.1)' }}>
                                  <Typography variant="body2" component="pre" sx={{ 
                                    fontSize: '0.875rem', 
                                    margin: 0, 
                                    whiteSpace: 'pre-wrap',
                                    fontFamily: 'monospace',
                                    lineHeight: 1.6,
                                    color: 'text.primary'
                                  }}>
                                    {step.result.formatted_output}
                                  </Typography>
                                </Paper>
                              ) : step.result.summary ? (
                                <Alert severity="success" sx={{ mb: 2 }}>
                                  <Typography variant="body2">
                                    {step.result.summary}
                                  </Typography>
                                </Alert>
                              ) : (
                                <Paper sx={{ p: 2, backgroundColor: '#2d2d2d' }}>
                                  <pre style={{ 
                                    fontSize: '0.8rem', 
                                    margin: 0, 
                                    whiteSpace: 'pre-wrap',
                                    maxHeight: '200px',
                                    overflow: 'auto'
                                  }}>
                                    {typeof step.result === 'string' 
                                      ? step.result 
                                      : JSON.stringify(step.result, null, 2)}
                                  </pre>
                                </Paper>
                              )}
                            </Box>
                          )}
                        </StepContent>
                      </Step>
                    );
                  }) || []}
                </Stepper>
              </Paper>
            </motion.div>

            {/* Real-time Activity Feed */}
            {renderRealTimeActivity()}

            {/* Completed Results */}
            {renderCompletedResults()}

            {/* Generated Code Preview */}
            {Object.keys(generatedCode).length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <CodePreview 
                  files={generatedCode} 
                  title="Generated Application Code" 
                  language="python" 
                />
              </motion.div>
            )}

            {/* Results Dialog */}
            {renderResultsDialog()}

            {/* Debug Dialog */}
            {renderDebugDialog()}
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default MultiAgentOrchestrator;