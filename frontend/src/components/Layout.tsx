import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Box, Button } from '@mui/material';

const Layout: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            מערכת השכרת רכבים
          </Typography>
          <Button 
            color="inherit" 
            component={Link} 
            to="/"
            sx={{ 
              backgroundColor: isActive('/') ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.2)'
              }
            }}
          >
            לוח בקרה
          </Button>
          <Button 
            color="inherit" 
            component={Link} 
            to="/customers"
            sx={{ 
              backgroundColor: isActive('/customers') ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.2)'
              }
            }}
          >
            לקוחות
          </Button>
          <Button 
            color="inherit" 
            component={Link} 
            to="/vehicles"
            sx={{ 
              backgroundColor: isActive('/vehicles') ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.2)'
              }
            }}
          >
            רכבים
          </Button>
          <Button 
            color="inherit" 
            component={Link} 
            to="/rentals"
            sx={{ 
              backgroundColor: isActive('/rentals') ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.2)'
              }
            }}
          >
            השכרות
          </Button>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
        <Outlet />
      </Container>
    </Box>
  );
};

export default Layout; 