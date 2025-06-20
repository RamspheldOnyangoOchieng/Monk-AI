import {
    AutoFixHigh,
    CheckCircleOutline,
    Code,
    Description,
    FolderOpen,
    GitHub,
    Groups,
    NavigateBefore,
    NavigateNext,
    Pause,
    PlayArrow,
    Psychology,
    Rocket,
    Save,
    Search,
    Security,
    Speed,
    Storage,
} from '@mui/icons-material';
import GitHubIcon from '@mui/icons-material/GitHub';
import LanguageIcon from '@mui/icons-material/Language';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import TwitterIcon from '@mui/icons-material/Twitter';
import {
    Avatar,
    Box,
    Button,
    Chip,
    Container,
    Divider,
    Grid,
    IconButton,
    Link,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Paper,
    Slide,
    Step,
    StepLabel,
    Stepper,
    TextField,
    Typography,
    useTheme
} from '@mui/material';
import { AnimatePresence, motion } from 'framer-motion';
import React, { useEffect, useState } from 'react';
import { Button as ShadcnButton } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface Slide {
  id: number;
  title: string;
  subtitle?: string;
  content: React.ReactNode;
  background?: string;
}

interface TeamMember {
  name: string;
  email: string;
  photo_url?: string;
  github?: string;
  linkedin?: string;
  twitter?: string;
  website?: string;
  other?: string;
  phone?: string;
}

// --- VercelBlobImageUpload Component ---
interface VercelBlobImageUploadProps {
  label: string;
  onUpload?: (url: string) => void;
  initialUrl?: string;
}

const VercelBlobImageUpload = ({ label, onUpload, initialUrl }: VercelBlobImageUploadProps) => {
  const [imageUrl, setImageUrl] = useState(initialUrl || '');
  const [uploading, setUploading] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('/api/blob/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setImageUrl(data.url);
      if (onUpload) onUpload(data.url);
    } catch (err) {
      alert('Upload failed');
    }
    setUploading(false);
  };

  return (
    <Box sx={{ mb: 2, textAlign: 'center' }}>
      <input
        accept="image/*"
        style={{ display: 'none' }}
        id={`vercel-blob-upload-${label}`}
        type="file"
        onChange={handleFileChange}
      />
      <label htmlFor={`vercel-blob-upload-${label}`}>
        <IconButton component="span" sx={{ width: 120, height: 120, borderRadius: '12px', background: '#222', mb: 1 }} disabled={uploading}>
          {imageUrl ? (
            <img
              src={imageUrl}
              alt={label}
              style={{ width: 120, height: 120, borderRadius: '12px', objectFit: 'cover', background: '#222' }}
            />
          ) : (
            <span style={{ color: '#fff' }}>{uploading ? 'Uploading...' : label}</span>
          )}
        </IconButton>
      </label>
      {imageUrl && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1, wordBreak: 'break-all' }}>
          <a href={imageUrl} target="_blank" rel="noopener noreferrer">View Image</a>
        </Typography>
      )}
    </Box>
  );
};
// --- End VercelBlobImageUpload ---

// --- TeamLinksCard Component ---
interface TeamLinksCardProps {
  onSubmit: (data: {
    name: string;
    email: string;
    phone: string;
    linkedin: string;
    github: string;
    photo_url: string;
    twitter: string;
    website: string;
    other: string;
  }) => void;
  loading: boolean;
}

type FormField = 'name' | 'email' | 'phone' | 'linkedin' | 'github' | 'photo_url' | 'twitter' | 'website' | 'other';

