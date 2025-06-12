import sqlite3

# רשימה של רכבים להוספה - כל רכב מכיל מספר רישוי, יצרן ודגם
cars = [
    (f'100-000-0{i}', f'יצרן{i}', f'דגם{i}') for i in range(1, 11)
]

# רשימה של לקוחות להוספה - כל לקוח מכיל ת.ז, שם, טלפון ואימייל
customers = [
    (f'90000000{i}', f'לקוח{i}', f'05000000{i}', f'customer{i}@mail.com') 
    for i in range(1, 11)
]

def add_bulk_data():
    # מוסיף הרבה נתונים בבת אחת לבסיס הנתונים
    conn = sqlite3.connect('rental_system.db')
    c = conn.cursor()
    
    try:
        # מנסה להוסיף את כל הרכבים
        c.executemany(
            'INSERT INTO Vehicle (licensePlate, brand, model) VALUES (?, ?, ?)', 
            cars
        )
    except sqlite3.IntegrityError:
        print('חלק מהרכבים כבר קיימים במערכת')
    
    try:
        # מנסה להוסיף את כל הלקוחות
        c.executemany(
            'INSERT INTO Customer (id, name, phone, email) VALUES (?, ?, ?, ?)', 
            customers
        )
    except sqlite3.IntegrityError:
        print('חלק מהלקוחות כבר קיימים במערכת')
    
    conn.commit()
    conn.close()
    print('נוספו 10 רכבים ו-10 לקוחות למערכת.')

if __name__ == '__main__':
    add_bulk_data() 