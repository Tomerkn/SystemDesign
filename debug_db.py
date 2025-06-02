import sqlite3

def view_database_contents():
    # מתחבר לבסיס הנתונים
    conn = sqlite3.connect('rental_system.db')
    c = conn.cursor()
    
    print("\n=== לקוחות ===")
    c.execute("SELECT * FROM Customer")
    customers = c.fetchall()
    for customer in customers:
        print(
            f"ת.ז: {customer[0]}, "
            f"שם: {customer[1]}, "
            f"טלפון: {customer[2]}, "
            f"אימייל: {customer[3]}"
        )
    
    print("\n=== רכבים ===")
    c.execute("SELECT * FROM Vehicle")
    vehicles = c.fetchall()
    for vehicle in vehicles:
        print(
            f"מספר רישוי: {vehicle[0]}, "
            f"יצרן: {vehicle[1]}, "
            f"דגם: {vehicle[2]}, "
            f"סטטוס: {vehicle[3]}"
        )
    
    print("\n=== השכרות ===")
    c.execute("SELECT * FROM Rental")
    rentals = c.fetchall()
    for rental in rentals:
        print(
            f"מספר השכרה: {rental[0]}, "
            f"לקוח: {rental[1]}, "
            f"רכב: {rental[2]}, "
            f"מתאריך: {rental[3]}, "
            f"עד תאריך: {rental[4]}"
        )
    
    conn.close()

if __name__ == "__main__":
    # מציג את כל הנתונים בבסיס הנתונים - משמש לבדיקות ודיבוג
    view_database_contents() 