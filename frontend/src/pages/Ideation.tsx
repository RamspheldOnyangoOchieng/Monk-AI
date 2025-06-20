import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Container,
  Divider,
  FormControl,
  Grid,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  MenuItem,
  Paper,
  Select,
  Tab,
  Tabs,
  TextField,
  Typography,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Add as AddIcon,
  ExpandMore as ExpandMoreIcon,
  LightbulbOutlined as IdeaIcon,
  Code as CodeIcon,
  Assignment as StoryIcon,
  ViewTimeline as SprintIcon,
  Description as SpecIcon,
} from '@mui/icons-material';
import axios from 'axios';

// Define interfaces for the data structures
interface ProjectScope {
  project_overview: string;
  goals_and_objectives: string[];
  key_features: string[];
  technical_requirements: string[];
  constraints_and_limitations: string[];
  timeline_estimates: {
    planning_phase: string;
    development_phase: string;
    testing_phase: string;
    deployment_phase: string;
  };
  resources_needed: string[];
}

interface TechnicalSpec {
  system_architecture: {
    frontend: string;
    backend: string;
    database: string;
    caching: string;
    deployment: string;
  };
  data_models: Array<{
    name: string;
    fields: Array<{
      name: string;
      type: string;
      description: string;
    }>;
  }>;
  api_endpoints: Array<{
    path: string;
    methods: string[];
    description: string;
  }>;
  third_party_integrations: Array<{
    name: string;
    purpose: string;
    implementation: string;
  }>;
  security_considerations: string[];
  scalability_plans: string[];
  technology_stack: {
    frontend: string[];
    backend: string[];
    database: string[];
    devops: string[];
  };
}

interface UserStory {
  id: string;
  as_a: string;
  i_want_to: string;
  so_that: string;
  priority: string;
  story_points: number;
  acceptance_criteria: string[];
}

interface Sprint {
  sprint_number: number;
  sprint_goal: string;
  user_stories: UserStory[];
  total_story_points: number;
  key_deliverables: string[];
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

// Tab Panel component for the tabbed interface
function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`ideation-tabpanel-${index}`}
      aria-labelledby={`ideation-tab-${index}`}
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

