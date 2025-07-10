import React from 'react';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
} from '@mui/material';
import {
  Timeline as TrendIcon,
  Speed as MetricsIcon,
  Storage as StorageIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';

const Dashboard = () => {
  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      <Typography variant="h4" gutterBottom>
        Observability Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <MetricsIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6">Metrics</Typography>
            <Typography variant="body2" color="text.secondary">
              Real-time performance metrics
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <ErrorIcon sx={{ fontSize: 48, color: 'error.main', mb: 2 }} />
            <Typography variant="h6">Logs</Typography>
            <Typography variant="body2" color="text.secondary">
              System logs and error tracking
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <TrendIcon sx={{ fontSize: 48, color: 'secondary.main', mb: 2 }} />
            <Typography variant="h6">Traces</Typography>
            <Typography variant="body2" color="text.secondary">
              Distributed tracing
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6} lg={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <StorageIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
            <Typography variant="h6">Storage</Typography>
            <Typography variant="body2" color="text.secondary">
              Data storage metrics
            </Typography>
          </Paper>
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            AI-Powered Insights
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Use the Chat interface to get AI-powered insights about your system performance.
            Ask questions like "What's the current system health?" or "Show me recent errors".
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default Dashboard;