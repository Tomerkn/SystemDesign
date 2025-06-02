// ייבוא ספריות וקומפוננטות
import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Box, Alert, Snackbar } from '@mui/material';
import {
  People as PeopleIcon,
  DirectionsCar as CarIcon,
  Assignment as RentalIcon,
} from '@mui/icons-material';
import { getCustomers, getVehicles, getRentals } from '../services/api';

// קומפוננטת דף הבית - מציגה סטטיסטיקות כלליות של המערכת
const Dashboard: React.FC = () => {
  // מצב המכיל את הנתונים הסטטיסטיים
  const [stats, setStats] = useState({
    customers: 0,  // מספר הלקוחות
    vehicles: 0,   // מספר הרכבים
    activeRentals: 0,  // מספר ההשכרות הפעילות
  });
  // מצבים לטיפול בטעינה ושגיאות
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // טעינת הנתונים בעת טעינת הדף
  useEffect(() => {
    fetchStats();
  }, []);

  // פונקציה לטעינת הנתונים מהשרת
  const fetchStats = async () => {
    try {
      setLoading(true);
      // טעינה מקבילה של כל הנתונים
      const [customersRes, vehiclesRes, rentalsRes] = await Promise.all([
        getCustomers(),
        getVehicles(),
        getRentals(),
      ]);

      // חישוב מספר ההשכרות הפעילות
      const activeRentals = rentalsRes.data.filter(
        (rental) => rental.status === 'active'
      ).length;

      // עדכון הנתונים במצב
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

  // הגדרת פריטי הסטטיסטיקה שיוצגו
  const statItems = [
    {
      title: 'לקוחות',
      value: stats.customers.toString(),
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      color: '#1976d2',  // כחול
    },
    {
      title: 'רכבים',
      value: stats.vehicles.toString(),
      icon: <CarIcon sx={{ fontSize: 40 }} />,
      color: '#2e7d32',  // ירוק
    },
    {
      title: 'השכרות פעילות',
      value: stats.activeRentals.toString(),
      icon: <RentalIcon sx={{ fontSize: 40 }} />,
      color: '#ed6c02',  // כתום
    },
  ];

  return (
    <Box>
      {/* כותרת הדף */}
      <Typography variant="h4" gutterBottom>
        דשבורד
      </Typography>

      {/* הצגת שגיאות */}
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

      {/* רשת הסטטיסטיקות */}
      <Grid container spacing={3}>
        {statItems.map((stat) => (
          <Grid
            key={stat.title}
            sx={{
              display: 'flex',
              width: { xs: '100%', sm: '50%', md: '33.33%' },  // רספונסיביות
              p: 1,
            }}
          >
            {/* כרטיס סטטיסטיקה */}
            <Paper
              sx={{
                p: 3,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                width: '100%',
              }}
            >
              {/* אייקון הסטטיסטיקה */}
              <Box
                sx={{
                  backgroundColor: `${stat.color}15`,  // צבע רקע שקוף
                  borderRadius: '50%',
                  p: 2,
                  mb: 2,
                  color: stat.color,
                }}
              >
                {stat.icon}
              </Box>
              {/* ערך הסטטיסטיקה */}
              <Typography variant="h4" component="div" gutterBottom>
                {stat.value}
              </Typography>
              {/* כותרת הסטטיסטיקה */}
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