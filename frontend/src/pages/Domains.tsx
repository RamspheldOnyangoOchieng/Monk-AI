import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControlLabel,
  Switch,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Snackbar,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Refresh as RefreshIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Lock as LockIcon,
  LockOpen as LockOpenIcon,
  Dns as DnsIcon,
  Public as PublicIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import axios from 'axios';


// Mock data - replace with actual API calls in production

const domainsMock: DomainRecord[] = [
  {
    id: 1,
    name: 'example.com',
    status: 'active' as const,
    sslStatus: 'valid' as const,
    sslExpiry: '2024-12-31',
    environment: 'production',
    createdAt: '2023-01-01',
    dnsRecords: [
      {
        type: 'A',
        name: '@',
        value: '192.168.1.1',
        ttl: 3600
      },
      {
        type: 'CNAME',
        name: 'www',
        value: 'example.com',
        ttl: 3600
      }
    ]
  },
  {
    id: 2,
    name: 'test.example.com',
    status: 'pending' as const,
    sslStatus: 'none' as const,
    sslExpiry: '2024-12-31',
    environment: 'staging',
    createdAt: '2023-02-01',
    dnsRecords: [
      {
        type: 'A',
        name: '@',
        value: '192.168.1.2',
        ttl: 3600
      }
    ]
  }
];

interface DomainRecord {
  id: number;
  name: string;
  status: 'active' | 'inactive' | 'pending';
  sslStatus: 'valid' | 'expired' | 'invalid' | 'none';
  sslExpiry: string;
  environment: string;
  createdAt: string;
  dnsRecords: DNSRecord[];
}

interface DNSRecord {
  type: string;
  name: string;
  value: string;
  ttl: number;
  priority?: number;
}

interface DomainFormData {
  name: string;
  environment: string;
  enableSSL: boolean;
}

interface DNSFormData {
  type: string;
  name: string;
  value: string;
  ttl: number;
  priority?: number;
}

