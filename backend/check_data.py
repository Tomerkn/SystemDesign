import sqlite3

conn = sqlite3.connect('rental_system.db')
c = conn.cursor()

print('\n=== מדגם לקוחות ===')
c.execute('SELECT * FROM Customer LIMIT 5')
for customer in c.fetchall():
    print(
        f'ת.ז: {customer[0]}, '
        f'שם: {customer[1]}, '
        f'טלפון: {customer[2]}, '
        f'אימייל: {customer[3]}'
    )

print('\n=== מדגם רכבים ===')
c.execute('SELECT * FROM Vehicle LIMIT 5')
for vehicle in c.fetchall():
    print(
        f'מספר רישוי: {vehicle[0]}, '
        f'יצרן: {vehicle[1]}, '
        f'דגם: {vehicle[2]}, '
        f'סטטוס: {vehicle[3]}'
    )

print('\n=== מדגם השכרות ===')
c.execute('''
    SELECT 
        r.rentalId, 
        c.name, 
        v.brand, 
        v.model, 
        r.startDate, 
        r.endDate, 
        r.totalPrice, 
        r.status 
    FROM Rental r 
    JOIN Customer c ON r.customerId = c.id 
    JOIN Vehicle v ON r.vehicleId = v.licensePlate 
    LIMIT 5
''')
for rental in c.fetchall():
    print(
        f'מספר השכרה: {rental[0]}, '
        f'לקוח: {rental[1]}, '
        f'רכב: {rental[2]} {rental[3]}, '
        f'מתאריך: {rental[4]}, '
        f'עד תאריך: {rental[5]}, '
        f'מחיר: {rental[6]}₪, '
        f'סטטוס: {rental[7]}'
    )

conn.close() 