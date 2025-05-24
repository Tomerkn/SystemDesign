import sqlite3

cars = [
    (f'100-000-0{i}', f'Brand{i}', f'Model{i}') for i in range(1, 11)
]

customers = [
    (f'90000000{i}', f'לקוח{i}', f'05000000{i}', f'customer{i}@mail.com') for i in range(1, 11)
]

def add_bulk_data():
    conn = sqlite3.connect('rental_system.db')
    c = conn.cursor()
    try:
        c.executemany('INSERT INTO Vehicle (licensePlate, brand, model) VALUES (?, ?, ?)', cars)
    except sqlite3.IntegrityError:
        print('Some cars already exist')
    try:
        c.executemany('INSERT INTO Customer (id, name, phone, email) VALUES (?, ?, ?, ?)', customers)
    except sqlite3.IntegrityError:
        print('Some customers already exist')
    conn.commit()
    conn.close()
    print('Added 10 cars and 10 customers.')

if __name__ == '__main__':
    add_bulk_data() 