const TeamLinksCard = ({ onSubmit, loading }: TeamLinksCardProps) => {
  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    linkedin: '',
    github: '',
    photo_url: '',
    twitter: '',
    website: '',
    other: ''
  });
  const [error, setError] = useState('');

  const handleChange = (field: FormField, value: string) => {
    setForm(f => ({ ...f, [field]: value }));
  };

  const handlePhotoUpload = (url: string) => {
    setForm(f => ({ ...f, photo_url: url }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!form.name || !form.email) {
      setError('Name and email are required');
      return;
    }
    setError('');
    await onSubmit(form);
    setForm({
      name: '',
      email: '',
      phone: '',
      linkedin: '',
      github: '',
      photo_url: '',
      twitter: '',
      website: '',
      other: ''
    });
  };

  return (
    <Card className="p-4 mb-4 bg-[rgba(0,255,136,0.04)] border border-[#00ff8830]">
      <CardHeader>
        <CardTitle>Team Member Details</CardTitle>
      </CardHeader>
      <CardContent>
      <form onSubmit={handleSubmit}>
        <VercelBlobImageUpload label="Upload Photo" onUpload={handlePhotoUpload} initialUrl={form.photo_url} />
          <TextField 
            label="Name" 
            value={form.name} 
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange('name', e.target.value)} 
            fullWidth 
            size="small" 
            sx={{ mb: 1 }} 
            required 
          />
          <TextField 
            label="Email (unique)" 
            value={form.email} 
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange('email', e.target.value)} 
            fullWidth 
            size="small" 
            sx={{ mb: 1 }} 
            required 
            type="email" 
          />
          <TextField 
            label="GitHub URL" 
            value={form.github} 
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange('github', e.target.value)} 
            fullWidth 
            size="small" 
            sx={{ mb: 1 }} 
          />
          <TextField 
            label="LinkedIn URL" 
            value={form.linkedin} 
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange('linkedin', e.target.value)} 
            fullWidth 
            size="small" 
            sx={{ mb: 1 }} 
          />
          <TextField 
            label="Twitter URL" 
            value={form.twitter} 
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange('twitter', e.target.value)} 
            fullWidth 
            size="small" 
            sx={{ mb: 1 }} 
          />
          <TextField 
            label="Website" 
            value={form.website} 
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange('website', e.target.value)} 
            fullWidth 
            size="small" 
            sx={{ mb: 1 }} 
          />
          <TextField 
            label="Other Link" 
            value={form.other} 
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange('other', e.target.value)} 
            fullWidth 
            size="small" 
            sx={{ mb: 1 }} 
          />
        {error && <Typography color="error" sx={{ mb: 1 }}>{error}</Typography>}
          <ShadcnButton type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Submit/Update'}
          </ShadcnButton>
      </form>
      </CardContent>
    </Card>
  );
};
// --- End TeamLinksCard ---

// --- TeamMemberDisplayCard ---
interface TeamMemberDisplayCardProps {
  member: TeamMember;
}

