import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Container,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Divider,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  CircularProgress,
  Alert,
  Chip,
  IconButton,
  Tooltip,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControlLabel,
  Switch,
  Tabs,
  Tab,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemSecondaryAction,
  Snackbar,
  Badge,
  Dialog as MuiDialog,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Refresh as RefreshIcon,
  Group as GroupIcon,
  Person as PersonIcon,
  Code as CodeIcon,
  Assignment as AssignmentIcon,
  Chat as ChatIcon,
  MoreVert as MoreVertIcon,
  Send as SendIcon,
  AttachFile as AttachFileIcon,
  Close as CloseIcon,
} from '@mui/icons-material';

// Define interfaces for our data models
interface Team {
  id: number;
  name: string;
  description: string;
  avatar_url?: string;
  members_count: number;
  created_at: string;
}

interface TeamMember {
  id: number;
  user_id: number;
  username: string;
  email: string;
  avatar_url?: string;
  role: 'owner' | 'admin' | 'member';
  is_active: boolean;
  joined_at: string;
}

interface Project {
  id: number;
  name: string;
  description: string;
  repository_url: string;
  status: 'active' | 'archived' | 'completed';
  programming_language: string;
  created_at: string;
}

interface Message {
  id: number;
  sender_id: number;
  sender_name: string;
  sender_avatar?: string;
  content: string;
  timestamp: string;
  attachments?: Array<{
    id: number;
    name: string;
    url: string;
    type: string;
  }>;
}

interface TeamFormData {
  name: string;
  description: string;
  avatar_url?: string;
}

interface ProjectFormData {
  name: string;
  description: string;
  repository_url: string;
  programming_language: string;
}

interface MemberFormData {
  email: string;
  role: 'owner' | 'admin' | 'member';
}

// Mock data for development
const teamsMock: Team[] = [
  {
    id: 1,
    name: 'Frontend Team',
    description: 'Responsible for all frontend development',
    avatar_url: 'https://via.placeholder.com/40',
    members_count: 5,
    created_at: '2023-01-15T10:30:00Z',
  },
  {
    id: 2,
    name: 'Backend Team',
    description: 'Handles API and database development',
    avatar_url: 'https://via.placeholder.com/40',
    members_count: 4,
    created_at: '2023-01-20T14:45:00Z',
  },
  {
    id: 3,
    name: 'DevOps',
    description: 'Infrastructure and deployment',
    avatar_url: 'https://via.placeholder.com/40',
    members_count: 3,
    created_at: '2023-02-05T09:15:00Z',
  },
];

const membersMock: TeamMember[] = [
  {
    id: 1,
    user_id: 101,
    username: 'johndoe',
    email: 'john@example.com',
    avatar_url: 'https://via.placeholder.com/40',
    role: 'owner',
    is_active: true,
    joined_at: '2023-01-15T10:30:00Z',
  },
  {
    id: 2,
    user_id: 102,
    username: 'janedoe',
    email: 'jane@example.com',
    avatar_url: 'https://via.placeholder.com/40',
    role: 'admin',
    is_active: true,
    joined_at: '2023-01-16T11:20:00Z',
  },
  {
    id: 3,
    user_id: 103,
    username: 'bobsmith',
    email: 'bob@example.com',
    avatar_url: 'https://via.placeholder.com/40',
    role: 'member',
    is_active: true,
    joined_at: '2023-01-18T14:10:00Z',
  },
  {
    id: 4,
    user_id: 104,
    username: 'alicejones',
    email: 'alice@example.com',
    avatar_url: 'https://via.placeholder.com/40',
    role: 'member',
    is_active: false,
    joined_at: '2023-01-20T09:45:00Z',
  },
];

const projectsMock: Project[] = [
  {
    id: 1,
    name: 'User Authentication Service',
    description: 'Secure authentication and authorization service',
    repository_url: 'https://github.com/org/auth-service',
    status: 'active',
    programming_language: 'Python',
    created_at: '2023-01-25T10:00:00Z',
  },
  {
    id: 2,
    name: 'Frontend Dashboard',
    description: 'Main dashboard UI components',
    repository_url: 'https://github.com/org/dashboard-ui',
    status: 'active',
    programming_language: 'TypeScript',
    created_at: '2023-02-10T11:30:00Z',
  },
  {
    id: 3,
    name: 'API Gateway',
    description: 'Central API gateway for microservices',
    repository_url: 'https://github.com/org/api-gateway',
    status: 'completed',
    programming_language: 'Go',
    created_at: '2023-01-05T14:20:00Z',
  },
];

