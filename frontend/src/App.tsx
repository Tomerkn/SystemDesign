import React from 'react';
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CacheProvider } from '@emotion/react';
import { StyledEngineProvider } from '@mui/material/styles';
import theme, { cacheRtl } from './theme';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Vehicles from './pages/Vehicles';
import Rentals from './pages/Rentals';
import Login from './pages/Login';

// Route protection wrapper
const RequireAuth = ({ children }: { children: JSX.Element }) => {
  if (localStorage.getItem('isLoggedIn') !== 'true') {
    return <Navigate to="/login" replace />;
  }
  return children;
};

// הגדרת נתיבי האפליקציה
const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: <RequireAuth><Layout /></RequireAuth>,
    children: [
      {
        index: true,  // דף הבית
        element: <Dashboard />
      },
      {
        path: 'customers',  // ניהול לקוחות
        element: <Customers />
      },
      {
        path: 'vehicles',  // ניהול רכבים
        element: <Vehicles />
      },
      {
        path: 'rentals',  // ניהול השכרות
        element: <Rentals />
      }
    ]
  }
]);

// קומפוננטת האפליקציה הראשית
const App: React.FC = () => {
  return (
    // מספק תמיכה בסגנונות MUI
    <StyledEngineProvider injectFirst>
      {/* מספק תמיכה בכיוון RTL עבור עברית */}
      <CacheProvider value={cacheRtl}>
        {/* מספק ערכת נושא מותאמת */}
        <ThemeProvider theme={theme}>
          {/* מספק ניתוב בין דפים */}
          <RouterProvider router={router} />
        </ThemeProvider>
      </CacheProvider>
    </StyledEngineProvider>
  );
};

export default App;
