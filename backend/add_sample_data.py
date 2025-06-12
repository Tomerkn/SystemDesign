import sqlite3

def add_sample_cars():
    conn = sqlite3.connect('rental_system.db')
    c = conn.cursor()
    
    cars = [
        ('11-222-33', 'רנו', 'קליאו', 2018, 'פנוי'),
        ('12-345-67', 'טויוטה', 'קורולה', 2020, 'פנוי'),
        ('23-456-78', 'הונדה', 'סיוויק', 2021, 'מושכר'),
        ('34-567-89', 'מזדה', '3', 2019, 'בטיפול'),
        ('45-678-90', 'קיה', 'ספורטאז׳', 2022, 'פנוי'),
        ('56-789-01', 'הונדה', 'CR-V', 2021, 'פנוי'),
        ('67-890-12', 'סובארו', 'XV', 2020, 'מושכר'),
        ('78-123-45', 'יונדאי', 'איוניק', 2021, 'מושכר'),
        ('89-234-56', 'סקודה', 'אוקטביה', 2020, 'פנוי'),
        ('90-345-67', 'פיג׳ו', '3008', 2022, 'בטיפול')
    ]
    
    c.executemany('INSERT OR REPLACE INTO Vehicle (licensePlate, brand, model, year, status) VALUES (?, ?, ?, ?, ?)', cars)
    conn.commit()
    conn.close()

def add_sample_rentals():
    conn = sqlite3.connect('rental_system.db')
    c = conn.cursor()
    
    rentals = [
        ('900000001', '11-222-33', '2024-01-01', '2024-01-05', '1000', 'active'),
        ('900000002', '12-345-67', '2024-01-02', '2024-01-07', '1500', 'active'),
        ('900000003', '23-456-78', '2024-01-03', '2024-01-10', '2000', 'completed'),
        ('900000004', '34-567-89', '2024-01-04', '2024-01-08', '1200', 'cancelled'),
        ('900000005', '45-678-90', '2024-01-05', '2024-01-12', '1800', 'active')
    ]
    
    c.executemany('''
        INSERT OR REPLACE INTO Rental 
        (customerId, vehicleId, startDate, endDate, totalPrice, status) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', rentals)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_sample_cars()
    add_sample_rentals() 