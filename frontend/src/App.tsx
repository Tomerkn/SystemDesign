import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CacheProvider } from '@emotion/react';
import theme, { cacheRtl } from './theme';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Vehicles from './pages/Vehicles';
import Rentals from './pages/Rentals';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Dashboard />
      },
      {
        path: 'customers',
        element: <Customers />
      },
      {
        path: 'vehicles',
        element: <Vehicles />
      },
      {
        path: 'rentals',
        element: <Rentals />
      }
    ]
  }
]);

const App: React.FC = () => {
  return (
    <CacheProvider value={cacheRtl}>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </CacheProvider>
  );
};

export default App;
