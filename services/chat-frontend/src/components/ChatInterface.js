import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Container,
  Grid,
  Card,
  CardContent,
  Chip,
  IconButton,
  Divider,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
  Speed as MetricsIcon,
  Error as ErrorIcon,
  Timeline as TrendIcon,
  Storage as StorageIcon,
} from '@mui/icons-material';
import { io } from 'socket.io-client';
import { format } from 'date-fns';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [quickQueries, setQuickQueries] = useState([]);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  
  const socketRef = useRef();
  const messagesEndRef = useRef();

  // Initialize WebSocket connection
  useEffect(() => {
    const socket = io(API_BASE_URL);
    socketRef.current = socket;

    socket.on('connect', () => {
      setIsConnected(true);
      console.log('Connected to chat server');
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
      console.log('Disconnected from chat server');
    });

    socket.on('response', (data) => {
      setIsLoading(false);
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'assistant',
        content: data.response,
        timestamp: new Date(data.timestamp),
        metadata: data.metadata,
        suggestions: data.suggestions
      }]);
    });

    socket.on('error', (data) => {
      setIsLoading(false);
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'error',
        content: `Error: ${data.error}`,
        timestamp: new Date(data.timestamp)
      }]);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load quick queries on component mount
  useEffect(() => {
    const loadQuickQueries = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/quick-queries`);
        setQuickQueries(response.data);
      } catch (error) {
        console.error('Failed to load quick queries:', error);
      }
    };

    loadQuickQueries();
  }, []);

  const sendMessage = (message = inputMessage) => {
    if (!message.trim() || !isConnected) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Send to server via WebSocket
    socketRef.current.emit('message', {
      message: message,
      session_id: sessionId,
      include_metrics: true,
      include_logs: true,
      include_traces: true,
      time_range: '1h'
    });

    setInputMessage('');
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const handleQuickQuery = (query) => {
    sendMessage(query);
  };

  const getMessageIcon = (type) => {
    switch (type) {
      case 'user':
        return <PersonIcon color="primary" />;
      case 'assistant':
        return <BotIcon color="secondary" />;
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return <BotIcon />;
    }
  };

  const formatMetadata = (metadata) => {
    if (!metadata) return null;

    return (
      <Box sx={{ mt: 2 }}>
        {metadata.metrics && (
          <Box sx={{ mb: 1 }}>
            <Typography variant="caption" color="text.secondary">
              Metrics analyzed: {metadata.metrics.count} data points
            </Typography>
          </Box>
        )}
        {metadata.logs && (
          <Box sx={{ mb: 1 }}>
            <Typography variant="caption" color="text.secondary">
              Logs analyzed: {metadata.logs.count} entries
            </Typography>
          </Box>
        )}
        {metadata.traces && (
          <Box sx={{ mb: 1 }}>
            <Typography variant="caption" color="text.secondary">
              Traces analyzed: {metadata.traces.count} spans
            </Typography>
          </Box>
        )}
      </Box>
    );
  };

  const quickQueryCategories = quickQueries.reduce((acc, query) => {
    if (!acc[query.category]) {
      acc[query.category] = [];
    }
    acc[query.category].push(query);
    return acc;
  }, {});

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'performance':
        return <MetricsIcon />;
      case 'troubleshooting':
        return <ErrorIcon />;
      case 'analysis':
        return <TrendIcon />;
      case 'monitoring':
        return <StorageIcon />;
      default:
        return <MetricsIcon />;
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      <Grid container spacing={3}>
        {/* Chat Interface */}
        <Grid item xs={12} md={8}>
          <Paper
            elevation={3}
            sx={{
              height: '80vh',
              display: 'flex',
              flexDirection: 'column',
              bgcolor: 'background.paper',
            }}
          >
            {/* Header */}
            <Box
              sx={{
                p: 2,
                borderBottom: 1,
                borderColor: 'divider',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}
            >
              <Typography variant="h6">
                Observability AI Assistant
              </Typography>
              <Chip
                label={isConnected ? 'Connected' : 'Disconnected'}
                color={isConnected ? 'success' : 'error'}
                size="small"
              />
            </Box>

            {/* Messages */}
            <Box
              sx={{
                flexGrow: 1,
                overflow: 'auto',
                p: 2,
                bgcolor: 'background.default',
              }}
            >
              {messages.length === 0 && (
                <Box sx={{ textAlign: 'center', mt: 4 }}>
                  <BotIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    Welcome to the Observability AI Assistant
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Ask me about your system performance, errors, or any observability data.
                  </Typography>
                </Box>
              )}

              {messages.map((message) => (
                <Box key={message.id} sx={{ mb: 2 }}>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: 1,
                      flexDirection: message.type === 'user' ? 'row-reverse' : 'row',
                    }}
                  >
                    <Box
                      sx={{
                        bgcolor: message.type === 'user' ? 'primary.main' : 'background.paper',
                        color: message.type === 'user' ? 'white' : 'text.primary',
                        borderRadius: 2,
                        p: 2,
                        maxWidth: '70%',
                        border: message.type === 'error' ? '1px solid red' : 'none',
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        {getMessageIcon(message.type)}
                        <Typography variant="caption" color="text.secondary">
                          {format(message.timestamp, 'HH:mm:ss')}
                        </Typography>
                      </Box>
                      
                      <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                        {message.content}
                      </Typography>

                      {formatMetadata(message.metadata)}

                      {message.suggestions && message.suggestions.length > 0 && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                            Suggested actions:
                          </Typography>
                          {message.suggestions.map((suggestion, index) => (
                            <Chip
                              key={index}
                              label={suggestion}
                              size="small"
                              onClick={() => handleQuickQuery(suggestion)}
                              sx={{ mr: 1, mb: 1 }}
                              variant="outlined"
                            />
                          ))}
                        </Box>
                      )}
                    </Box>
                  </Box>
                </Box>
              ))}

              {isLoading && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                  <CircularProgress size={20} />
                  <Typography variant="body2" color="text.secondary">
                    AI is analyzing your request...
                  </Typography>
                </Box>
              )}

              <div ref={messagesEndRef} />
            </Box>

            {/* Input */}
            <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Ask about your system performance, errors, or any observability question..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  multiline
                  maxRows={3}
                  disabled={!isConnected || isLoading}
                />
                <IconButton
                  color="primary"
                  onClick={() => sendMessage()}
                  disabled={!inputMessage.trim() || !isConnected || isLoading}
                  sx={{ alignSelf: 'flex-end' }}
                >
                  <SendIcon />
                </IconButton>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Quick Queries Panel */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 2, height: '80vh', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              Quick Queries
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Click on any of these common queries to get started
            </Typography>

            {Object.entries(quickQueryCategories).map(([category, queries]) => (
              <Box key={category} sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                  {getCategoryIcon(category)}
                  <Typography variant="subtitle1" sx={{ textTransform: 'capitalize' }}>
                    {category}
                  </Typography>
                </Box>
                
                {queries.map((query, index) => (
                  <Card
                    key={index}
                    sx={{
                      mb: 1,
                      cursor: 'pointer',
                      '&:hover': {
                        bgcolor: 'action.hover',
                      },
                    }}
                    onClick={() => handleQuickQuery(query.query)}
                  >
                    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                      <Typography variant="body2" fontWeight="medium">
                        {query.query}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {query.description}
                      </Typography>
                    </CardContent>
                  </Card>
                ))}
              </Box>
            ))}

            {!isConnected && (
              <Alert severity="warning" sx={{ mt: 2 }}>
                Connection lost. Attempting to reconnect...
              </Alert>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ChatInterface;