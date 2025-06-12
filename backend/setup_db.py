import sqlite3  # מייבא את הספרייה שמאפשרת לנו לעבוד עם בסיס נתונים מסוג SQLite

# כאן אנחנו מגדירים את שם קובץ בסיס הנתונים שבו יאוחסנו כל הנתונים של המערכת
DB_PATH = "rental_system.db"  # שם הקובץ של בסיס הנתונים

# מתחברים לבסיס הנתונים (אם הקובץ לא קיים - הוא ייווצר אוטומטית)
conn = sqlite3.connect(DB_PATH)  # יוצר חיבור לקובץ הנתונים
c = conn.cursor()  # יוצר "סמן" שמאפשר לנו להריץ פקודות SQL

# יוצרים טבלה חדשה בשם SystemUser אם היא לא קיימת כבר
# טבלה זו תשמור את כל המשתמשים שיכולים להיכנס למערכת
c.execute('''
CREATE TABLE IF NOT EXISTS SystemUser (
    userId INTEGER PRIMARY KEY AUTOINCREMENT,  -- עמודה ראשית שמספרת כל משתמש באופן אוטומטי
    username TEXT NOT NULL UNIQUE,             -- שם משתמש (חייב להיות ייחודי, אי אפשר שניים אותו דבר)
    password TEXT NOT NULL,                    -- סיסמה (שדה חובה)
    role TEXT NOT NULL                         -- תפקיד המשתמש (למשל: מנהל)
)
''')  # סוגר את הפקודה

# עכשיו נוסיף שני משתמשים ברירת מחדל: admin ו-user
try:
    c.execute(
        "INSERT INTO SystemUser (username, password, role) VALUES (?, ?, ?)",
        ("admin", "admin", "מנהל")
    )
    print("משתמש admin נוסף!")
except sqlite3.IntegrityError:
    print("המשתמש admin כבר קיים.")

try:
    c.execute(
        "INSERT INTO SystemUser (username, password, role) VALUES (?, ?, ?)",
        ("user", "user", "משתמש")
    )
    print("משתמש user נוסף!")
except sqlite3.IntegrityError:
    print("המשתמש user כבר קיים.")

conn.commit()  # שומרים את כל השינויים שביצענו בבסיס הנתונים
conn.close()  # סוגרים את החיבור לבסיס הנתונים (חשוב כדי לשחרר משאבים) 