const messagesMock: Message[] = [
  {
    id: 1,
    sender_id: 101,
    sender_name: 'John Doe',
    sender_avatar: 'https://via.placeholder.com/40',
    content: 'Hey team, I just pushed the new authentication module. Please review when you get a chance.',
    timestamp: '2023-03-10T09:30:00Z',
  },
  {
    id: 2,
    sender_id: 102,
    sender_name: 'Jane Doe',
    sender_avatar: 'https://via.placeholder.com/40',
    content: "I'll take a look at it this afternoon. Are there any specific areas you want me to focus on?",
    timestamp: '2023-03-10T09:45:00Z',
  },
  {
    id: 3,
    sender_id: 103,
    sender_name: 'Bob Smith',
    sender_avatar: 'https://via.placeholder.com/40',
    content: 'I have reviewed the code and left some comments. Please check.',
    timestamp: '2023-03-10T10:00:00Z',
  },
];

const Collaboration: React.FC = () => {
  // State for teams, members, projects, and messages
  const [teams, setTeams] = useState<Team[]>(teamsMock);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>(membersMock);
  const [projects, setProjects] = useState<Project[]>(projectsMock);
  const [messages, setMessages] = useState<Message[]>(messagesMock);
  const [newMessage, setNewMessage] = useState<string>('');
  
  // UI state
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [tabValue, setTabValue] = useState<number>(0);
  const [showTeamDialog, setShowTeamDialog] = useState<boolean>(false);
  const [showProjectDialog, setShowProjectDialog] = useState<boolean>(false);
  const [showMemberDialog, setShowMemberDialog] = useState<boolean>(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<boolean>(false);
  const [deleteItemType, setDeleteItemType] = useState<'team' | 'project' | 'member'>('team');
  const [deleteItemId, setDeleteItemId] = useState<number | null>(null);
  
  // Form data
  const [teamFormData, setTeamFormData] = useState<TeamFormData>({
    name: '',
    description: '',
  });
  const [projectFormData, setProjectFormData] = useState<ProjectFormData>({
    name: '',
    description: '',
    repository_url: '',
    programming_language: 'Python',
  });
  const [memberFormData, setMemberFormData] = useState<MemberFormData>({
    email: '',
    role: 'member',
  });
  
  // Edit mode
  const [editMode, setEditMode] = useState<boolean>(false);
  const [editId, setEditId] = useState<number | null>(null);
  
  // Snackbar
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error' | 'info' | 'warning'}>({ 
    open: false, 
    message: '', 
    severity: 'info' 
  });

  // Fetch data on component mount
  useEffect(() => {
    // In a real app, you would fetch this data from your API
    // Example: axios.get('/api/teams').then(response => { ... })
  }, []);

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Handle refresh
  const handleRefresh = () => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  };

  // Team form handlers
  const handleTeamFormChange = (field: keyof TeamFormData, value: any) => {
    setTeamFormData({
      ...teamFormData,
      [field]: value,
    });
  };

  const openTeamDialog = (team?: Team) => {
    if (team) {
      setEditMode(true);
      setEditId(team.id);
      setTeamFormData({
        name: team.name,
        description: team.description,
        avatar_url: team.avatar_url,
      });
    } else {
      setEditMode(false);
      setEditId(null);
      setTeamFormData({
        name: '',
        description: '',
        avatar_url: '',
      });
    }
    setShowTeamDialog(true);
  };

  const saveTeam = () => {
    if (!teamFormData.name) {
      setSnackbar({
        open: true,
        message: 'Team name is required',
        severity: 'error'
      });
      return;
    }

    if (editMode && editId !== null) {
      // Update existing team
      const updatedTeams = teams.map(team => {
        if (team.id === editId) {
          return {
            ...team,
            name: teamFormData.name,
            description: teamFormData.description,
            avatar_url: teamFormData.avatar_url,
          };
        }
        return team;
      });
      setTeams(updatedTeams);
      setSnackbar({
        open: true,
        message: 'Team updated successfully',
        severity: 'success'
      });
    } else {
      // Create new team
      const newTeam: Team = {
        id: Math.max(...teams.map(t => t.id), 0) + 1,
        name: teamFormData.name,
        description: teamFormData.description,
        avatar_url: teamFormData.avatar_url,
        members_count: 1, // Start with the creator
        created_at: new Date().toISOString(),
      };
      setTeams([...teams, newTeam]);
      setSnackbar({
        open: true,
        message: 'Team created successfully',
        severity: 'success'
      });
    }

    setShowTeamDialog(false);
  };

  // Project form handlers
  const handleProjectFormChange = (field: keyof ProjectFormData, value: any) => {
    setProjectFormData({
      ...projectFormData,
      [field]: value,
    });
  };

  const openProjectDialog = (project?: Project) => {
    if (project) {
      setEditMode(true);
      setEditId(project.id);
      setProjectFormData({
        name: project.name,
        description: project.description,
        repository_url: project.repository_url,
        programming_language: project.programming_language,
      });
    } else {
      setEditMode(false);
      setEditId(null);
      setProjectFormData({
        name: '',
        description: '',
        repository_url: '',
        programming_language: 'Python',
      });
    }
    setShowProjectDialog(true);
  };

  const saveProject = () => {
    if (!projectFormData.name || !projectFormData.repository_url) {
      setSnackbar({
        open: true,
        message: 'Project name and repository URL are required',
        severity: 'error'
      });
      return;
    }

    if (editMode && editId !== null) {
      // Update existing project
      const updatedProjects = projects.map(project => {
        if (project.id === editId) {
          return {
            ...project,
            name: projectFormData.name,
            description: projectFormData.description,
            repository_url: projectFormData.repository_url,
            programming_language: projectFormData.programming_language,
          };
        }
        return project;
      });
      setProjects(updatedProjects);
      setSnackbar({
        open: true,
        message: 'Project updated successfully',
        severity: 'success'
      });
    } else {
      // Create new project
      const newProject: Project = {
        id: Math.max(...projects.map(p => p.id), 0) + 1,
        name: projectFormData.name,
        description: projectFormData.description,
        repository_url: projectFormData.repository_url,
        programming_language: projectFormData.programming_language,
        status: 'active',
        created_at: new Date().toISOString(),
      };
      setProjects([...projects, newProject]);
      setSnackbar({
        open: true,
        message: 'Project created successfully',
        severity: 'success'
      });
    }

    setShowProjectDialog(false);
  };

  // Member form handlers
  const handleMemberFormChange = (field: keyof MemberFormData, value: any) => {
    setMemberFormData({
      ...memberFormData,
      [field]: value,
    });
  };

  const openMemberDialog = () => {
    setMemberFormData({
      email: '',
      role: 'member',
    });
    setShowMemberDialog(true);
  };

  const addMember = () => {
    if (!memberFormData.email) {
      setSnackbar({
        open: true,
        message: 'Email is required',
        severity: 'error'
      });
      return;
    }

    // In a real app, you would send an invitation to the email
    // For now, we'll just add a mock member
    const newMember: TeamMember = {
      id: Math.max(...teamMembers.map(m => m.id), 0) + 1,
      user_id: Math.floor(Math.random() * 1000) + 200, // Random user ID
      username: memberFormData.email.split('@')[0],
      email: memberFormData.email,
      role: memberFormData.role,
      is_active: true,
      joined_at: new Date().toISOString(),
    };

    setTeamMembers([...teamMembers, newMember]);
    setSnackbar({
      open: true,
      message: 'Team member invited successfully',
      severity: 'success'
    });
    setShowMemberDialog(false);
  };

  // Delete handlers
  const openDeleteConfirm = (type: 'team' | 'project' | 'member', id: number) => {
    setDeleteItemType(type);
    setDeleteItemId(id);
    setShowDeleteConfirm(true);
  };

  const handleDelete = () => {
    if (deleteItemId === null) return;

    switch (deleteItemType) {
      case 'team':
        setTeams(teams.filter(team => team.id !== deleteItemId));
        setSnackbar({
          open: true,
          message: 'Team deleted successfully',
          severity: 'success'
        });
        break;
      case 'project':
        setProjects(projects.filter(project => project.id !== deleteItemId));
        setSnackbar({
          open: true,
          message: 'Project deleted successfully',
          severity: 'success'
        });
        break;
      case 'member':
        setTeamMembers(teamMembers.filter(member => member.id !== deleteItemId));
        setSnackbar({
          open: true,
          message: 'Team member removed successfully',
          severity: 'success'
        });
        break;
    }

    setShowDeleteConfirm(false);
  };

  // Message handlers
  const handleSendMessage = () => {
    if (!newMessage.trim()) return;

    const message: Message = {
      id: Math.max(...messages.map(m => m.id), 0) + 1,
      sender_id: 101, // Current user ID (mock)
      sender_name: 'John Doe', // Current user name (mock)
      sender_avatar: 'https://via.placeholder.com/40',
      content: newMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages([...messages, message]);
    setNewMessage('');
  };

  // Snackbar close handler
  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Select team handler
  const handleSelectTeam = (team: Team) => {
    setSelectedTeam(team);
    // In a real app, you would fetch team members, projects, and messages for this team
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Team Collaboration
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Manage your teams, projects, and collaborate with team members
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Teams List */}
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Teams</Typography>
              <Box>
                <Tooltip title="Refresh">
                  <IconButton size="small" onClick={handleRefresh} disabled={isLoading}>
                    {isLoading ? <CircularProgress size={20} /> : <RefreshIcon />}
                  </IconButton>
                </Tooltip>
                <Tooltip title="Create Team">
                  <IconButton size="small" onClick={() => openTeamDialog()} color="primary">
                    <AddIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Box>
            <Divider sx={{ mb: 2 }} />
            <List sx={{ maxHeight: 'calc(100vh - 300px)', overflow: 'auto' }}>
              {teams.map((team) => (
                <ListItem 
                  key={team.id} 
                  button 
                  selected={selectedTeam?.id === team.id}
                  onClick={() => handleSelectTeam(team)}
                  sx={{ 
                    borderRadius: 1, 
                    mb: 1,
                    '&.Mui-selected': {
                      backgroundColor: 'rgba(0, 255, 136, 0.1)',
                      '&:hover': {
                        backgroundColor: 'rgba(0, 255, 136, 0.2)',
                      }
                    }
                  }}
                >
                  <ListItemAvatar>
                    <Avatar src={team.avatar_url} alt={team.name}>
                      <GroupIcon />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText 
                    primary={team.name} 
                    secondary={`${team.members_count} members`} 
                  />
                  <ListItemSecondaryAction>
                    <Tooltip title="Edit Team">
                      <IconButton edge="end" size="small" onClick={(e) => {
                        e.stopPropagation();
                        openTeamDialog(team);
                      }}>
                        <EditIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete Team">
                      <IconButton edge="end" size="small" onClick={(e) => {
                        e.stopPropagation();
                        openDeleteConfirm('team', team.id);
                      }}>
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
              {teams.length === 0 && (
                <Box sx={{ textAlign: 'center', py: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    No teams found. Create your first team!
                  </Typography>
                </Box>
              )}
            </List>
          </Paper>
        </Grid>

        {/* Team Details */}
        <Grid item xs={12} md={9}>
          {selectedTeam ? (
            <Paper sx={{ p: 0 }}>
              <Box sx={{ p: 2, backgroundColor: 'rgba(0, 255, 136, 0.05)' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Avatar 
                    src={selectedTeam.avatar_url} 
                    alt={selectedTeam.name}
                    sx={{ width: 56, height: 56 }}
                  >
                    <GroupIcon fontSize="large" />
                  </Avatar>
                  <Box>
                    <Typography variant="h5">{selectedTeam.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {selectedTeam.description}
                    </Typography>
                  </Box>
                </Box>
              </Box>
              
              <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={tabValue} onChange={handleTabChange} aria-label="team tabs">
                  <Tab label="Members" />
                  <Tab label="Projects" />
                  <Tab label="Chat" />
                </Tabs>
              </Box>
              
              {/* Members Tab */}
              {tabValue === 0 && (
                <Box sx={{ p: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">Team Members</Typography>
                    <Button
                      startIcon={<AddIcon />}
                      variant="contained"
                      size="small"
                      onClick={openMemberDialog}
                    >
                      Add Member
                    </Button>
                  </Box>
                  <List>
                    {teamMembers.map((member) => (
                      <ListItem key={member.id} sx={{ borderBottom: '1px solid rgba(0, 0, 0, 0.12)' }}>
                        <ListItemAvatar>
                          <Avatar src={member.avatar_url} alt={member.username}>
                            <PersonIcon />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              {member.username}
                              <Chip 
                                label={member.role.toUpperCase()} 
                                size="small" 
                                color={member.role === 'owner' ? 'primary' : member.role === 'admin' ? 'secondary' : 'default'}
                                sx={{ height: 20, fontSize: '0.7rem' }}
                              />
                              {!member.is_active && (
                                <Chip 
                                  label="INACTIVE" 
                                  size="small" 
                                  color="error"
                                  sx={{ height: 20, fontSize: '0.7rem' }}
                                />
                              )}
                            </Box>
                          }
                          secondary={member.email}
                        />
                        <ListItemSecondaryAction>
                          <Tooltip title="Remove Member">
                            <IconButton edge="end" size="small" onClick={() => openDeleteConfirm('member', member.id)}>
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </ListItemSecondaryAction>
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
              
              {/* Projects Tab */}
              {tabValue === 1 && (
                <Box sx={{ p: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">Team Projects</Typography>
                    <Button
                      startIcon={<AddIcon />}
                      variant="contained"
                      size="small"
                      onClick={() => openProjectDialog()}
                    >
                      Add Project
                    </Button>
                  </Box>
                  <Grid container spacing={2}>
                    {projects.map((project) => (
                      <Grid item xs={12} sm={6} md={4} key={project.id}>
                        <Card sx={{ height: '100%' }}>
                          <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                              <Typography variant="h6" component="div">
                                {project.name}
                              </Typography>
                              <Chip 
                                label={project.status.toUpperCase()} 
                                size="small" 
                                color={project.status === 'active' ? 'success' : project.status === 'archived' ? 'warning' : 'info'}
                              />
                            </Box>
                            <Typography variant="body2" color="text.secondary" sx={{ mt: 1, mb: 2 }}>
                              {project.description}
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                              <CodeIcon fontSize="small" color="action" />
                              <Typography variant="body2">{project.programming_language}</Typography>
                            </Box>
                            <Typography variant="caption" color="text.secondary">
                              Created: {new Date(project.created_at).toLocaleDateString()}
                            </Typography>
                          </CardContent>
                          <CardActions>
                            <Button size="small" href={project.repository_url} target="_blank">
                              View Repository
                            </Button>
                            <Box sx={{ flexGrow: 1 }} />
                            <IconButton size="small" onClick={() => openProjectDialog(project)}>
                              <EditIcon fontSize="small" />
                            </IconButton>
                            <IconButton size="small" onClick={() => openDeleteConfirm('project', project.id)}>
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </CardActions>
                        </Card>
                      </Grid>
                    ))}
                    {projects.length === 0 && (
                      <Grid item xs={12}>
                        <Box sx={{ textAlign: 'center', py: 4 }}>
                          <Typography variant="body1" color="text.secondary">
                            No projects found. Add your first project!
                          </Typography>
                        </Box>
                      </Grid>
                    )}
                  </Grid>
                </Box>
              )}
              
              {/* Chat Tab */}
              {tabValue === 2 && (
                <Box sx={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 300px)' }}>
                  <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
                    {messages.map((message) => (
                      <Box 
                        key={message.id} 
                        sx={{ 
                          display: 'flex', 
                          mb: 2,
                          flexDirection: message.sender_id === 101 ? 'row-reverse' : 'row',
                        }}
                      >
                        <Avatar 
                          src={message.sender_avatar} 
                          alt={message.sender_name}
                          sx={{ width: 36, height: 36, mx: 1 }}
                        />
                        <Box 
                          sx={{ 
                            maxWidth: '70%',
                            backgroundColor: message.sender_id === 101 ? 'primary.light' : 'grey.100',
                            color: message.sender_id === 101 ? 'white' : 'inherit',
                            borderRadius: 2,
                            p: 1.5,
                            position: 'relative',
                          }}
                        >
                          <Typography variant="subtitle2">{message.sender_name}</Typography>
                          <Typography variant="body2">{message.content}</Typography>
                          {message.attachments && message.attachments.length > 0 && (
                            <Box sx={{ mt: 1 }}>
                              {message.attachments.map(attachment => (
                                <Chip
                                  key={attachment.id}
                                  icon={<AttachFileIcon />}
                                  label={attachment.name}
                                  size="small"
                                  component="a"
                                  href={attachment.url}
                                  clickable
                                  sx={{ mr: 1 }}
                                />
                              ))}
                            </Box>
                          )}
                          <Typography 
                            variant="caption" 
                            sx={{ 
                              position: 'absolute', 
                              bottom: 2, 
                              right: 8,
                              color: message.sender_id === 101 ? 'rgba(255,255,255,0.7)' : 'text.secondary',
                            }}
                          >
                            {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </Typography>
                        </Box>
                      </Box>
                    ))}
                  </Box>
                  <Box sx={{ p: 2, borderTop: '1px solid rgba(0, 0, 0, 0.12)' }}>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <TextField
                        fullWidth
                        placeholder="Type a message..."
                        variant="outlined"
                        size="small"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSendMessage();
                          }
                        }}
                      />
                      <IconButton color="primary" onClick={handleSendMessage} disabled={!newMessage.trim()}>
                        <SendIcon />
                      </IconButton>
                    </Box>
                  </Box>
                </Box>
              )}
            </Paper>
          ) : (
            <Paper sx={{ p: 4, textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <GroupIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h5" gutterBottom>Select a Team</Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Choose a team from the list or create a new one to start collaborating
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => openTeamDialog()}
              >
                Create New Team
              </Button>
            </Paper>
          )}
        </Grid>
      </Grid>

      {/* Team Dialog */}
      <MuiDialog open={showTeamDialog} onClose={() => setShowTeamDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editMode ? 'Edit Team' : 'Create New Team'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Team Name"
            fullWidth
            variant="outlined"
            value={teamFormData.name}
            onChange={(e) => handleTeamFormChange('name', e.target.value)}
            required
            sx={{ mb: 2, mt: 1 }}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            variant="outlined"
            value={teamFormData.description}
            onChange={(e) => handleTeamFormChange('description', e.target.value)}
            multiline
            rows={3}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Avatar URL"
            fullWidth
            variant="outlined"
            value={teamFormData.avatar_url || ''}
            onChange={(e) => handleTeamFormChange('avatar_url', e.target.value)}
            placeholder="https://example.com/avatar.png"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowTeamDialog(false)}>Cancel</Button>
          <Button onClick={saveTeam} variant="contained">{editMode ? 'Update' : 'Create'}</Button>
        </DialogActions>
      </MuiDialog>

      {/* Project Dialog */}
      <MuiDialog open={showProjectDialog} onClose={() => setShowProjectDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editMode ? 'Edit Project' : 'Add Project'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Project Name"
            fullWidth
            variant="outlined"
            value={projectFormData.name}
            onChange={(e) => handleProjectFormChange('name', e.target.value)}
            required
            sx={{ mb: 2, mt: 1 }}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            variant="outlined"
            value={projectFormData.description}
            onChange={(e) => handleProjectFormChange('description', e.target.value)}
            multiline
            rows={3}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Repository URL"
            fullWidth
            variant="outlined"
            value={projectFormData.repository_url}
            onChange={(e) => handleProjectFormChange('repository_url', e.target.value)}
            required
            placeholder="https://github.com/org/repo"
            sx={{ mb: 2 }}
          />
          <FormControl fullWidth variant="outlined" margin="dense">
            <InputLabel>Programming Language</InputLabel>
            <Select
              value={projectFormData.programming_language}
              onChange={(e) => handleProjectFormChange('programming_language', e.target.value)}
              label="Programming Language"
            >
              <MenuItem value="Python">Python</MenuItem>
              <MenuItem value="JavaScript">JavaScript</MenuItem>
              <MenuItem value="TypeScript">TypeScript</MenuItem>
              <MenuItem value="Java">Java</MenuItem>
              <MenuItem value="Go">Go</MenuItem>
              <MenuItem value="C#">C#</MenuItem>
              <MenuItem value="Ruby">Ruby</MenuItem>
              <MenuItem value="PHP">PHP</MenuItem>
              <MenuItem value="Other">Other</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowProjectDialog(false)}>Cancel</Button>
          <Button onClick={saveProject} variant="contained">{editMode ? 'Update' : 'Add'}</Button>
        </DialogActions>
      </MuiDialog>

      {/* Member Dialog */}
      <MuiDialog open={showMemberDialog} onClose={() => setShowMemberDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Team Member</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Email Address"
            fullWidth
            variant="outlined"
            value={memberFormData.email}
            onChange={(e) => handleMemberFormChange('email', e.target.value)}
            required
            type="email"
            placeholder="colleague@example.com"
            sx={{ mb: 2, mt: 1 }}
          />
          <FormControl fullWidth variant="outlined" margin="dense">
            <InputLabel>Role</InputLabel>
            <Select
              value={memberFormData.role}
              onChange={(e) => handleMemberFormChange('role', e.target.value)}
              label="Role"
            >
              <MenuItem value="owner">Owner</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="member">Member</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowMemberDialog(false)}>Cancel</Button>
          <Button onClick={addMember} variant="contained">Invite</Button>
        </DialogActions>
      </MuiDialog>

      {/* Delete Confirmation Dialog */}
      <MuiDialog open={showDeleteConfirm} onClose={() => setShowDeleteConfirm(false)}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this {deleteItemType}? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDeleteConfirm(false)}>Cancel</Button>
          <Button onClick={handleDelete} color="error" variant="contained">Delete</Button>
        </DialogActions>
      </MuiDialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Collaboration;