const Domains: React.FC = () => {
  const [domains, setDomains] = useState<DomainRecord[]>(domainsMock);
  const [selectedDomain, setSelectedDomain] = useState<DomainRecord | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [tabValue, setTabValue] = useState<number>(0);
  const [showDomainDialog, setShowDomainDialog] = useState<boolean>(false);
  const [showDNSDialog, setShowDNSDialog] = useState<boolean>(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<boolean>(false);
  const [domainFormData, setDomainFormData] = useState<DomainFormData>({
    name: '',
    environment: 'production',
    enableSSL: true,
  });
  const [dnsFormData, setDnsFormData] = useState<DNSFormData>({
    type: 'A',
    name: '',
    value: '',
    ttl: 3600,
    priority: 10,
  });
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error' | 'info' | 'warning'}>({ 
    open: false, 
    message: '', 
    severity: 'info' 
  });
  const [editMode, setEditMode] = useState<boolean>(false);
  const [editId, setEditId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<{name: string; environment: string; sslStatus: 'none' | 'valid' | 'expired' | 'invalid'}>({
    name: '',
    environment: '',
    sslStatus: 'none'
  });

  // Fetch domains
  useEffect(() => {
    // In a real app, you would fetch this data from your API
    // Example: axios.get('/api/domains').then(response => { ... })
  }, []);

  const handleRefresh = () => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleDomainSelect = (domain: DomainRecord) => {
    setSelectedDomain(domain);
  };

  const handleDomainFormChange = (field: keyof DomainFormData, value: any) => {
    setDomainFormData({
      ...domainFormData,
      [field]: value,
    });
  };

  const handleDnsFormChange = (field: keyof DNSFormData, value: any) => {
    setDnsFormData({
      ...dnsFormData,
      [field]: value,
    });
  };

  const handleAddDomain = () => {
    setEditMode(false);
    setDomainFormData({
      name: '',
      environment: 'production',
      enableSSL: true,
    });
    setShowDomainDialog(true);
  };

  const handleEditDomain = (editId: number) => {
    const domainToEdit = domains.find(d => d.id === editId);
    if (domainToEdit) {
      setEditId(editId);
      setEditForm({
        name: domainToEdit.name,
        environment: domainToEdit.environment,
        sslStatus: domainToEdit.sslStatus as 'none' | 'valid' | 'expired' | 'invalid'
      });
      setShowDomainDialog(true);
    }
  };

  const handleDeleteDomain = (domain: DomainRecord) => {
    setSelectedDomain(domain);
    setShowDeleteConfirm(true);
  };

  const confirmDeleteDomain = () => {
    if (selectedDomain) {
      // In a real app, you would call your API to delete the domain
      // Example: axios.delete(`/api/domains/${selectedDomain.id}`).then(...)
      
      // Update local state
      setDomains(domains.filter(d => d.id !== selectedDomain.id));
      setSelectedDomain(null);
      setShowDeleteConfirm(false);
      
      setSnackbar({
        open: true,
        message: `Domain ${selectedDomain.name} has been deleted`,
        severity: 'success'
      });
    }
  };

  const handleAddDNSRecord = () => {
    setEditMode(false);
    setDnsFormData({
      type: 'A',
      name: '',
      value: '',
      ttl: 3600,
      priority: 10,
    });
    setShowDNSDialog(true);
  };

  const handleEditDNSRecord = (record: DNSRecord, index: number) => {
    setEditMode(true);
    setEditId(index);
    setDnsFormData({
      ...record
    });
    setShowDNSDialog(true);
  };

  const handleDeleteDNSRecord = (index: number) => {
    if (selectedDomain) {
      // In a real app, you would call your API to delete the DNS record
      // Example: axios.delete(`/api/domains/${selectedDomain.id}/dns/${index}`).then(...)
      
      // Update local state
      const updatedDomain = { ...selectedDomain };
      updatedDomain.dnsRecords = updatedDomain.dnsRecords.filter((_, i) => i !== index);
      
      setSelectedDomain(updatedDomain);
      setDomains(domains.map(d => d.id === updatedDomain.id ? updatedDomain : d));
      
      setSnackbar({
        open: true,
        message: 'DNS record has been deleted',
        severity: 'success'
      });
    }
  };

  const handleSaveEdit = () => {
    if (editId && editForm.name && editForm.environment) {
      const updatedDomains = domains.map(domain => {
        if (domain.id === editId) {
          return {
            ...domain,
            name: editForm.name,
            environment: editForm.environment,
            sslStatus: editForm.sslStatus as 'none' | 'valid' | 'expired' | 'invalid'
          };
        }
        return domain;
      });
      
      setDomains(updatedDomains);
      setSelectedDomain(updatedDomains.find(d => d.id === editId) || null);
      
      setSnackbar({
        open: true,
        message: 'Domain updated successfully',
        severity: 'success'
      });
      setShowDomainDialog(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const getStatusChip = (status: string) => {
    switch (status) {
      case 'active':
        return <Chip icon={<CheckCircleIcon />} label="Active" color="success" size="small" />;
      case 'inactive':
        return <Chip icon={<ErrorIcon />} label="Inactive" color="error" size="small" />;
      case 'pending':
        return <Chip icon={<WarningIcon />} label="Pending" color="warning" size="small" />;
      default:
        return <Chip label={status} size="small" />;
    }
  };

  const getSSLStatusChip = (status: string) => {
    switch (status) {
      case 'valid':
        return <Chip icon={<LockIcon />} label="Valid" color="success" size="small" />;
      case 'expired':
        return <Chip icon={<LockOpenIcon />} label="Expired" color="error" size="small" />;
      case 'invalid':
        return <Chip icon={<WarningIcon />} label="Invalid" color="warning" size="small" />;
      case 'none':
        return <Chip icon={<LockOpenIcon />} label="None" color="default" size="small" />;
      default:
        return <Chip label={status} size="small" />;
    }
  };

  const getDomainCard = (domain: DomainRecord) => {
    const isSelected = selectedDomain?.id === domain.id;
    
    return (
      <Card 
        key={domain.id} 
        sx={{
          border: isSelected ? '2px solid #1976d2' : 'none',
          cursor: 'pointer',
        }}
        onClick={() => handleDomainSelect(domain)}
      >
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">{domain.name}</Typography>
            {getStatusChip(domain.status)}
          </Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Environment: {domain.environment}
          </Typography>
          <Box display="flex" alignItems="center" mt={1}>
            <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
              SSL:
            </Typography>
            {getSSLStatusChip(domain.sslStatus)}
            {domain.sslStatus === 'valid' && (
              <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                Expires: {domain.sslExpiry}
              </Typography>
            )}
          </Box>
        </CardContent>
        <CardActions>
          <Button 
            size="small" 
            startIcon={<EditIcon />}
            onClick={(e) => {
              e.stopPropagation();
              handleEditDomain(domain.id);
            }}
          >
            Edit
          </Button>
          <Button 
            size="small" 
            color="error"
            startIcon={<DeleteIcon />}
            onClick={(e) => {
              e.stopPropagation();
              handleDeleteDomain(domain);
            }}
          >
            Delete
          </Button>
        </CardActions>
      </Card>
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Domain Management
      </Typography>
      
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6">Domains</Typography>
        <Box>
          <Button 
            startIcon={<RefreshIcon />} 
            onClick={handleRefresh}
            disabled={isLoading}
            sx={{ mr: 1 }}
          >
            {isLoading ? <CircularProgress size={24} /> : 'Refresh'}
          </Button>
          <Button 
            variant="contained" 
            color="primary"
            startIcon={<AddIcon />}
            onClick={handleAddDomain}
          >
            Add Domain
          </Button>
        </Box>
      </Box>
      
      <Grid container spacing={3} mb={4}>
        {domains.map(domain => (
          <Grid item xs={12} sm={6} md={4} key={domain.id}>
            {getDomainCard(domain)}
          </Grid>
        ))}
      </Grid>
      
      {selectedDomain && (
        <>
          <Divider sx={{ my: 4 }} />
          
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h5">
              {selectedDomain.name}
            </Typography>
            <Box>
              <Button 
                variant="outlined" 
                startIcon={<SettingsIcon />}
                onClick={() => handleEditDomain(selectedDomain.id)}
                sx={{ mr: 1 }}
              >
                Settings
              </Button>
            </Box>
          </Box>
          
          <Paper sx={{ mb: 4 }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange}
              indicatorColor="primary"
              textColor="primary"
            >
              <Tab label="DNS Records" icon={<DnsIcon />} iconPosition="start" />
              <Tab label="SSL Certificate" icon={<LockIcon />} iconPosition="start" />
              <Tab label="Domain Settings" icon={<SettingsIcon />} iconPosition="start" />
            </Tabs>
            
            <Box p={3}>
              {/* DNS Records Tab */}
              {tabValue === 0 && (
                <>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6">DNS Records</Typography>
                    <Button 
                      variant="contained" 
                      color="primary"
                      startIcon={<AddIcon />}
                      onClick={handleAddDNSRecord}
                    >
                      Add Record
                    </Button>
                  </Box>
                  
                  <TableContainer component={Paper} variant="outlined">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Type</TableCell>
                          <TableCell>Name</TableCell>
                          <TableCell>Value</TableCell>
                          <TableCell>TTL</TableCell>
                          {selectedDomain.dnsRecords.some(r => r.type === 'MX') && (
                            <TableCell>Priority</TableCell>
                          )}
                          <TableCell>Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {selectedDomain.dnsRecords.length > 0 ? (
                          selectedDomain.dnsRecords.map((record, index) => (
                            <TableRow key={index}>
                              <TableCell>{record.type}</TableCell>
                              <TableCell>{record.name}</TableCell>
                              <TableCell>{record.value}</TableCell>
                              <TableCell>{record.ttl}</TableCell>
                              {selectedDomain.dnsRecords.some(r => r.type === 'MX') && (
                                <TableCell>{record.type === 'MX' ? record.priority : '-'}</TableCell>
                              )}
                              <TableCell>
                                <IconButton size="small" onClick={() => handleEditDNSRecord(record, index)}>
                                  <EditIcon fontSize="small" />
                                </IconButton>
                                <IconButton size="small" color="error" onClick={() => handleDeleteDNSRecord(index)}>
                                  <DeleteIcon fontSize="small" />
                                </IconButton>
                              </TableCell>
                            </TableRow>
                          ))
                        ) : (
                          <TableRow>
                            <TableCell colSpan={6} align="center">
                              No DNS records found
                            </TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </>
              )}
              
              {/* SSL Certificate Tab */}
              {tabValue === 1 && (
                <>
                  <Box mb={3}>
                    <Typography variant="h6" gutterBottom>SSL Certificate</Typography>
                    
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2">Status</Typography>
                          <Box mt={1}>
                            {getSSLStatusChip(selectedDomain.sslStatus)}
                          </Box>
                        </Grid>
                        
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2">Expiry Date</Typography>
                          <Typography>
                            {selectedDomain.sslStatus !== 'none' ? selectedDomain.sslExpiry : 'N/A'}
                          </Typography>
                        </Grid>
                        
                        <Grid item xs={12} mt={2}>
                          <Divider />
                        </Grid>
                        
                        <Grid item xs={12} mt={2}>
                          <Typography variant="subtitle2" gutterBottom>Actions</Typography>
                          <Button 
                            variant="contained" 
                            color="primary"
                            disabled={selectedDomain.sslStatus === 'valid'}
                            sx={{ mr: 1 }}
                          >
                            {selectedDomain.sslStatus === 'none' ? 'Enable SSL' : 'Renew Certificate'}
                          </Button>
                          
                          {selectedDomain.sslStatus !== 'none' && (
                            <Button 
                              variant="outlined" 
                              color="error"
                            >
                              Disable SSL
                            </Button>
                          )}
                        </Grid>
                      </Grid>
                    </Paper>
                  </Box>
                  
                  <Box>
                    <Typography variant="h6" gutterBottom>SSL Configuration</Typography>
                    
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>Certificate Provider</Typography>
                      <Typography variant="body2" gutterBottom>
                        Let's Encrypt (Automatic)
                      </Typography>
                      
                      <Divider sx={{ my: 2 }} />
                      
                      <Typography variant="subtitle2" gutterBottom>HTTPS Redirect</Typography>
                      <FormControlLabel
                        control={<Switch checked={true} />}
                        label="Redirect HTTP to HTTPS"
                      />
                      
                      <Divider sx={{ my: 2 }} />
                      
                      <Typography variant="subtitle2" gutterBottom>HSTS (HTTP Strict Transport Security)</Typography>
                      <FormControlLabel
                        control={<Switch checked={true} />}
                        label="Enable HSTS"
                      />
                      <Typography variant="body2" color="text.secondary">
                        Forces browsers to use HTTPS for future visits
                      </Typography>
                    </Paper>
                  </Box>
                </>
              )}
              
              {/* Domain Settings Tab */}
              {tabValue === 2 && (
                <>
                  <Box mb={3}>
                    <Typography variant="h6" gutterBottom>Domain Information</Typography>
                    
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2">Domain Name</Typography>
                          <Typography>{selectedDomain.name}</Typography>
                        </Grid>
                        
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2">Status</Typography>
                          <Box mt={1}>
                            {getStatusChip(selectedDomain.status)}
                          </Box>
                        </Grid>
                        
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2">Environment</Typography>
                          <Typography>{selectedDomain.environment}</Typography>
                        </Grid>
                        
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2">Created</Typography>
                          <Typography>{selectedDomain.createdAt}</Typography>
                        </Grid>
                      </Grid>
                    </Paper>
                  </Box>
                  
                  <Box>
                    <Typography variant="h6" gutterBottom>Domain Configuration</Typography>
                    
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>Environment</Typography>
                      <FormControl fullWidth size="small" sx={{ mb: 2 }}>
                        <Select
                          value={selectedDomain.environment}
                          disabled
                        >
                          <MenuItem value="production">Production</MenuItem>
                          <MenuItem value="staging">Staging</MenuItem>
                          <MenuItem value="development">Development</MenuItem>
                        </Select>
                      </FormControl>
                      
                      <Divider sx={{ my: 2 }} />
                      
                      <Typography variant="subtitle2" gutterBottom>Domain Status</Typography>
                      <FormControl fullWidth size="small">
                        <Select
                          value={selectedDomain.status}
                        >
                          <MenuItem value="active">Active</MenuItem>
                          <MenuItem value="inactive">Inactive</MenuItem>
                          <MenuItem value="pending">Pending</MenuItem>
                        </Select>
                      </FormControl>
                      
                      <Box mt={3} display="flex" justifyContent="flex-end">
                        <Button 
                          variant="contained" 
                          color="primary"
                        >
                          Save Changes
                        </Button>
                      </Box>
                    </Paper>
                  </Box>
                </>
              )}
            </Box>
          </Paper>
        </>
      )}
      
      {/* Add/Edit Domain Dialog */}
      <Dialog open={showDomainDialog} onClose={() => setShowDomainDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editMode ? 'Edit Domain' : 'Add Domain'}</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <TextField
              fullWidth
              margin="normal"
              label="Domain Name"
              value={domainFormData.name}
              onChange={(e) => handleDomainFormChange('name', e.target.value)}
              helperText="e.g. example.com"
            />
            
            <FormControl fullWidth margin="normal">
              <InputLabel>Environment</InputLabel>
              <Select
                value={domainFormData.environment}
                label="Environment"
                onChange={(e) => handleDomainFormChange('environment', e.target.value)}
              >
                <MenuItem value="production">Production</MenuItem>
                <MenuItem value="staging">Staging</MenuItem>
                <MenuItem value="development">Development</MenuItem>
              </Select>
            </FormControl>
            
            <Box mt={2}>
              <FormControlLabel
                control={
                  <Switch
                    checked={domainFormData.enableSSL}
                    onChange={(e) => handleDomainFormChange('enableSSL', e.target.checked)}
                  />
                }
                label="Enable SSL Certificate"
              />
            </Box>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDomainDialog(false)}>Cancel</Button>
          <Button onClick={handleSaveEdit} variant="contained" color="primary">
            {editMode ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Add/Edit DNS Record Dialog */}
      <Dialog open={showDNSDialog} onClose={() => setShowDNSDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editMode ? 'Edit DNS Record' : 'Add DNS Record'}</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Record Type</InputLabel>
              <Select
                value={dnsFormData.type}
                label="Record Type"
                onChange={(e) => handleDnsFormChange('type', e.target.value)}
              >
                <MenuItem value="A">A (Address)</MenuItem>
                <MenuItem value="AAAA">AAAA (IPv6 Address)</MenuItem>
                <MenuItem value="CNAME">CNAME (Canonical Name)</MenuItem>
                <MenuItem value="MX">MX (Mail Exchange)</MenuItem>
                <MenuItem value="TXT">TXT (Text)</MenuItem>
                <MenuItem value="NS">NS (Name Server)</MenuItem>
                <MenuItem value="SRV">SRV (Service)</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              fullWidth
              margin="normal"
              label="Name"
              value={dnsFormData.name}
              onChange={(e) => handleDnsFormChange('name', e.target.value)}
              helperText="e.g. @ for root, www for subdomain"
            />
            
            <TextField
              fullWidth
              margin="normal"
              label="Value"
              value={dnsFormData.value}
              onChange={(e) => handleDnsFormChange('value', e.target.value)}
              helperText={dnsFormData.type === 'A' ? 'e.g. 192.168.1.1' : 'e.g. example.com'}
            />
            
            <TextField
              fullWidth
              margin="normal"
              label="TTL (seconds)"
              type="number"
              value={dnsFormData.ttl}
              onChange={(e) => handleDnsFormChange('ttl', parseInt(e.target.value))}
              helperText="Time to live in seconds (e.g. 3600 for 1 hour)"
            />
            
            {dnsFormData.type === 'MX' && (
              <TextField
                fullWidth
                margin="normal"
                label="Priority"
                type="number"
                value={dnsFormData.priority}
                onChange={(e) => handleDnsFormChange('priority', parseInt(e.target.value))}
                helperText="Lower values have higher priority"
              />
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDNSDialog(false)}>Cancel</Button>
          <Button onClick={() => {}} variant="contained" color="primary">
            {editMode ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Delete Confirmation Dialog */}
      <Dialog open={showDeleteConfirm} onClose={() => setShowDeleteConfirm(false)}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete the domain <strong>{selectedDomain?.name}</strong>?
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDeleteConfirm(false)}>Cancel</Button>
          <Button onClick={confirmDeleteDomain} variant="contained" color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
      
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
    </Box>
  );
};

export default Domains;
