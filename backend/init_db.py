import sqlite3  # מייבא את הספרייה שעובדת עם מסד נתונים

def init_db():
    # יוצר את בסיס הנתונים אם הוא לא קיים
    conn = sqlite3.connect('rental_system.db')
    cursor = conn.cursor()

    # קורא את המבנה של בסיס הנתונים מהקובץ schema.sql
    with open('schema.sql', 'r') as f:
        schema = f.read()

    # מריץ את הפקודות שיוצרות את הטבלאות
    cursor.executescript(schema)

    # מוסיף כמה דוגמאות של נתונים לבדיקה
    sample_data = [
        # דוגמאות של לקוחות
        """
        INSERT OR IGNORE INTO Customer (id, name, phone, email) VALUES
        ('123456789', 'ישראל ישראלי', '050-1234567', 'israel@example.com'),
        ('987654321', 'שרה כהן', '052-9876543', 'sarah@example.com')
        """,
        
        # דוגמאות של רכבים
        """
        INSERT OR IGNORE INTO Vehicle (licensePlate, brand, model, status) VALUES
        ('12-345-67', 'טויוטה', 'קורולה', 'available'),
        ('98-765-43', 'יונדאי', 'i35', 'available')
        """
    ]

    # מכניס את הנתונים לטבלאות
    for command in sample_data:
        cursor.execute(command)

    # שומר את השינויים וסוגר את החיבור
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("בסיס הנתונים אותחל בהצלחה!") 