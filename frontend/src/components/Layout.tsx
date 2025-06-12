// ייבוא ספריות וקומפוננטות
import React from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Box, Button } from '@mui/material';

// קומפוננטת תבנית הבסיס של האפליקציה
const Layout: React.FC = () => {
  // מקבל את המיקום הנוכחי בניתוב
  const location = useLocation();
  const navigate = useNavigate();

  // פונקציה לבדיקה האם הכפתור פעיל (מסלול נוכחי)
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    // מיכל ראשי עם כיוון מלמעלה למטה וגובה מינימלי של המסך
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* סרגל ניווט עליון */}
      <AppBar position="static">
        <Toolbar>
          {/* כותרת האפליקציה */}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            מערכת השכרת רכבים
          </Typography>
          {/* כפתור לוח בקרה */}
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
          {/* כפתור לקוחות */}
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
          {/* כפתור רכבים */}
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
          {/* כפתור השכרות */}
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
          <Button color="inherit" onClick={handleLogout} sx={{ ml: 2 }}>
            התנתק
          </Button>
        </Toolbar>
      </AppBar>
      {/* מיכל ראשי לתוכן הדף */}
      <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
        {/* כאן יוצג התוכן של כל דף */}
        <Outlet />
      </Container>
    </Box>
  );
};

export default Layout;