const Ideation = () => {
  // State for the tabbed interface
  const [tabValue, setTabValue] = useState(0);

  // State for project scope
  const [projectDescription, setProjectDescription] = useState('');
  const [templateKey, setTemplateKey] = useState('');
  const [projectScope, setProjectScope] = useState<ProjectScope | null>(null);

  // State for technical specs
  const [technicalSpecs, setTechnicalSpecs] = useState<TechnicalSpec | null>(null);

  // State for user stories
  const [userStories, setUserStories] = useState<UserStory[]>([]);

  // State for sprint planning
  const [sprintCount, setSprintCount] = useState(3);
  const [sprintPlan, setSprintPlan] = useState<Sprint[]>([]);

  // Loading and error states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Handle generating project scope
  const handleGenerateProjectScope = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/generate-project-scope', {
        description: projectDescription,
        template_key: templateKey || undefined,
      });

      setProjectScope(response.data.project_scope);
      // Automatically move to the next tab after generating scope
      setTabValue(1);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate project scope');
    } finally {
      setLoading(false);
    }
  };

  // Handle generating technical specs
  const handleGenerateTechnicalSpecs = async () => {
    if (!projectScope) {
      setError('Please generate a project scope first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/generate-technical-specs', {
        project_scope: projectScope,
      });

      setTechnicalSpecs(response.data.technical_specs);
      // Automatically move to the next tab after generating specs
      setTabValue(2);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate technical specifications');
    } finally {
      setLoading(false);
    }
  };

  // Handle generating user stories
  const handleGenerateUserStories = async () => {
    if (!projectScope) {
      setError('Please generate a project scope first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/generate-user-stories', {
        project_scope: projectScope,
      });

      setUserStories(response.data.user_stories);
      // Automatically move to the next tab after generating user stories
      setTabValue(3);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate user stories');
    } finally {
      setLoading(false);
    }
  };

  // Handle generating sprint plan
  const handleGenerateSprintPlan = async () => {
    if (userStories.length === 0) {
      setError('Please generate user stories first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/generate-sprint-plan', {
        user_stories: userStories,
        sprint_count: sprintCount,
      });

      setSprintPlan(response.data.sprint_plan);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate sprint plan');
    } finally {
      setLoading(false);
    }
  };

  // Get color for priority
  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Ideation
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" paragraph>
          Define your project scope, generate technical specifications, create user stories, and plan sprints.
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="ideation tabs">
            <Tab icon={<IdeaIcon />} label="Project Scope" />
            <Tab icon={<SpecIcon />} label="Technical Specs" />
            <Tab icon={<StoryIcon />} label="User Stories" />
            <Tab icon={<SprintIcon />} label="Sprint Planning" />
          </Tabs>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Project Scope Tab */}
        <TabPanel value={tabValue} index={0}>
          <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Define Your Project
            </Typography>
            <form onSubmit={handleGenerateProjectScope}>
              <TextField
                label="Project Description"
                multiline
                rows={4}
                fullWidth
                value={projectDescription}
                onChange={(e) => setProjectDescription(e.target.value)}
                placeholder="Describe your project in detail. What problem does it solve? Who are the users? What are the main features?"
                required
                sx={{ mb: 2 }}
              />

              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel id="template-select-label">Project Template (Optional)</InputLabel>
                <Select
                  labelId="template-select-label"
                  value={templateKey}
                  label="Project Template (Optional)"
                  onChange={(e) => setTemplateKey(e.target.value)}
                >
                  <MenuItem value="">None</MenuItem>
                  <MenuItem value="web_app">Web Application</MenuItem>
                  <MenuItem value="mobile_app">Mobile Application</MenuItem>
                  <MenuItem value="api">API Service</MenuItem>
                  <MenuItem value="data_pipeline">Data Pipeline</MenuItem>
                  <MenuItem value="ml_model">Machine Learning Model</MenuItem>
                  <MenuItem value="desktop_app">Desktop Application</MenuItem>
                </Select>
              </FormControl>

              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading || !projectDescription}
                startIcon={loading ? <CircularProgress size={20} /> : <IdeaIcon />}
              >
                {loading ? 'Generating...' : 'Generate Project Scope'}
              </Button>
            </form>
          </Paper>

          {projectScope && (
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Project Scope
              </Typography>
              
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Project Overview
              </Typography>
              <Typography paragraph>{projectScope.project_overview}</Typography>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Goals and Objectives
              </Typography>
              <List dense>
                                      {projectScope?.goals_and_objectives?.map((goal, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={goal} />
                  </ListItem>
                ))}
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Key Features
              </Typography>
              <List dense>
                                      {projectScope?.key_features?.map((feature, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={feature} />
                  </ListItem>
                ))}
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Technical Requirements
              </Typography>
              <List dense>
                                      {projectScope?.technical_requirements?.map((req, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={req} />
                  </ListItem>
                ))}
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Constraints and Limitations
              </Typography>
              <List dense>
                                      {projectScope?.constraints_and_limitations?.map((constraint, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={constraint} />
                  </ListItem>
                ))}
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Timeline Estimates
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle2" color="text.secondary">
                        Planning Phase
                      </Typography>
                      <Typography variant="h6">
                        {projectScope?.timeline_estimates?.planning_phase || 'Not specified'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle2" color="text.secondary">
                        Development Phase
                      </Typography>
                      <Typography variant="h6">
                        {projectScope?.timeline_estimates?.development_phase || 'Not specified'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle2" color="text.secondary">
                        Testing Phase
                      </Typography>
                      <Typography variant="h6">
                        {projectScope?.timeline_estimates?.testing_phase || 'Not specified'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle2" color="text.secondary">
                        Deployment Phase
                      </Typography>
                      <Typography variant="h6">
                        {projectScope?.timeline_estimates?.deployment_phase || 'Not specified'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Resources Needed
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                      {projectScope?.resources_needed?.map((resource, index) => (
                  <Chip key={index} label={resource} />
                ))}
              </Box>
              
              <Box sx={{ mt: 3 }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setTabValue(1)}
                >
                  Continue to Technical Specs
                </Button>
              </Box>
            </Paper>
          )}
        </TabPanel>

        {/* Technical Specs Tab */}
        <TabPanel value={tabValue} index={1}>
          {!projectScope ? (
            <Alert severity="info">
              Please generate a project scope first in the Project Scope tab.
            </Alert>
          ) : (
            <>
              <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Technical Specifications
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleGenerateTechnicalSpecs}
                    disabled={loading}
                    startIcon={loading ? <CircularProgress size={20} /> : <CodeIcon />}
                  >
                    {loading ? 'Generating...' : 'Generate Technical Specs'}
                  </Button>
                </Box>
                <Typography color="text.secondary">
                  Generate detailed technical specifications based on your project scope.
                </Typography>
              </Paper>

              {technicalSpecs && (
                <Paper elevation={3} sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    System Architecture
                  </Typography>
                  <Grid container spacing={2} sx={{ mb: 3 }}>
                    <Grid item xs={12} sm={6} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" color="text.secondary">
                            Frontend
                          </Typography>
                          <Typography variant="body1">
                            {technicalSpecs?.system_architecture?.frontend || 'Not specified'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" color="text.secondary">
                            Backend
                          </Typography>
                          <Typography variant="body1">
                            {technicalSpecs?.system_architecture?.backend || 'Not specified'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" color="text.secondary">
                            Database
                          </Typography>
                          <Typography variant="body1">
                            {technicalSpecs?.system_architecture?.database || 'Not specified'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" color="text.secondary">
                            Caching
                          </Typography>
                          <Typography variant="body1">
                            {technicalSpecs?.system_architecture?.caching || 'Not specified'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" color="text.secondary">
                            Deployment
                          </Typography>
                          <Typography variant="body1">
                            {technicalSpecs?.system_architecture?.deployment || 'Not specified'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>

                  <Divider sx={{ my: 3 }} />

                  <Typography variant="h6" gutterBottom>
                    Data Models
                  </Typography>
                  {technicalSpecs?.data_models?.map((model, index) => (
                    <Accordion key={index} sx={{ mb: 1 }}>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography fontWeight="bold">{model.name}</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <List dense>
                          {model.fields?.map((field, fieldIndex) => (
                            <ListItem key={fieldIndex}>
                              <ListItemText 
                                primary={`${field.name} (${field.type})`} 
                                secondary={field.description} 
                              />
                            </ListItem>
                          ))}
                        </List>
                      </AccordionDetails>
                    </Accordion>
                  ))}

                  <Divider sx={{ my: 3 }} />

                  <Typography variant="h6" gutterBottom>
                    API Endpoints
                  </Typography>
                  {technicalSpecs?.api_endpoints?.map((endpoint, index) => (
                    <Box key={index} sx={{ mb: 2, p: 2, border: 1, borderColor: 'divider', borderRadius: 1 }}>
                      <Typography fontWeight="bold" sx={{ mb: 1 }}>
                        {endpoint.path}
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                        {endpoint.methods?.map((method, methodIndex) => (
                          <Chip 
                            key={methodIndex} 
                            label={method} 
                            size="small" 
                            color={method === 'GET' ? 'success' : method === 'POST' ? 'primary' : method === 'PUT' ? 'warning' : 'error'}
                          />
                        ))}
                      </Box>
                      <Typography variant="body2">
                        {endpoint.description}
                      </Typography>
                    </Box>
                  ))}

                  <Divider sx={{ my: 3 }} />

                  <Typography variant="h6" gutterBottom>
                    Third-Party Integrations
                  </Typography>
                  <Grid container spacing={2} sx={{ mb: 3 }}>
                    {technicalSpecs?.third_party_integrations?.map((integration, index) => (
                      <Grid item xs={12} sm={6} md={4} key={index}>
                        <Card variant="outlined">
                          <CardContent>
                            <Typography variant="subtitle1" fontWeight="bold">
                              {integration.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                              {integration.purpose}
                            </Typography>
                            <Typography variant="body2">
                              {integration.implementation}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>

                  <Divider sx={{ my: 3 }} />

                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="h6" gutterBottom>
                        Security Considerations
                      </Typography>
                      <List dense>
                        {technicalSpecs?.security_considerations?.map((item, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={item} />
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="h6" gutterBottom>
                        Scalability Plans
                      </Typography>
                      <List dense>
                        {technicalSpecs?.scalability_plans?.map((item, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={item} />
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                  </Grid>

                  <Divider sx={{ my: 3 }} />

                  <Typography variant="h6" gutterBottom>
                    Technology Stack
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6} md={3}>
                      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        Frontend
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {technicalSpecs?.technology_stack?.frontend?.map((tech, index) => (
                          <Chip key={index} label={tech} size="small" />
                        ))}
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        Backend
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {technicalSpecs?.technology_stack?.backend?.map((tech, index) => (
                          <Chip key={index} label={tech} size="small" />
                        ))}
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        Database
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {technicalSpecs?.technology_stack?.database?.map((tech, index) => (
                          <Chip key={index} label={tech} size="small" />
                        ))}
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        DevOps
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {technicalSpecs?.technology_stack?.devops?.map((tech, index) => (
                          <Chip key={index} label={tech} size="small" />
                        ))}
                      </Box>
                    </Grid>
                  </Grid>

                  <Box sx={{ mt: 3 }}>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => setTabValue(2)}
                    >
                      Continue to User Stories
                    </Button>
                  </Box>
                </Paper>
              )}
            </>
          )}
        </TabPanel>

        {/* User Stories Tab */}
        <TabPanel value={tabValue} index={2}>
          {!projectScope ? (
            <Alert severity="info">
              Please generate a project scope first in the Project Scope tab.
            </Alert>
          ) : (
            <>
              <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    User Stories
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleGenerateUserStories}
                    disabled={loading}
                    startIcon={loading ? <CircularProgress size={20} /> : <StoryIcon />}
                  >
                    {loading ? 'Generating...' : 'Generate User Stories'}
                  </Button>
                </Box>
                <Typography color="text.secondary">
                  Generate user stories based on your project scope to define the features from the user's perspective.
                </Typography>
              </Paper>

              {userStories.length > 0 && (
                <Paper elevation={3} sx={{ p: 3 }}>
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      User Stories
                    </Typography>
                    <Typography color="text.secondary">
                      {userStories.length} user stories generated
                    </Typography>
                  </Box>

                  {userStories?.map((story, index) => (
                    <Card key={index} variant="outlined" sx={{ mb: 2 }}>
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                          <Typography variant="subtitle1" fontWeight="bold">
                            {story.id}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Chip 
                              label={`${story.priority}`} 
                              size="small" 
                              color={getPriorityColor(story.priority) as any}
                            />
                            <Chip 
                              label={`${story.story_points} points`} 
                              size="small" 
                              variant="outlined"
                            />
                          </Box>
                        </Box>

                        <Typography paragraph>
                          <strong>As a</strong> {story.as_a}, <strong>I want to</strong> {story.i_want_to}, <strong>so that</strong> {story.so_that}
                        </Typography>

                        <Typography variant="subtitle2" gutterBottom>
                          Acceptance Criteria:
                        </Typography>
                        <List dense>
                                                      {story.acceptance_criteria?.map((criteria, criteriaIndex) => (
                            <ListItem key={criteriaIndex}>
                              <ListItemText primary={criteria} />
                            </ListItem>
                          ))}
                        </List>
                      </CardContent>
                    </Card>
                  ))}

                  <Box sx={{ mt: 3 }}>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => setTabValue(3)}
                    >
                      Continue to Sprint Planning
                    </Button>
                  </Box>
                </Paper>
              )}
            </>
          )}
        </TabPanel>

        {/* Sprint Planning Tab */}
        <TabPanel value={tabValue} index={3}>
          {userStories.length === 0 ? (
            <Alert severity="info">
              Please generate user stories first in the User Stories tab.
            </Alert>
          ) : (
            <>
              <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Sprint Planning
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <TextField
                      label="Number of Sprints"
                      type="number"
                      value={sprintCount}
                      onChange={(e) => setSprintCount(parseInt(e.target.value) || 3)}
                      InputProps={{ inputProps: { min: 1, max: 10 } }}
                      size="small"
                      sx={{ width: 150 }}
                    />
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={handleGenerateSprintPlan}
                      disabled={loading}
                      startIcon={loading ? <CircularProgress size={20} /> : <SprintIcon />}
                    >
                      {loading ? 'Generating...' : 'Generate Sprint Plan'}
                    </Button>
                  </Box>
                </Box>
                <Typography color="text.secondary">
                  Generate a sprint plan based on your user stories to organize the development process.
                </Typography>
              </Paper>

              {sprintPlan.length > 0 && (
                <Paper elevation={3} sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Sprint Plan
                  </Typography>

                  {sprintPlan?.map((sprint, index) => (
                    <Accordion key={index} defaultExpanded={index === 0} sx={{ mb: 2 }}>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', pr: 2 }}>
                          <Typography fontWeight="bold">
                            Sprint {sprint.sprint_number}
                          </Typography>
                          <Chip 
                            label={`${sprint.total_story_points} points`} 
                            size="small" 
                            color="primary"
                          />
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                          Goal: {sprint.sprint_goal}
                        </Typography>

                        <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                          Key Deliverables:
                        </Typography>
                        <List dense>
                                                        {sprint.key_deliverables?.map((deliverable, deliverableIndex) => (
                            <ListItem key={deliverableIndex}>
                              <ListItemText primary={deliverable} />
                            </ListItem>
                          ))}
                        </List>

                        <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                          User Stories:
                        </Typography>
                                                      {sprint.user_stories?.map((story, storyIndex) => (
                          <Card key={storyIndex} variant="outlined" sx={{ mb: 1 }}>
                            <CardContent sx={{ py: 1 }}>
                              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <Typography variant="body2">
                                  <strong>{story.id}:</strong> As a {story.as_a}, I want to {story.i_want_to}
                                </Typography>
                                <Box sx={{ display: 'flex', gap: 1 }}>
                                  <Chip 
                                    label={story.priority} 
                                    size="small" 
                                    color={getPriorityColor(story.priority) as any}
                                  />
                                  <Chip 
                                    label={`${story.story_points} pts`} 
                                    size="small" 
                                    variant="outlined"
                                  />
                                </Box>
                              </Box>
                            </CardContent>
                          </Card>
                        ))}
                      </AccordionDetails>
                    </Accordion>
                  ))}

                  <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
                    <Button
                      variant="contained"
                      color="success"
                      startIcon={<AddIcon />}
                    >
                      Export to Project Management Tool
                    </Button>
                  </Box>
                </Paper>
              )}
            </>
          )}
        </TabPanel>
      </Box>
    </Container>
  );
};

export default Ideation;