import unittest
import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = "test_rental_system.db"


class TestRentalSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Create tables
        c.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS Customer (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS Vehicle (
                licensePlate TEXT PRIMARY KEY,
                status TEXT DEFAULT 'available' 
                CHECK(status IN ('available', 'rented', 'maintenance'))
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS Rental (
                rentalId INTEGER PRIMARY KEY AUTOINCREMENT,
                customerId TEXT,
                vehicleId TEXT,
                startDate TEXT NOT NULL,
                endDate TEXT NOT NULL,
                FOREIGN KEY (customerId) REFERENCES Customer(id),
                FOREIGN KEY (vehicleId) REFERENCES Vehicle(licensePlate)
            )
        ''')
        
        # Add test data
        c.execute("INSERT INTO Users VALUES (?, ?, ?)", 
                 ('testuser', 'testpass', 'user'))
        c.execute("INSERT INTO Vehicle (licensePlate) VALUES (?)", 
                 ('TEST-123',))
        conn.commit()
        conn.close()

    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up test database
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_register_customer(self):
        # Test customer registration
        self.c.execute("""
            INSERT INTO Customer (id, name, phone, email) 
            VALUES (?, ?, ?, ?)
        """, ('123456789', 'Test User', '0501234567', 'test@test.com'))
        self.conn.commit()
        
        # Verify customer was added
        self.c.execute("SELECT * FROM Customer WHERE id = ?", ('123456789',))
        customer = self.c.fetchone()
        self.assertIsNotNone(customer)
        self.assertEqual(customer[1], 'Test User')

    def test_rent_vehicle(self):
        # Add test customer if not exists
        try:
            self.c.execute("""
                INSERT INTO Customer (id, name, phone, email)
                VALUES (?, ?, ?, ?)
            """, ('999999999', 'Rent Test', '0509999999', 'rent@test.com'))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

        # Test vehicle rental
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        self.c.execute("""
            INSERT INTO Rental (customerId, vehicleId, startDate, endDate)
            VALUES (?, ?, ?, ?)
        """, ('999999999', 'TEST-123', start_date, end_date))
        
        self.c.execute("UPDATE Vehicle SET status = 'rented' WHERE licensePlate = ?",
                      ('TEST-123',))
        self.conn.commit()
        
        # Verify rental was added
        self.c.execute("""
            SELECT * FROM Rental 
            WHERE customerId = ? AND vehicleId = ?
        """, ('999999999', 'TEST-123'))
        rental = self.c.fetchone()
        self.assertIsNotNone(rental)
        
        # Verify vehicle status was updated
        self.c.execute("SELECT status FROM Vehicle WHERE licensePlate = ?",
                      ('TEST-123',))
        status = self.c.fetchone()[0]
        self.assertEqual(status, 'rented')

    def test_return_vehicle(self):
        # Test vehicle return
        self.c.execute("""
            UPDATE Vehicle SET status = 'available' 
            WHERE licensePlate = ?
        """, ('TEST-123',))
        self.conn.commit()
        
        # Verify vehicle status was updated
        self.c.execute("SELECT status FROM Vehicle WHERE licensePlate = ?",
                      ('TEST-123',))
        status = self.c.fetchone()[0]
        self.assertEqual(status, 'available')


if __name__ == '__main__':
    unittest.main() 