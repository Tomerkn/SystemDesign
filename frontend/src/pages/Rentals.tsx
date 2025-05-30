import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Snackbar,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { he } from 'date-fns/locale';
import { Rental, getRentals, createRental } from '../services/api';

const Rentals: React.FC = () => {
  const [rentals, setRentals] = useState<Rental[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);
  const [newRental, setNewRental] = useState<Omit<Rental, 'id'>>({
    customer_id: '',
    vehicle_id: '',
    start_date: new Date().toISOString(),
    end_date: new Date().toISOString(),
    total_price: 0,
    status: 'active',
  });

  useEffect(() => {
    fetchRentals();
  }, []);

  const fetchRentals = async () => {
    try {
      setLoading(true);
      const response = await getRentals();
      setRentals(response.data);
      setError(null);
    } catch (err) {
      setError('שגיאה בטעינת רשימת ההשכרות');
      console.error('Error fetching rentals:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setNewRental({
      customer_id: '',
      vehicle_id: '',
      start_date: new Date().toISOString(),
      end_date: new Date().toISOString(),
      total_price: 0,
      status: 'active',
    });
  };

  const handleAddRental = async () => {
    try {
      const response = await createRental(newRental);
      setRentals([...rentals, response.data]);
      handleClose();
      setError(null);
    } catch (err) {
      setError('שגיאה בהוספת השכרה חדשה');
      console.error('Error creating rental:', err);
    }
  };

  const getStatusText = (status: Rental['status']) => {
    switch (status) {
      case 'active':
        return 'פעיל';
      case 'completed':
        return 'הושלם';
      case 'cancelled':
        return 'בוטל';
      default:
        return status;
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">השכרות</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleClickOpen}
        >
          הוסף השכרה
        </Button>
      </Box>

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

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>מזהה</TableCell>
              <TableCell>מזהה לקוח</TableCell>
              <TableCell>מזהה רכב</TableCell>
              <TableCell>תאריך התחלה</TableCell>
              <TableCell>תאריך סיום</TableCell>
              <TableCell>מחיר כולל</TableCell>
              <TableCell>סטטוס</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rentals.map((rental) => (
              <TableRow key={rental.id}>
                <TableCell>{rental.id}</TableCell>
                <TableCell>{rental.customer_id}</TableCell>
                <TableCell>{rental.vehicle_id}</TableCell>
                <TableCell>
                  {new Date(rental.start_date).toLocaleDateString('he-IL')}
                </TableCell>
                <TableCell>
                  {new Date(rental.end_date).toLocaleDateString('he-IL')}
                </TableCell>
                <TableCell>₪{rental.total_price}</TableCell>
                <TableCell>{getStatusText(rental.status)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>הוסף השכרה חדשה</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="מזהה לקוח"
            fullWidth
            value={newRental.customer_id}
            onChange={(e) =>
              setNewRental({ ...newRental, customer_id: e.target.value })
            }
          />
          <TextField
            margin="dense"
            label="מזהה רכב"
            fullWidth
            value={newRental.vehicle_id}
            onChange={(e) =>
              setNewRental({ ...newRental, vehicle_id: e.target.value })
            }
          />
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={he}>
            <DatePicker
              label="תאריך התחלה"
              value={new Date(newRental.start_date)}
              onChange={(date: Date | null) =>
                setNewRental({ ...newRental, start_date: date ? date.toISOString() : new Date().toISOString() })
              }
              sx={{ width: '100%', mt: 2 }}
            />
            <DatePicker
              label="תאריך סיום"
              value={new Date(newRental.end_date)}
              onChange={(date: Date | null) =>
                setNewRental({ ...newRental, end_date: date ? date.toISOString() : new Date().toISOString() })
              }
              sx={{ width: '100%', mt: 2 }}
            />
          </LocalizationProvider>
          <TextField
            margin="dense"
            label="מחיר כולל"
            type="number"
            fullWidth
            value={newRental.total_price}
            onChange={(e) =>
              setNewRental({
                ...newRental,
                total_price: parseFloat(e.target.value) || 0,
              })
            }
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>סטטוס</InputLabel>
            <Select
              value={newRental.status}
              label="סטטוס"
              onChange={(e) =>
                setNewRental({
                  ...newRental,
                  status: e.target.value as Rental['status'],
                })
              }
            >
              <MenuItem value="active">פעיל</MenuItem>
              <MenuItem value="completed">הושלם</MenuItem>
              <MenuItem value="cancelled">בוטל</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>ביטול</Button>
          <Button onClick={handleAddRental} variant="contained">
            הוסף
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Rentals; 