import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  Chip,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  CheckCircle as HealthyIcon,
  Error as UnhealthyIcon,
  Warning as DegradedIcon,
  Help as UnknownIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const SystemStatus = () => {
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_BASE_URL}/status`);
        setSystemStatus(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch system status');
        console.error('Status fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
        return <HealthyIcon color="success" />;
      case 'unhealthy':
        return <UnhealthyIcon color="error" />;
      case 'degraded':
        return <DegradedIcon color="warning" />;
      case 'unreachable':
        return <UnhealthyIcon color="error" />;
      default:
        return <UnknownIcon color="disabled" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'success';
      case 'unhealthy':
        return 'error';
      case 'degraded':
        return 'warning';
      case 'unreachable':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Container maxWidth="xl" sx={{ py: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ py: 3 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  const overallStatus = systemStatus?.status || 'unknown';
  const services = systemStatus?.services || {};

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      <Typography variant="h4" gutterBottom>
        System Status
      </Typography>
      
      {/* Overall Status */}
      <Box sx={{ mb: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
            {getStatusIcon(overallStatus)}
            <Typography variant="h5">
              Overall Status: 
              <Chip 
                label={overallStatus.toUpperCase()} 
                color={getStatusColor(overallStatus)}
                sx={{ ml: 2 }}
              />
            </Typography>
          </Box>
          <Typography variant="body2" color="text.secondary">
            Last updated: {systemStatus?.timestamp ? new Date(systemStatus.timestamp).toLocaleString() : 'Unknown'}
          </Typography>
        </Paper>
      </Box>

      {/* Services Status */}
      <Paper sx={{ mb: 4 }}>
        <Box sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Service Health
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Service</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Response Time</TableCell>
                  <TableCell>Details</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {Object.entries(services).map(([serviceName, serviceData]) => (
                  <TableRow key={serviceName}>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getStatusIcon(serviceData.status)}
                        <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                          {serviceName.replace('_', ' ')}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={serviceData.status} 
                        color={getStatusColor(serviceData.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {serviceData.response_time ? 
                        `${(serviceData.response_time * 1000).toFixed(0)}ms` : 
                        'N/A'
                      }
                    </TableCell>
                    <TableCell>
                      {serviceData.error ? (
                        <Typography variant="caption" color="error">
                          {serviceData.error}
                        </Typography>
                      ) : serviceData.status_code ? (
                        <Typography variant="caption">
                          HTTP {serviceData.status_code}
                        </Typography>
                      ) : (
                        <Typography variant="caption" color="text.secondary">
                          Operational
                        </Typography>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      </Paper>

      {/* System Information */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Data Sources
            </Typography>
            <Box>
              <Typography variant="body2" color="text.secondary">
                • Prometheus - Metrics collection and storage
              </Typography>
              <Typography variant="body2" color="text.secondary">
                • Elasticsearch - Log storage and search
              </Typography>
              <Typography variant="body2" color="text.secondary">
                • Jaeger - Distributed tracing
              </Typography>
              <Typography variant="body2" color="text.secondary">
                • Qdrant - Vector database for AI
              </Typography>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              AI Services
            </Typography>
            <Box>
              <Typography variant="body2" color="text.secondary">
                • AI Processor - Data analysis and insights
              </Typography>
              <Typography variant="body2" color="text.secondary">
                • Chat API - Natural language interface
              </Typography>
              <Typography variant="body2" color="text.secondary">
                • Vector Store - Semantic search
              </Typography>
              <Typography variant="body2" color="text.secondary">
                • Analytics Engine - Performance analysis
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default SystemStatus;