import sqlite3

def view_database_contents():
    conn = sqlite3.connect('rental_system.db')
    c = conn.cursor()
    
    print("\n=== Customers ===")
    c.execute("SELECT * FROM Customer")
    customers = c.fetchall()
    for customer in customers:
        print(f"ID: {customer[0]}, Name: {customer[1]}, Phone: {customer[2]}, Email: {customer[3]}")
    
    print("\n=== Vehicles ===")
    c.execute("SELECT * FROM Vehicle")
    vehicles = c.fetchall()
    for vehicle in vehicles:
        print(f"License: {vehicle[0]}, Brand: {vehicle[1]}, Model: {vehicle[2]}, Status: {vehicle[3]}")
    
    print("\n=== Rentals ===")
    c.execute("SELECT * FROM Rental")
    rentals = c.fetchall()
    for rental in rentals:
        print(f"ID: {rental[0]}, Customer: {rental[1]}, Vehicle: {rental[2]}, Start: {rental[3]}, End: {rental[4]}")
    
    conn.close()

if __name__ == "__main__":
    view_database_contents() 