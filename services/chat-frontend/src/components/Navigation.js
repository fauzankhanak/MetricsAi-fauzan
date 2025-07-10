import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
} from '@mui/material';
import {
  Chat as ChatIcon,
  Dashboard as DashboardIcon,
  HealthAndSafety as HealthIcon,
  SmartToy as BotIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { path: '/chat', label: 'Chat', icon: ChatIcon },
    { path: '/dashboard', label: 'Dashboard', icon: DashboardIcon },
    { path: '/status', label: 'Status', icon: HealthIcon },
  ];

  return (
    <AppBar position="static" elevation={1}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <BotIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ mr: 4 }}>
            Observability AI
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 1 }}>
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Button
                  key={item.path}
                  color="inherit"
                  startIcon={<Icon />}
                  onClick={() => navigate(item.path)}
                  sx={{
                    bgcolor: location.pathname === item.path ? 'rgba(255,255,255,0.1)' : 'transparent',
                  }}
                >
                  {item.label}
                </Button>
              );
            })}
          </Box>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;