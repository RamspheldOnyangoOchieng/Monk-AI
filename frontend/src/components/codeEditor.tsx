import React, { useEffect, useState } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

const CodeEditor = () => {
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Show loading screen for 2 seconds before redirecting
    const timer = setTimeout(() => {
      // Replace this URL with your actual deployed app URL
      window.location.href = 'https://browser-ide-for-monk-ai.vercel.app/';
    }, 2000);
    
    return () => clearTimeout(timer);
  }, []);
  
  return (
    <Box 
      sx={{ 
        display: 'flex', 
        flexDirection: 'column',
        alignItems: 'center', 
        justifyContent: 'center',
        height: '70vh'
      }}
    >
      <CircularProgress size={60} />
      <Typography variant="h5" sx={{ mt: 4 }}>
        Loading Code Editor...
      </Typography>
    </Box>
  );
};

export default CodeEditor;
