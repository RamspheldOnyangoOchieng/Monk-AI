import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Tabs,
  Tab,
  IconButton,
  Tooltip,
  Card,
  CardContent,
  Chip,
  Button,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider
} from '@mui/material';
import {
  ContentCopy as CopyIcon,
  PlayArrow as RunIcon,
  Download as DownloadIcon,
  Code as CodeIcon,
  Visibility as PreviewIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodeFile {
  filename: string;
  content: string;
  language: string;
  description?: string;
}

interface CodePreviewProps {
  files: Record<string, string>;
  title?: string;
  language?: string;
}

const getLanguageFromFilename = (filename: string): string => {
  const extension = filename.split('.').pop()?.toLowerCase();
  const languageMap: Record<string, string> = {
    'py': 'python',
    'js': 'javascript',
    'ts': 'typescript',
    'tsx': 'typescript',
    'jsx': 'javascript',
    'java': 'java',
    'cpp': 'cpp',
    'c': 'c',
    'cs': 'csharp',
    'go': 'go',
    'rs': 'rust',
    'php': 'php',
    'rb': 'ruby',
    'sql': 'sql',
    'json': 'json',
    'yaml': 'yaml',
    'yml': 'yaml',
    'xml': 'xml',
    'html': 'html',
    'css': 'css',
    'scss': 'scss',
    'md': 'markdown',
    'txt': 'text',
    'dockerfile': 'dockerfile',
    'sh': 'bash'
  };
  return languageMap[extension || ''] || 'text';
};

const getFileIcon = (filename: string): string => {
  if (filename.includes('main') || filename.includes('app')) return '🚀';
  if (filename.includes('model')) return '📊';
  if (filename.includes('database') || filename.includes('db')) return '🗄️';
  if (filename.includes('test')) return '🧪';
  if (filename.includes('config')) return '⚙️';
  if (filename.includes('requirements') || filename.includes('package')) return '📦';
  if (filename.includes('README') || filename.includes('readme')) return '📖';
  if (filename.includes('.py')) return '🐍';
  if (filename.includes('.js') || filename.includes('.ts')) return '⚡';
  if (filename.includes('.json')) return '📄';
  return '📝';
};

const CodePreview: React.FC<CodePreviewProps> = ({ files, title = "Generated Code", language = "python" }) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [viewMode, setViewMode] = useState<'code' | 'preview'>('code');
  const [copiedFile, setCopiedFile] = useState<string | null>(null);

  const fileEntries = Object.entries(files || {});
  const codeFiles: CodeFile[] = fileEntries.map(([filename, content]) => ({
    filename,
    content,
    language: getLanguageFromFilename(filename),
    description: getFileDescription(filename)
  }));

  function getFileDescription(filename: string): string {
    const descriptions: Record<string, string> = {
      'main.py': 'Main application entry point with FastAPI setup',
      'models.py': 'Pydantic models for data validation',
      'database.py': 'Database operations and connection management',
      'requirements.txt': 'Python package dependencies',
      'README.md': 'Project documentation and setup instructions'
    };
    return descriptions[filename] || 'Application file';
  }

  const handleCopyCode = async (content: string, filename: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedFile(filename);
      setTimeout(() => setCopiedFile(null), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  const handleDownloadFile = (content: string, filename: string) => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadAll = () => {
    fileEntries.forEach(([filename, content]) => {
      handleDownloadFile(content, filename);
    });
  };

  const renderCodeContent = (file: CodeFile) => (
    <Box sx={{ position: 'relative' }}>
      {/* File Header */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        p: 2,
        bgcolor: 'rgba(0,0,0,0.02)',
        borderBottom: 1,
        borderColor: 'divider'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <span>{getFileIcon(file.filename)}</span>
            {file.filename}
          </Typography>
          <Chip 
            label={file.language} 
            size="small" 
            variant="outlined"
            sx={{ textTransform: 'uppercase' }}
          />
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title={copiedFile === file.filename ? "Copied!" : "Copy to clipboard"}>
            <IconButton 
              size="small" 
              onClick={() => handleCopyCode(file.content, file.filename)}
              color={copiedFile === file.filename ? "success" : "default"}
            >
              {copiedFile === file.filename ? <CheckIcon /> : <CopyIcon />}
            </IconButton>
          </Tooltip>
          <Tooltip title="Download file">
            <IconButton 
              size="small" 
              onClick={() => handleDownloadFile(file.content, file.filename)}
            >
              <DownloadIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* File Description */}
      {file.description && (
        <Alert severity="info" sx={{ m: 2, mb: 0 }}>
          {file.description}
        </Alert>
      )}

      {/* Code Content */}
      <Box sx={{ 
        maxHeight: '500px', 
        overflow: 'auto',
        '& pre': { margin: '0 !important', padding: '16px !important' }
      }}>
        <SyntaxHighlighter
          language={file.language}
          style={vscDarkPlus}
          showLineNumbers
          wrapLines
          customStyle={{
            fontSize: '14px',
            lineHeight: '1.5',
            margin: 0,
            borderRadius: 0
          }}
        >
          {file.content}
        </SyntaxHighlighter>
      </Box>
    </Box>
  );

  const renderPreviewContent = () => (
    <Card sx={{ m: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <PreviewIcon />
          Application Preview
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          This generated application includes:
        </Typography>

        <Box sx={{ mb: 3 }}>
          {fileEntries.map(([filename, content], index) => (
            <Chip
              key={index}
              label={`${getFileIcon(filename)} ${filename}`}
              variant="outlined"
              sx={{ m: 0.5 }}
            />
          ))}
        </Box>

        <Divider sx={{ my: 2 }} />

        <Typography variant="subtitle2" gutterBottom>
          🚀 Quick Start Commands:
        </Typography>
        
        <Paper sx={{ p: 2, bgcolor: 'grey.900', color: 'grey.100', mb: 2 }}>
          <Typography variant="body2" component="pre" sx={{ fontFamily: 'monospace' }}>
{`# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# View API documentation
# Navigate to: http://localhost:8000/docs`}
          </Typography>
        </Paper>

        <Alert severity="success" sx={{ mb: 2 }}>
          <Typography variant="body2">
            ✅ This application includes authentication, CRUD operations, and auto-generated API documentation.
          </Typography>
        </Alert>

        <Button
          variant="contained"
          startIcon={<RunIcon />}
          onClick={() => {
            alert('🚀 Code execution would happen here in a containerized environment!');
          }}
          sx={{ mr: 2 }}
        >
          Run Application
        </Button>

        <Button
          variant="outlined"
          startIcon={<DownloadIcon />}
          onClick={handleDownloadAll}
        >
          Download All Files
        </Button>
      </CardContent>
    </Card>
  );

  if (!files || Object.keys(files).length === 0) {
    return (
      <Alert severity="info">
        No code files generated yet. Execute a workflow to see the generated code.
      </Alert>
    );
  }

  return (
    <Paper elevation={3} sx={{ width: '100%', mt: 2 }}>
      {/* Header */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        p: 2,
        borderBottom: 1,
        borderColor: 'divider'
      }}>
        <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CodeIcon />
          {title}
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant={viewMode === 'code' ? 'contained' : 'outlined'}
            size="small"
            onClick={() => setViewMode('code')}
            startIcon={<CodeIcon />}
          >
            Code
          </Button>
          <Button
            variant={viewMode === 'preview' ? 'contained' : 'outlined'}
            size="small"
            onClick={() => setViewMode('preview')}
            startIcon={<PreviewIcon />}
          >
            Preview
          </Button>
        </Box>
      </Box>

      {/* Content */}
      {viewMode === 'code' ? (
        <Box>
          {/* File Tabs */}
          <Tabs 
            value={selectedTab} 
            onChange={(_, newValue) => setSelectedTab(newValue)}
            variant="scrollable"
            scrollButtons="auto"
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            {codeFiles.map((file, index) => (
              <Tab 
                key={index}
                label={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <span>{getFileIcon(file.filename)}</span>
                    {file.filename}
                  </Box>
                }
              />
            ))}
          </Tabs>

          {/* File Content */}
          {codeFiles[selectedTab] && renderCodeContent(codeFiles[selectedTab])}
        </Box>
      ) : (
        renderPreviewContent()
      )}
    </Paper>
  );
};

export default CodePreview; 