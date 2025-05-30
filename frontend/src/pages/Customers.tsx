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
  Alert,
  Snackbar,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { Customer, getCustomers, createCustomer } from '../services/api';

const Customers: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);
  const [newCustomer, setNewCustomer] = useState<Customer>({
    id: '',
    name: '',
    phone: '',
    email: '',
  });

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const response = await getCustomers();
      setCustomers(response.data);
      setError(null);
    } catch (err) {
      setError('שגיאה בטעינת רשימת הלקוחות');
      console.error('Error fetching customers:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setNewCustomer({ id: '', name: '', phone: '', email: '' });
  };

  const handleAddCustomer = async () => {
    try {
      const response = await createCustomer(newCustomer);
      setCustomers([...customers, response.data]);
      handleClose();
      setError(null);
    } catch (err) {
      setError('שגיאה בהוספת לקוח חדש');
      console.error('Error creating customer:', err);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">לקוחות</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleClickOpen}
        >
          הוסף לקוח
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
              <TableCell>ת.ז</TableCell>
              <TableCell>שם</TableCell>
              <TableCell>טלפון</TableCell>
              <TableCell>אימייל</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {customers.map((customer) => (
              <TableRow key={customer.id}>
                <TableCell>{customer.id}</TableCell>
                <TableCell>{customer.name}</TableCell>
                <TableCell>{customer.phone}</TableCell>
                <TableCell>{customer.email}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>הוסף לקוח חדש</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="ת.ז"
            fullWidth
            value={newCustomer.id}
            onChange={(e) =>
              setNewCustomer({ ...newCustomer, id: e.target.value })
            }
          />
          <TextField
            margin="dense"
            label="שם"
            fullWidth
            value={newCustomer.name}
            onChange={(e) =>
              setNewCustomer({ ...newCustomer, name: e.target.value })
            }
          />
          <TextField
            margin="dense"
            label="טלפון"
            fullWidth
            value={newCustomer.phone}
            onChange={(e) =>
              setNewCustomer({ ...newCustomer, phone: e.target.value })
            }
          />
          <TextField
            margin="dense"
            label="אימייל"
            type="email"
            fullWidth
            value={newCustomer.email}
            onChange={(e) =>
              setNewCustomer({ ...newCustomer, email: e.target.value })
            }
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>ביטול</Button>
          <Button onClick={handleAddCustomer} variant="contained">
            הוסף
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Customers; 