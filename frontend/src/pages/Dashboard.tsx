import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Box, Alert, Snackbar } from '@mui/material';
import {
  People as PeopleIcon,
  DirectionsCar as CarIcon,
  Assignment as RentalIcon,
} from '@mui/icons-material';
import { getCustomers, getVehicles, getRentals } from '../services/api';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    customers: 0,
    vehicles: 0,
    activeRentals: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const [customersRes, vehiclesRes, rentalsRes] = await Promise.all([
        getCustomers(),
        getVehicles(),
        getRentals(),
      ]);

      const activeRentals = rentalsRes.data.filter(
        (rental) => rental.status === 'active'
      ).length;

      setStats({
        customers: customersRes.data.length,
        vehicles: vehiclesRes.data.length,
        activeRentals,
      });
      setError(null);
    } catch (err) {
      setError('שגיאה בטעינת נתוני הדשבורד');
      console.error('Error fetching dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  };

  const statItems = [
    {
      title: 'לקוחות',
      value: stats.customers.toString(),
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      color: '#1976d2',
    },
    {
      title: 'רכבים',
      value: stats.vehicles.toString(),
      icon: <CarIcon sx={{ fontSize: 40 }} />,
      color: '#2e7d32',
    },
    {
      title: 'השכרות פעילות',
      value: stats.activeRentals.toString(),
      icon: <RentalIcon sx={{ fontSize: 40 }} />,
      color: '#ed6c02',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        דשבורד
      </Typography>

      {error && (
        <Snackbar
          open={!!error}
          autoHideDuration={6000}
          onClose={() => setError(null)}
        >
          <Alert severity="error" onClose={() => setError(null)}>
            {error}
          </Alert>
        </Snackbar>
      )}

      <Grid container spacing={3}>
        {statItems.map((stat) => (
          <Grid
            key={stat.title}
            sx={{
              display: 'flex',
              width: { xs: '100%', sm: '50%', md: '33.33%' },
              p: 1,
            }}
          >
            <Paper
              sx={{
                p: 3,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                width: '100%',
              }}
            >
              <Box
                sx={{
                  backgroundColor: `${stat.color}15`,
                  borderRadius: '50%',
                  p: 2,
                  mb: 2,
                  color: stat.color,
                }}
              >
                {stat.icon}
              </Box>
              <Typography variant="h4" component="div" gutterBottom>
                {stat.value}
              </Typography>
              <Typography variant="h6" color="text.secondary">
                {stat.title}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Dashboard; 