import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CacheProvider } from '@emotion/react';
import { StyledEngineProvider } from '@mui/material/styles';
import theme, { cacheRtl } from './theme';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Vehicles from './pages/Vehicles';
import Rentals from './pages/Rentals';

// הגדרת נתיבי האפליקציה
const router = createBrowserRouter([
  {
    path: '/',  // נתיב ראשי
    element: <Layout />,  // תבנית בסיס לכל הדפים
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