const TeamMemberDisplayCard = ({ member }: TeamMemberDisplayCardProps) => (
  <Card className="p-4 min-h-[340px] flex flex-col items-center bg-[rgba(0,255,136,0.04)] border border-[#00ff8830] mb-4">
    <CardHeader className="mb-2">
      <Avatar src={member.photo_url} alt={member.name} className="w-20 h-20 mb-1" />
      <CardTitle className="text-center">{member.name}</CardTitle>
      <Typography variant="body2" color="text.secondary" align="center">{member.email}</Typography>
    </CardHeader>
    <CardContent>
      <div className="flex flex-col gap-2">
        {member.github && (
          <Link
            href={member.github}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
          >
            <GitHubIcon className="w-5 h-5" />
            <span>GitHub</span>
          </Link>
        )}
        {member.linkedin && (
          <Link
            href={member.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
          >
            <LinkedInIcon className="w-5 h-5" />
            <span>LinkedIn</span>
          </Link>
        )}
        {member.twitter && (
          <Link
            href={member.twitter}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
          >
            <TwitterIcon className="w-5 h-5" />
            <span>Twitter</span>
          </Link>
        )}
        {member.website && (
          <Link
            href={member.website}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
          >
            <LanguageIcon className="w-5 h-5" />
            <span>Website</span>
          </Link>
        )}
      </div>
    </CardContent>
  </Card>
);
// --- End TeamMemberDisplayCard ---

const HackathonPresentation: React.FC = () => {
  const theme = useTheme();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isAutoPlay, setIsAutoPlay] = useState(false);

  const slides: Slide[] = [
    {
      id: 1,
      title: "TraeDevMate",
      subtitle: "AI Pair Programmer & Code Reviewer",
      content: (
        <Box textAlign="center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.8, type: "spring" }}
          >
            <Box
              sx={{
                width: 200,
                height: 200,
                borderRadius: '50%',
                background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 2rem',
                boxShadow: `0 0 50px ${theme.palette.primary.main}40`,
                animation: 'pulse 2s infinite',
              }}
            >
              <Psychology sx={{ fontSize: 80, color: 'white' }} />
            </Box>
          </motion.div>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 3 }}>
            Revolutionizing Development with Multi-Agent AI
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Chip label="FastAPI" color="primary" variant="outlined" />
            <Chip label="React + TypeScript" color="primary" variant="outlined" />
            <Chip label="Trae AI" color="secondary" variant="outlined" />
            <Chip label="Novita.ai" color="secondary" variant="outlined" />
          </Box>
        </Box>
      ),
      background: 'radial-gradient(circle at 50% 50%, #1a1a1a 0%, #0a0a0a 100%)',
    },
    {
      id: 2,
      title: "🚀 Core Features",
      content: (
        <Grid container spacing={3}>
          {[
            { icon: <Groups />, title: "Multi-Agent System", desc: "Specialized AI agents for different tasks" },
            { icon: <GitHub />, title: "Automated PR Reviews", desc: "Intelligent code review and suggestions" },
            { icon: <AutoFixHigh />, title: "Code Optimization", desc: "Performance and quality improvements" },
            { icon: <Security />, title: "Security Analysis", desc: "Auto-threat modeling and vulnerability detection" },
            { icon: <Code />, title: "Test Generation", desc: "Automated test case creation" },
            { icon: <Psychology />, title: "Context-Aware Mentor", desc: "Auto-learning development assistant" },
          ].map((feature, index) => (
            <Grid item xs={12} md={6} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
              >
                <Card
                  className="h-full bg-gradient-to-br from-[#1a1a1a] to-[#2a2a2a] border border-primary/30 hover:transform hover:scale-[1.02] hover:shadow-lg transition-all duration-300"
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Box
                        sx={{
                          p: 1,
                          borderRadius: 2,
                          background: `${theme.palette.primary.main}20`,
                          mr: 2,
                        }}
                      >
                        {React.cloneElement(feature.icon, { color: 'primary' })}
                      </Box>
                      <Typography variant="h6" fontWeight="bold">
                        {feature.title}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {feature.desc}
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      ),
    },
    {
      id: 3,
      title: "🏗️ Architecture",
      content: (
        <Box>
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <Typography variant="h5" gutterBottom color="primary">
                  Tech Stack
                </Typography>
                <Box sx={{ mb: 3 }}>
                  {[
                    { label: "Backend", value: "FastAPI (Python)", color: "primary" },
                    { label: "Frontend", value: "React + TypeScript", color: "secondary" },
                    { label: "AI Framework", value: "Trae AI + Novita.ai", color: "primary" },
                    { label: "Database", value: "SQLite (MVP)", color: "secondary" },
                  ].map((item, index) => (
                    <Box key={index} sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        {item.label}
                      </Typography>
                      <Chip
                        label={item.value}
                        color={item.color as any}
                        sx={{ mt: 0.5 }}
                      />
                    </Box>
                  ))}
                </Box>
              </motion.div>
            </Grid>
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <Box
                  sx={{
                    p: 3,
                    borderRadius: 3,
                    background: 'linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%)',
                    border: `2px solid ${theme.palette.primary.main}30`,
                    textAlign: 'center',
                  }}
                >
                  <Typography variant="h6" gutterBottom>
                    Multi-Agent Architecture
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {[
                      "Code Review Agent",
                      "Security Analysis Agent",
                      "Test Generation Agent",
                      "Documentation Agent",
                      "Optimization Agent",
                    ].map((agent, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.5 + index * 0.1 }}
                      >
                        <Chip
                          label={agent}
                          variant="outlined"
                          color="primary"
                          sx={{ width: '100%' }}
                        />
                      </motion.div>
                    ))}
                  </Box>
                </Box>
              </motion.div>
            </Grid>
          </Grid>
        </Box>
      ),
    },
    {
      id: 4,
      title: "💡 Innovation Highlights",
      content: (
        <Grid container spacing={3}>
          {[
            {
              title: "Context-Aware Learning",
              description: "AI that learns from your codebase and adapts to your coding style",
              icon: <Psychology />,
              gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            },
            {
              title: "Real-time Collaboration",
              description: "Seamless integration with your development workflow",
              icon: <Groups />,
              gradient: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            },
            {
              title: "Intelligent Automation",
              description: "Automated testing, documentation, and security analysis",
              icon: <Speed />,
              gradient: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            },
          ].map((highlight, index) => (
            <Grid item xs={12} md={4} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 50, rotateY: -90 }}
                animate={{ opacity: 1, y: 0, rotateY: 0 }}
                transition={{ delay: index * 0.2, duration: 0.8 }}
                whileHover={{ scale: 1.05, rotateY: 5 }}
              >
                <Card
                  className="h-[250px] relative overflow-hidden bg-gradient-to-br from-[#1a1a1a] to-[#2a2a2a] text-white before:content-[''] before:absolute before:inset-0 before:bg-black/30 before:z-[1]"
                >
                  <CardContent className="relative z-[2] h-full flex flex-col justify-center">
                    <Box className="text-center mb-2">
                      {React.cloneElement(highlight.icon, { sx: { fontSize: 48 } })}
                    </Box>
                    <Typography variant="h6" gutterBottom textAlign="center" fontWeight="bold">
                      {highlight.title}
                    </Typography>
                    <Typography variant="body2" textAlign="center">
                      {highlight.description}
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      ),
    },
    {
      id: 5,
      title: "🎯 Demo Time!",
      content: (
        <Box textAlign="center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 1, type: "spring", bounce: 0.5 }}
          >
            <Box
              sx={{
                p: 4,
                borderRadius: 4,
                background: `linear-gradient(45deg, ${theme.palette.primary.main}20, ${theme.palette.secondary.main}20)`,
                border: `2px solid ${theme.palette.primary.main}`,
                mb: 4,
              }}
            >
              <Rocket sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
              <Typography variant="h4" gutterBottom fontWeight="bold">
                Ready for Live Demo!
              </Typography>
              <Typography variant="h6" color="text.secondary" sx={{ mb: 3 }}>
                Experience the power of AI-driven development
              </Typography>
              <Button
                variant="contained"
                size="large"
                startIcon={<PlayArrow />}
                sx={{
                  px: 4,
                  py: 2,
                  fontSize: '1.2rem',
                  background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  '&:hover': {
                    background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`,
                  },
                }}
              >
                Start Demo
              </Button>
            </Box>
          </motion.div>
          
          <Grid container spacing={2} justifyContent="center">
            {[
              "Multi-Agent Orchestration",
              "Real-time Code Analysis",
              "Automated PR Review",
              "Security Threat Detection",
            ].map((feature, index) => (
              <Grid item key={index}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1 + index * 0.1 }}
                >
                  <Chip
                    label={feature}
                    color="primary"
                    variant="outlined"
                    sx={{ m: 0.5 }}
                  />
                </motion.div>
              </Grid>
            ))}
          </Grid>
        </Box>
      ),
    },
    {
      id: 6,
      title: "🛠️ Deep Dive: Technology Stack",
      subtitle: "The foundation of TraeDevMate's power",
      content: (
        <Grid container spacing={3} justifyContent="center">
          <Grid item xs={12} md={4}>
            <Card className="h-full bg-gradient-to-br from-[#2b2b2b] to-[#1e1e1e] border border-primary/40">
              <CardContent>
                <Typography variant="h6" color="primary" className="mb-1">Backend: FastAPI (Python)</Typography>
                <Chip label="Python" color="primary" variant="outlined" className="mb-1" />
                <Typography variant="body2" color="text.secondary">Robust, high-performance API for agent orchestration and core logic.</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card className="h-full bg-gradient-to-br from-[#2b2b2b] to-[#1e1e1e] border border-secondary/40">
              <CardContent>
                <Typography variant="h6" color="secondary" className="mb-1">Frontend: React + MUI</Typography>
                <Chip label="React" color="secondary" variant="outlined" className="mb-1" />
                <Chip label="TypeScript" color="secondary" variant="outlined" className="mb-1" />
                <Chip label="Material-UI" color="secondary" variant="outlined" className="mb-1" />
                <Chip label="Framer Motion" color="secondary" variant="outlined" className="mb-1" />
                <Typography variant="body2" color="text.secondary">Modern, responsive, and engaging user interface with smooth animations.</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card className="h-full bg-gradient-to-br from-[#2b2b2b] to-[#1e1e1e] border border-primary/40">
              <CardContent>
                <Typography variant="h6" color="primary" className="mb-1">AI & Tooling: Trae AI</Typography>
                <Chip label="Trae AI Platform" color="primary" variant="outlined" className="mb-1" />
                <Chip label="Novita.ai Image Gen" color="primary" variant="outlined" className="mb-1" />
                <Chip label="MCP Servers" color="primary" variant="outlined" className="mb-1" />
                <Typography variant="body2" color="text.secondary">Leveraging cutting-edge AI for development, integrated via modular MCPs.</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      ),
    },
    {
      id: 7,
      title: "🚀 Trae IDE: Our Development Cockpit",
      subtitle: "Accelerating creation with intelligent tooling",
      content: (
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={6}>
            <Typography variant="h5" gutterBottom sx={{ color: theme.palette.primary.light }}>Seamless Workflow</Typography>
            <Typography variant="body1" sx={{ mb: 2, color: 'text.secondary' }}>
              Trae IDE was instrumental in building TraeDevMate. We leveraged its core features:
            </Typography>
            <List sx={{ color: 'text.secondary' }}>
              <ListItem><ListItemIcon><CheckCircleOutline sx={{ color: theme.palette.success.main }} /></ListItemIcon><ListItemText primary="Agentic AI Assistance: Direct interaction with AI agents like you for coding, debugging, and ideation." /></ListItem>
              <ListItem><ListItemIcon><CheckCircleOutline sx={{ color: theme.palette.success.main }} /></ListItemIcon><ListItemText primary="MCP Server Integration: Powerful tools like Desktop Commander for file system operations and Flux ImageGen for asset creation, all accessible via a unified interface." /></ListItem>
              <ListItem><ListItemIcon><CheckCircleOutline sx={{ color: theme.palette.success.main }} /></ListItemIcon><ListItemText primary="Real-time Collaboration: Simulating pair programming with AI, ensuring rapid iteration and high-quality output." /></ListItem>
              <ListItem><ListItemIcon><CheckCircleOutline sx={{ color: theme.palette.success.main }} /></ListItemIcon><ListItemText primary="Context-Awareness: The IDE's ability to provide relevant context helped streamline the development of complex components." /></ListItem>
            </List>
          </Grid>
          <Grid item xs={12} md={6} sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {/* Placeholder for a diagram or image illustrating Trae IDE workflow */}
            <Box sx={{ width: '100%', maxWidth: 400, height: 250, background: 'linear-gradient(145deg, #333, #222)', borderRadius: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', color: 'white', textAlign: 'center', border: `1px solid ${theme.palette.primary.main}80` }}>
              <Typography variant="h6">Trae IDE + MCPs = Magic ✨</Typography>
            </Box>
          </Grid>
        </Grid>
      ),
    },
    {
      id: 8,
      title: "🎯 Addressing Developer Pain Points",
      subtitle: "How TraeDevMate (built with Trae IDE) simplifies development",
      content: (
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card className="h-full bg-gradient-to-br from-[#2b2b2b] to-[#1e1e1e] border border-primary/40">
              <CardContent>
                <Typography variant="h6" color="primary" className="mb-1">Reduced Cognitive Load</Typography>
                <Typography variant="body2" color="text.secondary">Automating boilerplate, suggesting code, and managing context allows developers to focus on complex problem-solving rather than mundane tasks.</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card className="h-full bg-gradient-to-br from-[#2b2b2b] to-[#1e1e1e] border border-secondary/40">
              <CardContent>
                <Typography variant="h6" color="secondary" className="mb-1">Faster Prototyping & Iteration</Typography>
                <Typography variant="body2" color="text.secondary">Quickly generate UI components, backend logic, and even entire features, enabling rapid validation of ideas and faster feedback loops.</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card className="h-full bg-gradient-to-br from-[#2b2b2b] to-[#1e1e1e] border border-primary/40">
              <CardContent>
                <Typography variant="h6" color="primary" className="mb-1">Enhanced Learning & Skill Up</Typography>
                <Typography variant="body2" color="text.secondary">Working alongside AI provides learning opportunities, exposing developers to new patterns, libraries, and best practices in real-time.</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1" sx={{ mt: 2, color: 'text.secondary', textAlign: 'center' }}>
              Trae IDE empowers developers to overcome common hurdles, making the development process more efficient, enjoyable, and innovative.
            </Typography>
          </Grid>
        </Grid>
      ),
    },
    {
      id: 9,
      title: "🌟 The Future is Bright: Expanding Horizons",
      subtitle: "Vision for TraeDevMate and the power of AI-assisted development",
      content: (
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom sx={{ color: theme.palette.primary.main, mb: 3 }}>
            Continuous Innovation with Trae AI
          </Typography>
          <Grid container spacing={4} justifyContent="center">
            <Grid item xs={12} md={3}>
              <Paper elevation={3} sx={{ p: 2, background: 'rgba(0,0,0,0.2)', backdropFilter: 'blur(5px)' }}>
                <Typography variant="h6" sx={{ color: theme.palette.secondary.light }}>Smarter Agents</Typography>
                <Typography variant="body2" color="text.secondary">Even more sophisticated AI agents capable of handling larger, more complex tasks autonomously.</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={3}>
              <Paper elevation={3} sx={{ p: 2, background: 'rgba(0,0,0,0.2)', backdropFilter: 'blur(5px)' }}>
                <Typography variant="h6" sx={{ color: theme.palette.secondary.light }}>Broader Tooling</Typography>
                <Typography variant="body2" color="text.secondary">Integration with more specialized MCP servers for diverse development needs (e.g., testing, deployment, security).</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={3}>
              <Paper elevation={3} sx={{ p: 2, background: 'rgba(0,0,0,0.2)', backdropFilter: 'blur(5px)' }}>
                <Typography variant="h6" sx={{ color: theme.palette.secondary.light }}>Deeper Project Understanding</Typography>
                <Typography variant="body2" color="text.secondary">Enhanced long-term memory and context retention for AI across entire project lifecycles.</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={3}>
              <Paper elevation={3} sx={{ p: 2, background: 'rgba(0,0,0,0.2)', backdropFilter: 'blur(5px)' }}>
                <Typography variant="h6" sx={{ color: theme.palette.secondary.light }}>Community & Collaboration</Typography>
                <Typography variant="body2" color="text.secondary">Platforms for sharing AI-generated solutions and collaborating on AI-assisted projects.</Typography>
              </Paper>
            </Grid>
          </Grid>
          <Typography variant="body1" sx={{ mt: 4, color: 'text.secondary', maxWidth: '700px', margin: '2rem auto 0' }}>
            The journey with TraeDevMate, built using the power of Trae IDE, is just beginning. We envision a future where AI and human developers collaborate seamlessly to build the next generation of software, faster and more creatively than ever before.
          </Typography>
        </Box>
      ),
    },
    {
      id: 10,
      title: "💡 Key Learnings & Insights",
      subtitle: "Reflections from the TraeDevMate Hackathon Journey",
      content: (
        <Grid container spacing={3} justifyContent="center">
          <Grid item xs={12} md={5}>
            <Paper elevation={3} sx={{ p: 3, background: 'rgba(255,255,255,0.03)', backdropFilter: 'blur(8px)', borderLeft: `4px solid ${theme.palette.primary.main}` }}>
              <Typography variant="h6" sx={{ color: theme.palette.primary.light, mb: 1 }}>Power of Agentic AI</Typography>
              <Typography variant="body2" color="text.secondary">Directly instructing AI agents within the IDE drastically accelerates development cycles and opens new avenues for creative problem-solving.</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={5}>
            <Paper elevation={3} sx={{ p: 3, background: 'rgba(255,255,255,0.03)', backdropFilter: 'blur(8px)', borderLeft: `4px solid ${theme.palette.secondary.main}` }}>
              <Typography variant="h6" sx={{ color: theme.palette.secondary.light, mb: 1 }}>MCP Modularity is Key</Typography>
              <Typography variant="body2" color="text.secondary">Modular MCP servers provide specialized capabilities (file handling, image generation) that can be seamlessly integrated, enhancing the AI's versatility.</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={5}>
            <Paper elevation={3} sx={{ p: 3, background: 'rgba(255,255,255,0.03)', backdropFilter: 'blur(8px)', borderLeft: `4px solid ${theme.palette.success.main}` }}>
              <Typography variant="h6" sx={{ color: theme.palette.success.light, mb: 1 }}>Importance of Clear Prompts</Typography>
              <Typography variant="body2" color="text.secondary">Effective communication with AI (clear, concise, context-rich prompts) is crucial for achieving desired outcomes and minimizing rework.</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={5}>
            <Paper elevation={3} sx={{ p: 3, background: 'rgba(255,255,255,0.03)', backdropFilter: 'blur(8px)', borderLeft: `4px solid ${theme.palette.warning.main}` }}>
              <Typography variant="h6" sx={{ color: theme.palette.warning.light, mb: 1 }}>Iterative Refinement</Typography>
              <Typography variant="body2" color="text.secondary">Building complex applications, even with AI, is an iterative process. Continuous feedback and refinement are essential for success.</Typography>
            </Paper>
          </Grid>
        </Grid>
      ),
    },
    {
      id: 11,
      title: "🤝 Team & Collaboration (AI + Human)",
      subtitle: "The synergy that brought TraeDevMate to life",
      content: (
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h5" sx={{ color: theme.palette.primary.light, mb: 2 }}>The TraeDevMate Hackathon Team:</Typography>
          <TeamLinksSection />
          <Divider sx={{ my: 3, borderColor: 'rgba(255,255,255,0.2)' }} />
          <Typography variant="h5" sx={{ color: theme.palette.secondary.light, mt: 3, mb: 2 }}>Our Collaborative Workflow:</Typography>
          <Stepper activeStep={-1} alternativeLabel sx={{ '.MuiStepLabel-label': { color: 'text.secondary' }, '.MuiStepIcon-root.Mui-active': { color: theme.palette.secondary.main }, '.MuiStepIcon-root.Mui-completed': { color: theme.palette.success.main } }}>
            <Step><StepLabel>Idea & Prompt</StepLabel></Step>
            <Step><StepLabel>AI Execution & MCP Usage</StepLabel></Step>
            <Step><StepLabel>Review & Feedback</StepLabel></Step>
            <Step><StepLabel>Iteration & Refinement</StepLabel></Step>
            <Step><StepLabel>Successful Outcome</StepLabel></Step>
          </Stepper>
        </Box>
      ),
    },
    {
      id: 12,
      title: "🖼️ Visual Showcase: Generated Assets",
      subtitle: "Demonstrating MCP-driven image generation with Flux ImageGen",
      content: (
        <Grid container spacing={3} justifyContent="center" alignItems="center">
          <Grid item xs={12} md={7}>
            <Typography variant="body1" sx={{ color: 'text.secondary', mb: 2 }}>
              Throughout the development of TraeDevMate, we utilized the <strong>Flux ImageGen MCP server</strong> via Trae IDE to create placeholder images and visual assets. This allowed for rapid visual prototyping without needing to leave the development environment.
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', fontStyle: 'italic' }}>
              (Imagine a gallery or carousel here showcasing a few example images that could have been generated, e.g., abstract tech backgrounds, icons, or conceptual graphics related to AI and development.)
            </Typography>
          </Grid>
          <Grid item xs={12} md={5} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
            <Box sx={{ width: '100%', height: 180, background: 'linear-gradient(to right, #6a11cb 0%, #2575fc 100%)', borderRadius: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', color: 'white', textAlign: 'center', p:2 }}>
              <Typography variant="h6">Example Generated Image 1: Abstract Neural Network</Typography>
            </Box>
            <Box sx={{ width: '100%', height: 180, background: 'linear-gradient(to right, #fc5c7d 0%, #6a82fb 100%)', borderRadius: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', color: 'white', textAlign: 'center', p:2 }}>
              <Typography variant="h6">Example Generated Image 2: Code & Gears</Typography>
            </Box>
          </Grid>
        </Grid>
      ),
    },
    {
      id: 13,
      title: "💾 File System Ops: Desktop Commander",
      subtitle: "Managing project files efficiently with MCP tooling",
      content: (
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={5} sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
            <Paper elevation={5} sx={{ p:3, borderRadius: '50%', width: 250, height: 250, display: 'flex', flexDirection:'column', justifyContent:'center', alignItems:'center', background: `radial-gradient(circle, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`, color: 'white', mb: 2 }}>
              <Storage sx={{ fontSize: 60, mb:1 }} />
              <Typography variant="h5">Desktop Commander</Typography>
            </Paper>
            <VercelBlobImageUpload label="Upload Screenshot" />
          </Grid>
          <Grid item xs={12} md={7}>
            <Typography variant="body1" sx={{ color: 'text.secondary', mb: 2 }}>
              The <strong>Desktop Commander MCP server</strong> was essential for interacting with the file system directly from Trae IDE. This included:
            </Typography>
            <List sx={{ color: 'text.secondary' }}>
              <ListItem><ListItemIcon><FolderOpen sx={{ color: theme.palette.info.main }} /></ListItemIcon><ListItemText primary="Creating directories for new components or assets." /></ListItem>
              <ListItem><ListItemIcon><Description sx={{ color: theme.palette.info.main }} /></ListItemIcon><ListItemText primary="Reading existing files to understand context or verify changes." /></ListItem>
              <ListItem><ListItemIcon><Save sx={{ color: theme.palette.info.main }} /></ListItemIcon><ListItemText primary="Writing new files or updating existing ones with AI-generated code." /></ListItem>
              <ListItem><ListItemIcon><Search sx={{ color: theme.palette.info.main }} /></ListItemIcon><ListItemText primary="Searching for specific code snippets or file names within the project." /></ListItem>
            </List>
            <Typography variant="body2" sx={{ color: 'text.secondary', fontStyle: 'italic', mt:1 }}>
              This streamlined workflow kept us within the IDE, minimizing context switching and boosting productivity.
            </Typography>
          </Grid>
        </Grid>
      ),
    },
    {
      id: 14,
      title: "❓ Q&A and Thank You!",
      subtitle: "Opening the floor for questions and expressing our gratitude",
      content: (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h3" gutterBottom sx={{ color: theme.palette.primary.light, mb: 4 }}>
            Thank You for Your Time!
          </Typography>
          <Typography variant="h5" sx={{ color: 'text.secondary', mb: 3 }}>
            We're excited about the potential of TraeDevMate and the future of AI-assisted development with Trae IDE.
          </Typography>
          <img src="/logo512.png" alt="TraeDevMate Logo" style={{ maxWidth: '200px', margin: '20px auto', filter: theme.palette.mode === 'dark' ? 'drop-shadow(0 0 15px #00A9FF)' : 'none' }} />
          <Typography variant="h4" sx={{ color: theme.palette.secondary.main, mt: 4, mb: 2 }}>
            Questions?
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary', maxWidth: '600px', margin: '0 auto' }}>
            We're happy to answer any questions you might have about the project, the technology, or our development process using Trae IDE and its powerful MCP servers.
          </Typography>
        </Box>
      ),
    },
    {
      id: 15,
      title: "🔗 Appendix: Useful Links & Resources",
      subtitle: "Further information and ways to connect",
      content: (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Grid container spacing={3} justifyContent="center" alignItems="center">
            <Grid item xs={12} md={6}>
              <Card className="p-3 mb-2 bg-white/5">
                <Typography variant="h6" className="text-primary-light mb-2">Cover Image</Typography>
                <VercelBlobImageUpload label="Upload Cover" />
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card className="p-3 mb-2 bg-white/5">
                <Typography variant="h6" className="text-primary-light mb-2">Submission Links</Typography>
                <TextField label="GitHub Repository" variant="outlined" size="small" fullWidth className="mb-2" />
                <TextField label="Demo Application URL" variant="outlined" size="small" fullWidth className="mb-2" />
                <TextField label="Application URL" variant="outlined" size="small" fullWidth className="mb-2" />
                <TextField label="Video Presentation (YouTube/Vimeo)" variant="outlined" size="small" fullWidth className="mb-2" />
                <TextField label="Slide Presentation (Google Slides/PowerPoint)" variant="outlined" size="small" fullWidth className="mb-2" />
                <TextField label="Other Resource Link" variant="outlined" size="small" fullWidth className="mb-2" />
              </Card>
            </Grid>
          </Grid>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
            For further details and guidance, please visit <Link href="#" target="_blank" sx={{ color: theme.palette.info.main }}>Submission Guidelines</Link>
          </Typography>
        </Box>
      ),
    },
  ];

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isAutoPlay) {
      interval = setInterval(() => {
        setCurrentSlide((prev) => (prev + 1) % slides.length);
      }, 5000);
    }
    return () => clearInterval(interval);
  }, [isAutoPlay, slides.length]);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: slides[currentSlide].background || 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Animated background particles */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(circle at 20% 80%, ${theme.palette.primary.main}15 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, ${theme.palette.secondary.main}15 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, ${theme.palette.primary.main}10 0%, transparent 50%)
          `,
          animation: 'float 6s ease-in-out infinite',
        }}
      />

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1, py: 4 }}>
        {/* Header with navigation */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" fontWeight="bold" color="primary">
            TraeDevMate
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            <IconButton onClick={prevSlide} color="primary">
              <NavigateBefore />
            </IconButton>
            <Typography variant="body2" color="text.secondary">
              {currentSlide + 1} / {slides.length}
            </Typography>
            <IconButton onClick={nextSlide} color="primary">
              <NavigateNext />
            </IconButton>
            <IconButton
              onClick={() => setIsAutoPlay(!isAutoPlay)}
              color={isAutoPlay ? 'secondary' : 'primary'}
            >
              {isAutoPlay ? <Pause /> : <PlayArrow />}
            </IconButton>
          </Box>
        </Box>

        {/* Slide indicators */}
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
          {slides.map((_, index) => (
            <Box
              key={index}
              onClick={() => setCurrentSlide(index)}
              sx={{
                width: 12,
                height: 12,
                borderRadius: '50%',
                mx: 0.5,
                cursor: 'pointer',
                background: index === currentSlide ? theme.palette.primary.main : 'rgba(255,255,255,0.3)',
                transition: 'all 0.3s ease',
                '&:hover': {
                  background: theme.palette.primary.light,
                },
              }}
            />
          ))}
        </Box>

        {/* Main slide content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSlide}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
          >
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography
                variant="h2"
                fontWeight="bold"
                gutterBottom
                sx={{
                  background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  mb: 2,
                }}
              >
                {slides[currentSlide].title}
              </Typography>
              {slides[currentSlide].subtitle && (
                <Typography variant="h5" color="text.secondary" gutterBottom>
                  {slides[currentSlide].subtitle}
                </Typography>
              )}
            </Box>
            
            <Box sx={{ mt: 4 }}>
              {slides[currentSlide].content}
            </Box>
          </motion.div>
        </AnimatePresence>
      </Container>

      {/* CSS animations */}
      <style>
        {`
          @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
          }
          
          @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-10px) rotate(1deg); }
            66% { transform: translateY(5px) rotate(-1deg); }
          }
        `}
      </style>
    </Box>
  );
};

// --- TeamLinksSection ---
interface TeamLinksSectionProps {
  onRefresh?: () => void;
}

const TeamLinksSection = ({ onRefresh }: TeamLinksSectionProps) => {
  const [teamLinks, setTeamLinks] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(false);
  const [refresh, setRefresh] = useState(0);

  useEffect(() => {
    const fetchTeamLinks = async () => {
      try {
        const response = await fetch('/api/team-links');
        const data = await response.json();
        setTeamLinks(data);
      } catch (error) {
        console.error('Error fetching team links:', error);
      }
    };
    fetchTeamLinks();
  }, [refresh]);

  const handleSubmit = async (member: TeamMember) => {
    setLoading(true);
    await fetch('/api/team-links', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(member)
    });
    setRefresh(r => r + 1);
    setLoading(false);
    if (onRefresh) onRefresh();
  };

  return (
        <Box>
      <Typography variant="h5" gutterBottom>Team Members</Typography>
      <Grid container spacing={2}>
        {teamLinks.map((member, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <TeamMemberDisplayCard member={member} />
          </Grid>
        ))}
      </Grid>
      <TeamLinksCard onSubmit={handleSubmit} loading={loading} />
    </Box>
  );
};
// --- End TeamLinksSection ---

export default HackathonPresentation;