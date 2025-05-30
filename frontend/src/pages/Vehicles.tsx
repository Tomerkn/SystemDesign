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
import { Vehicle, getVehicles, createVehicle } from '../services/api';

const Vehicles: React.FC = () => {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);
  const [newVehicle, setNewVehicle] = useState<Vehicle>({
    licensePlate: '',
    brand: '',
    model: '',
    status: 'available',
  });

  useEffect(() => {
    fetchVehicles();
  }, []);

  const fetchVehicles = async () => {
    try {
      setLoading(true);
      const response = await getVehicles();
      setVehicles(response.data);
      setError(null);
    } catch (err) {
      setError('שגיאה בטעינת רשימת הרכבים');
      console.error('Error fetching vehicles:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setNewVehicle({
      licensePlate: '',
      brand: '',
      model: '',
      status: 'available',
    });
  };

  const handleAddVehicle = async () => {
    try {
      const response = await createVehicle(newVehicle);
      setVehicles([...vehicles, response.data]);
      handleClose();
      setError(null);
    } catch (err) {
      setError('שגיאה בהוספת רכב חדש');
      console.error('Error creating vehicle:', err);
    }
  };

  const getStatusText = (status: Vehicle['status']) => {
    switch (status) {
      case 'available':
        return 'זמין';
      case 'rented':
        return 'מושכר';
      case 'maintenance':
        return 'בטיפול';
      default:
        return status;
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">רכבים</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleClickOpen}
        >
          הוסף רכב
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
              <TableCell>מספר רישוי</TableCell>
              <TableCell>יצרן</TableCell>
              <TableCell>דגם</TableCell>
              <TableCell>סטטוס</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {vehicles.map((vehicle) => (
              <TableRow key={vehicle.licensePlate}>
                <TableCell>{vehicle.licensePlate}</TableCell>
                <TableCell>{vehicle.brand}</TableCell>
                <TableCell>{vehicle.model}</TableCell>
                <TableCell>{getStatusText(vehicle.status)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>הוסף רכב חדש</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="מספר רישוי"
            fullWidth
            value={newVehicle.licensePlate}
            onChange={(e) =>
              setNewVehicle({ ...newVehicle, licensePlate: e.target.value })
            }
          />
          <TextField
            margin="dense"
            label="יצרן"
            fullWidth
            value={newVehicle.brand}
            onChange={(e) =>
              setNewVehicle({ ...newVehicle, brand: e.target.value })
            }
          />
          <TextField
            margin="dense"
            label="דגם"
            fullWidth
            value={newVehicle.model}
            onChange={(e) =>
              setNewVehicle({ ...newVehicle, model: e.target.value })
            }
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>סטטוס</InputLabel>
            <Select
              value={newVehicle.status}
              label="סטטוס"
              onChange={(e) =>
                setNewVehicle({
                  ...newVehicle,
                  status: e.target.value as Vehicle['status'],
                })
              }
            >
              <MenuItem value="available">זמין</MenuItem>
              <MenuItem value="rented">מושכר</MenuItem>
              <MenuItem value="maintenance">בטיפול</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>ביטול</Button>
          <Button onClick={handleAddVehicle} variant="contained">
            הוסף
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Vehicles; 