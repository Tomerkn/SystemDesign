from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QDialog, QFormLayout,
    QMessageBox, QAbstractItemView, QSizePolicy, QGraphicsOpacityEffect, 
    QCalendarWidget, QDialogButtonBox, QComboBox
)
from PySide6.QtCore import Qt, QSize, QPointF, QDate
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPen, QPolygonF
import sqlite3
import sys
import os
from PySide6.QtCore import QLocale

DB_PATH = "rental_system.db"

# מיפוי סטטוסים לאנגלית -> עברית
STATUS_HE_TO_EN = {
    'available': 'פנוי',
    'rented': 'מושכר',
    'maintenance': 'בטיפול',
    'פנוי': 'פנוי',
    'מושכר': 'מושכר',
    'בטיפול': 'בטיפול',
}

# QSS (CSS-like) styling
QSS = """
/* רקע כללי */
QMainWindow, QWidget#ContentArea {
    background: #f7fafd;
    font-family: 'Segoe UI', 'Arial', sans-serif;
}

/* אזור כותרת ראשית (ברוכים הבאים) */
QWidget#HeaderArea, QWidget#WelcomeHeader, QWidget#welcomeHeader, QWidget#header_widget {
    background: #ffffff;
    border-radius: 22px;
    margin-bottom: 24px;
    padding: 24px 0 18px 0;
}

/* סרגל צד */
QWidget#Sidebar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0038B8, stop:1 #0038B8);
    min-width: 220px;
    max-width: 260px;
    border-right: 2.5px solid #b3c6e0; /* More contrast */
    border-top-left-radius: 18px;
    border-bottom-left-radius: 18px;
    margin: 18px 0 18px 18px; /* Add gap from main content */
    box-shadow: 0 4px 32px 0 rgba(0,56,184,0.10), 2px 0 12px rgba(0,56,184,0.04);
    position: relative;
    z-index: 2;
}

/* רקע בהיר מאחורי הסרגל צד להפרדה */
QWidget#SidebarBg {
    background: #f4f7fb;
    border-radius: 22px;
    margin: 0 0 0 0;
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 1;
}

/* לוגו */
QLabel#LogoLabel {
    color: #fff;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 8px;
    letter-spacing: 1px;
}
QLabel#LogoIcon {
    margin-bottom: 4px;
}

/* כפתורי ניווט */
QPushButton#NavButton {
    color: #ffffff;
    background: transparent;
    border: none;
    font-size: 18px;
    padding: 14px 20px;
    text-align: center;
    border-radius: 10px;
    margin: 4px 8px;
    transition: background 0.2s;
}
QPushButton#NavButton:hover {
    background: #e9f1ff;
    color: #0038B8;
    border-radius: 10px;
}

/* כותרות */
QLabel#HeaderHeadline {
    color: #0038B8;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 8px;
    border-bottom: 4px solid #0038B8;
    padding-bottom: 6px;
    background: transparent;
}
QLabel#HeaderSubtitle {
    color: #0038B8;
    font-size: 18px;
    margin-bottom: 24px;
}

/* כפתור הוספה */
QPushButton#AddButton, QPushButton#ActionBtn {
    color: #fff;
    background: #0038B8;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-size: 18px;
    margin: 18px 0;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(0,56,184,0.06);
    transition: background 0.2s;
}
QPushButton#AddButton:hover, QPushButton#ActionBtn:hover {
    background: #0057B8;
}

/* טבלה */
QTableWidget {
    background: #fff;
    border: 1.5px solid #b3c6e0;
    border-radius: 16px;
    margin: 18px 0;
    gridline-color: #b3c6e0;
    color: #0038B8;
    font-size: 17px;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    box-shadow: 0 2px 12px rgba(0,56,184,0.04);
    width: 100%;
    min-height: 500px;
}
QTableWidget::item {
    padding: 16px 12px;
    font-size: 17px;
    color: #0038B8;
    background: #fff;
    border-bottom: 1px solid #e0e0e0;
}
QTableWidget::item:alternate {
    background: #f7fafd;
}
QTableWidget::item:hover {
    background: #e9f1ff;
    color: #0038B8;
}

/* כותרות טבלה */
QHeaderView::section {
    background: #0038B8;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    border: none;
    border-radius: 0px;
    padding: 16px 12px;
    min-width: 120px;
}

/* כפתורי פעולה בטבלה */
QPushButton[objectName="table_btn_edit"] {
    background: #fff;
    color: #0038B8;
    border: 1.5px solid #0038B8;
    border-radius: 23px;
    font-size: 20px;
    padding: 0;
    margin: 0;
}
QPushButton[objectName="table_btn_edit"]:hover {
    background: #e6f0ff;
}
QPushButton[objectName="table_btn_delete"] {
    background: #fff;
    color: #dc3545;
    border: 1.5px solid #dc3545;
    border-radius: 21px;
    font-size: 18px;
}
QPushButton[objectName="table_btn_delete"]:hover {
    background: #ffebee;
}

/* דיאלוגים */
QDialog {
    background: #fff;
    border-radius: 18px;
}
QDialog QLabel {
    color: #0038B8;
    font-size: 16px;
}
QDialog QLineEdit {
    padding: 10px;
    border: 1px solid #b3c6e0;
    border-radius: 8px;
    background: #fafbfc;
    font-size: 16px;
}
QDialog QPushButton {
    background: #0038B8;
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    margin-top: 10px;
    font-size: 16px;
    font-weight: 600;
}
QDialog QPushButton:hover {
    background: #0057B8;
}

/* כרטיסי סטטיסטיקה */
/* עיצוב חדש עם כחול ישראלי */
QWidget[objectName="StatCard"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0038B8, stop:1 #0038B8);
    border-radius: 18px;
    min-width: 170px;
    max-width: 200px;
    min-height: 110px;
    box-shadow: 0 2px 16px rgba(0,56,184,0.08);
    border: 2px solid #0038B8;
}
QWidget[objectName="StatCard"] QLabel {
    color: #fff;
    font-weight: bold;
}
QWidget[objectName="StatCard"] QLabel[objectName="StatValue"] {
    font-size: 32px;
    font-weight: bold;
    color: #fff;
    background: transparent;
    border: none;
}
QWidget[objectName="StatCard"] QLabel[objectName="StatLabel"] {
    font-size: 18px;
    color: #e9f1ff;
    font-weight: 600;
    background: transparent;
    border: none;
}

/* דף כניסה */
QWidget#LoginWindow {
    background: #f7fafd;
}
QWidget#LoginCard {
    background: #fff;
    border-radius: 22px;
    border: 2px solid #b3c6e0;
    min-width: 400px;
    min-height: 500px;
}
QLabel#LoginTitle {
    color: #0038B8;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 8px;
}
QLabel#LoginSubtitle {
    color: #0038B8;
    font-size: 18px;
    margin-bottom: 24px;
}
QLineEdit#LoginInput {
    padding: 12px;
    border: 1.5px solid #b3c6e0;
    border-radius: 12px;
    background: #fafbfc;
    font-size: 16px;
    min-width: 300px;
}
QPushButton#LoginButton {
    background: #0038B8;
    color: #fff;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-size: 18px;
    font-weight: 600;
    min-width: 300px;
}
QPushButton#LoginButton:hover {
    background: #0057B8;
}
"""

def init_db():
    """יצירת טבלאות במסד הנתונים אם לא קיימות"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # טבלת משתמשים
    c.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # הוספת משתמש מנהל ראשוני אם לא קיים
    c.execute("SELECT COUNT(*) FROM Users")
    if c.fetchone()[0] == 0:
        c.execute("""
            INSERT INTO Users (username, password, full_name, role)
            VALUES (?, ?, ?, ?)
        """, ("admin", "admin", "מנהל מערכת", "admin"))
    
    conn.commit()
    conn.close()

def check_login(username, password):
    """בדיקת התחברות מול מסד הנתונים"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("LoginWindow")
        self.setWindowTitle("גלגל עומר - התחברות")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(QSS)
        
        # יצירת לייאאוט מרכזי
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # כרטיס התחברות
        login_card = QWidget()
        login_card.setObjectName("LoginCard")
        card_layout = QVBoxLayout(login_card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(20)
        
        # לוגו
        logo_label = QLabel("🛞")
        logo_label.setStyleSheet("font-size: 48px;")
        card_layout.addWidget(logo_label, 0, Qt.AlignCenter)
        
        # כותרת
        title_label = QLabel("ברוכים הבאים לגלגל עומר")
        title_label.setObjectName("LoginTitle")
        card_layout.addWidget(title_label, 0, Qt.AlignCenter)
        
        subtitle_label = QLabel("מערכת השכרת רכבים מקצועית")
        subtitle_label.setObjectName("LoginSubtitle")
        card_layout.addWidget(subtitle_label, 0, Qt.AlignCenter)
        
        # שדות התחברות
        self.username_input = QLineEdit()
        self.username_input.setObjectName("LoginInput")
        self.username_input.setPlaceholderText("שם משתמש")
        card_layout.addWidget(self.username_input, 0, Qt.AlignCenter)
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("LoginInput")
        self.password_input.setPlaceholderText("סיסמה")
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input, 0, Qt.AlignCenter)
        
        # כפתור התחברות
        login_button = QPushButton("התחבר")
        login_button.setObjectName("LoginButton")
        login_button.clicked.connect(self.try_login)
        card_layout.addWidget(login_button, 0, Qt.AlignCenter)
        
        layout.addWidget(login_card)
    
    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if check_login(username, password):
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "שגיאה", "שם משתמש או סיסמה שגויים")

def get_customers():  # פונקציה שמביאה את כל הלקוחות מהמסד
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד הנתונים
    c = conn.cursor()  # יוצר סמן כדי לרוץ על המסד
    c.execute(
        "SELECT id, name, phone, email "
        "FROM Customer ORDER BY name"
    )
    customers = c.fetchall()  # שומר את כל התוצאות
    conn.close()  # סוגר את החיבור למסד
    return customers  # מחזיר את הלקוחות שמצאנו

def add_customer(cid, name, phone, email):  # פונקציה שמוסיפה לקוח חדש
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    try:
        c.execute(
            "INSERT INTO Customer (id, name, phone, email) "
            "VALUES (?, ?, ?, ?)",
            (cid, name, phone, email)  # הפרטים של הלקוח
        )
        conn.commit()  # שומר את השינויים
        QMessageBox.information(None, "הצלחה", "הלקוח נוסף בהצלחה!")  # הצגת הודעת הצלחה
        return True, "הלקוח נוסף בהצלחה."  # אומר שהכל סבבה
    except sqlite3.IntegrityError:  # אם יש בעיה (למשל הת.ז כבר קיימת)
        QMessageBox.warning(None, "שגיאה", "הלקוח כבר קיים במערכת.")  # הצגת הודעת שגיאה
        return False, "הלקוח כבר קיים."  # אומר שיש בעיה
    finally:
        conn.close()  # סוגר את החיבור

def update_customer(cid, name, phone, email):  # פונקציה שמעדכנת פרטים של לקוח
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    c.execute(
        "UPDATE Customer SET name=?, phone=?, email=? "
        "WHERE id=?",
        (name, phone, email, cid)
    )
    conn.commit()  # שומר שינויים
    conn.close()  # סוגר חיבור

def delete_customer(cid):  # פונקציה שמוחקת לקוח לפי ת.ז
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    c.execute(
        "DELETE FROM Customer WHERE id=?",
        (cid,)
    )  # מוחק את הלקוח לפי ת.ז
    conn.commit()  # שומר שינויים
    conn.close()  # סוגר חיבור

class CustomerDialog(QDialog):  # חלון קופץ שמאפשר להוסיף או לערוך לקוחות
    def __init__(self, parent=None, data=None):  # הפונקציה שרצה כשיוצרים את החלון
        super().__init__(parent)  # קורא לפונקציה של המחלקה שירשנו ממנה
        self.setWindowTitle("פרטי לקוח")  # שם בכותרת של החלון
        self.setLayout(QFormLayout())  # בוחר תבנית של טופס לסידור
        self.setFixedWidth(350)  # קובע את הרוחב של החלון
        self.setLayoutDirection(Qt.RightToLeft)  # הופך את הכיוון לימין-שמאל
        self.id_edit = QLineEdit()  # יוצר תיבת טקסט לת.ז
        self.name_edit = QLineEdit()  # יוצר תיבת טקסט לשם
        self.phone_edit = QLineEdit()  # יוצר תיבת טקסט לטלפון
        self.email_edit = QLineEdit()  # יוצר תיבת טקסט לאימייל
        self.layout().addRow("ת.ז:", self.id_edit)  # מוסיף שורה עם תווית ותיבת טקסט לת.ז
        self.layout().addRow("שם:", self.name_edit)  # מוסיף שורה עם תווית ותיבת טקסט לשם
        self.layout().addRow("טלפון:", self.phone_edit)  # מוסיף שורה עם תווית ותיבת טקסט לטלפון
        self.layout().addRow("אימייל:", self.email_edit)  # מוסיף שורה עם תווית ותיבת טקסט לאימייל
        if data:  # אם העברנו נתונים (במקרה של עריכה)
            self.id_edit.setText(data[0])  # שם את הת.ז בתיבת הטקסט
            self.id_edit.setDisabled(True)  # לא נותן לשנות את הת.ז
            self.name_edit.setText(data[1])  # שם את השם בתיבת הטקסט
            self.phone_edit.setText(data[2])  # שם את הטלפון בתיבת הטקסט
            self.email_edit.setText(data[3])  # שם את האימייל בתיבת הטקסט
        self.btn = QPushButton("שמור")  # יוצר כפתור שמירה
        self.btn.setObjectName("ActionBtn")  # נותן לכפתור שם כדי לעצב אותו
        self.btn.clicked.connect(self.accept)  # קובע שלחיצה על הכפתור תסגור את החלון בהצלחה
        self.layout().addRow(self.btn)  # מוסיף את כפתור השמירה לטופס
    def get_data(self):  # פונקציה שנותנת את הנתונים שהמשתמש הכניס
        return (
            self.id_edit.text().strip(),  # ת.ז נקייה מרווחים
            self.name_edit.text().strip(),  # שם נקי מרווחים
            self.phone_edit.text().strip(),  # טלפון נקי מרווחים
            self.email_edit.text().strip(),  # אימייל נקי מרווחים
        )

def get_cars():  # פונקציה שמביאה את כל הרכבים
    conn = sqlite3.connect(DB_PATH)  # התחברות למסד
    c = conn.cursor()  # יצירת סמן
    c.execute(
        "SELECT licensePlate, brand, model, year, status "
        "FROM Vehicle ORDER BY licensePlate"
    )  # בחירת כל הרכבים לפי מספר רישוי
    cars = c.fetchall()  # שמירת התוצאות
    conn.close()  # סגירת החיבור
    return cars  # החזרת הרכבים

def add_car(license_plate, brand, model, year, status):  # פונקציה שמוסיפה רכב חדש
    conn = sqlite3.connect(DB_PATH)  # התחברות למסד
    c = conn.cursor()  # יצירת סמן
    try:  # ניסיון להוסיף רכב
        c.execute(
            "INSERT INTO Vehicle (licensePlate, brand, model, year, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (license_plate, brand, model, year, status)  # פרטי הרכב
        )
        conn.commit()  # שמירת השינויים
        QMessageBox.information(None, "הצלחה", "הרכב נוסף בהצלחה!")  # הצגת הודעת הצלחה
        return True, "הרכב נוסף בהצלחה"  # החזרת הצלחה
    except sqlite3.IntegrityError:  # אם יש שגיאה (למשל מספר רישוי כפול)
        QMessageBox.warning(None, "שגיאה", "הרכב כבר קיים במערכת.")  # הצגת הודעת שגיאה
        return False, "הרכב כבר קיים"  # החזרת שגיאה
    finally:
        conn.close()  # סגירת החיבור

def update_car(license_plate, brand, model, year, status):  # פונקציה שמעדכנת רכב
    conn = sqlite3.connect(DB_PATH)  # התחברות למסד
    c = conn.cursor()  # יצירת סמן
    c.execute(
        "UPDATE Vehicle SET brand=?, model=?, year=?, status=? "
        "WHERE licensePlate=?",
        (brand, model, year, status, license_plate)  # הפרטים החדשים
    )
    conn.commit()  # שמירת השינויים
    conn.close()  # סגירת החיבור

def delete_car(license_plate):  # פונקציה שמוחקת רכב
    conn = sqlite3.connect(DB_PATH)  # התחברות למסד
    c = conn.cursor()  # יצירת סמן
    c.execute(
        "DELETE FROM Vehicle WHERE licensePlate=?",
        (license_plate,)
    )  # מחיקת הרכב
    conn.commit()  # שמירת השינויים
    conn.close()  # סגירת החיבור

class CarDialog(QDialog):  # חלון קופץ לעריכת רכב
    def __init__(self, parent=None, data=None):  # אתחול החלון
        super().__init__(parent)  # קריאה למחלקת האב
        self.setWindowTitle("פרטי רכב")  # כותרת החלון
        self.setLayout(QFormLayout())  # סידור הטופס
        self.setFixedWidth(350)  # רוחב קבוע
        self.setLayoutDirection(Qt.RightToLeft)  # כיוון מימין לשמאל
        
        # יצירת שדות הקלט
        self.plate_edit = QLineEdit()  # שדה מספר רישוי
        self.brand_edit = QLineEdit()  # שדה יצרן
        self.model_edit = QLineEdit()  # שדה דגם
        self.year_edit = QLineEdit()  # שדה שנת ייצור
        self.status_edit = QLineEdit()  # שדה סטטוס
        
        # הוספת השדות לטופס
        self.layout().addRow("מספר רכב:", self.plate_edit)
        self.layout().addRow("יצרן:", self.brand_edit)
        self.layout().addRow("דגם:", self.model_edit)
        self.layout().addRow("שנת ייצור:", self.year_edit)
        self.layout().addRow("סטטוס:", self.status_edit)
        
        if data:  # אם יש נתונים (במקרה של עריכה)
            self.plate_edit.setText(data[0])  # מילוי מספר רישוי
            self.plate_edit.setDisabled(True)  # נעילת שדה מספר רישוי
            self.brand_edit.setText(data[1])  # מילוי יצרן
            self.model_edit.setText(data[2])  # מילוי דגם
            self.year_edit.setText(str(data[3]))  # מילוי שנת ייצור
            self.status_edit.setText(data[4])  # מילוי סטטוס
        
        # כפתור שמירה
        self.btn = QPushButton("שמור")
        self.btn.setObjectName("ActionBtn")
        self.btn.clicked.connect(self.accept)
        self.layout().addRow(self.btn)

    def get_data(self):  # קבלת הנתונים מהטופס
        return (
            self.plate_edit.text().strip(),  # מספר רישוי
            self.brand_edit.text().strip(),  # יצרן
            self.model_edit.text().strip(),  # דגם
            self.year_edit.text().strip(),  # שנת ייצור
            self.status_edit.text().strip(),  # סטטוס
        )

def get_rentals():
    """קבלת כל ההשכרות ממסד הנתונים"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                r.rentalId,
                r.customerId,
                r.vehicleId,
                r.startDate,
                r.endDate,
                r.totalPrice,
                r.status
            FROM Rental r
            ORDER BY r.rentalId DESC
        """)
        
        rentals = []
        for row in cursor.fetchall():
            rentals.append({
                "rentalId": row[0],
                "customerId": row[1],
                "vehicleId": row[2],
                "startDate": row[3],
                "endDate": row[4],
                "totalPrice": row[5],
                "status": row[6]
            })
        
        conn.close()
        return rentals
    except Exception as e:
        print(f"Error getting rentals: {e}")
        return []

def add_rental(customer_id, vehicle_id, start_date, end_date, total_price, status):  # פונקציה שמוסיפה השכרה חדשה
    conn = sqlite3.connect(DB_PATH)  # התחברות למסד
    c = conn.cursor()  # יצירת סמן
    try:  # ניסיון להוסיף השכרה
        c.execute(
            "INSERT INTO Rental (customerId, vehicleId, startDate, endDate, totalPrice, status) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (customer_id, vehicle_id, start_date, end_date, total_price, status)  # פרטי ההשכרה
        )
        conn.commit()  # שמירת השינויים
        QMessageBox.information(None, "הצלחה", "ההשכרה נוספה בהצלחה!")  # הצגת הודעת הצלחה
        return True, "ההשכרה נוספה בהצלחה"  # החזרת הצלחה
    except sqlite3.IntegrityError:  # אם יש שגיאה
        QMessageBox.warning(None, "שגיאה", "ההשכרה כבר קיימת במערכת.")  # הצגת הודעת שגיאה
        return False, "ההשכרה כבר קיימת"  # החזרת שגיאה
    finally:
        conn.close()  # סגירת החיבור

def update_rental(rental_id, customer_id, vehicle_id, start_date, end_date, total_price, status):
    """עדכון השכרה קיימת במסד הנתונים"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE Rental
            SET 
                customerId = ?,
                vehicleId = ?,
                startDate = ?,
                endDate = ?,
                totalPrice = ?,
                status = ?
            WHERE rentalId = ?
        """, (
            customer_id,
            vehicle_id,
            start_date,
            end_date,
            total_price,
            status,
            rental_id
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating rental: {e}")
        return False

def delete_rental(rental_id):
    """מחיקת השכרה ממסד הנתונים"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM Rental
            WHERE rentalId = ?
        """, (rental_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting rental: {e}")
        return False

class RentalDialog(QDialog):  # חלון קופץ לעריכת השכרה
    def __init__(self, parent=None, data=None):  # אתחול החלון
        super().__init__(parent)  # קריאה למחלקת האב
        self.setWindowTitle("פרטי השכרה")  # כותרת החלון
        self.setLayout(QFormLayout())  # סידור הטופס
        self.setFixedWidth(350)  # רוחב קבוע
        self.setLayoutDirection(Qt.RightToLeft)  # כיוון מימין לשמאל
        
        # יצירת שדות הקלט
        self.customer_id_edit = QLineEdit()  # שדה ת.ז לקוח
        self.vehicle_id_edit = QLineEdit()  # שדה מספר רישוי
        self.start_date_edit = QLineEdit()  # שדה תאריך התחלה
        self.end_date_edit = QLineEdit()  # שדה תאריך סיום
        self.total_price_edit = QLineEdit()  # שדה מחיר כולל
        self.status_edit = QLineEdit()  # שדה סטטוס
        
        # הוספת השדות לטופס
        self.layout().addRow("ת.ז לקוח:", self.customer_id_edit)
        self.layout().addRow("מספר רכב:", self.vehicle_id_edit)
        self.layout().addRow("תאריך התחלה:", self.start_date_edit)
        self.layout().addRow("תאריך סיום:", self.end_date_edit)
        self.layout().addRow("מחיר כולל:", self.total_price_edit)
        self.layout().addRow("סטטוס:", self.status_edit)
        
        if data:  # אם יש נתונים (במקרה של עריכה)
            self.customer_id_edit.setText(str(data[1]))  # מילוי ת.ז לקוח
            self.vehicle_id_edit.setText(data[3])  # מילוי מספר רישוי
            self.start_date_edit.setText(data[6])  # מילוי תאריך התחלה
            self.end_date_edit.setText(data[7])  # מילוי תאריך סיום
            self.total_price_edit.setText(str(data[8]))  # מילוי מחיר כולל
            self.status_edit.setText(data[9])  # מילוי סטטוס
        
        # כפתור שמירה
        self.btn = QPushButton("שמור")
        self.btn.setObjectName("ActionBtn")
        self.btn.clicked.connect(self.accept)
        self.layout().addRow(self.btn)

    def get_data(self):  # קבלת הנתונים מהטופס
        return (
            self.customer_id_edit.text().strip(),  # ת.ז לקוח
            self.vehicle_id_edit.text().strip(),  # מספר רישוי
            self.start_date_edit.text().strip(),  # תאריך התחלה
            self.end_date_edit.text().strip(),  # תאריך סיום
            self.total_price_edit.text().strip(),  # מחיר כולל
            self.status_edit.text().strip(),  # סטטוס
        )

def get_stats():  # פונקציה שמביאה נתונים סטטיסטיים
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    
    c.execute("SELECT COUNT(*) FROM Customer")  # סופר כמה לקוחות יש
    customers = c.fetchone()[0]  # שומר את המספר
    
    c.execute("SELECT COUNT(*) FROM Vehicle")  # סופר כמה רכבים יש
    cars = c.fetchone()[0]  # שומר את המספר
    
    c.execute("SELECT COUNT(*) FROM Rental")  # סופר כמה השכרות יש
    rentals = c.fetchone()[0]  # שומר את המספר
    
    c.execute(
        "SELECT COUNT(*) FROM Rental "
        "WHERE endDate < date('now')"
    )  # סופר כמה השכרות הסתיימו
    late = c.fetchone()[0]  # שומר את המספר
    
    conn.close()  # סוגר חיבור
    return customers, cars, rentals, late  # מחזיר את כל המספרים

class IsraeliFlagWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setFixedSize(120, 80)
        self.setStyleSheet("background: transparent;")
        opacity = QGraphicsOpacityEffect(self)
        opacity.setOpacity(0.85)
        self.setGraphicsEffect(opacity)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw two thin white stripes (lines) with no fill
        painter.setPen(QPen(Qt.white, 1.5))  # Thin white outline
        painter.setBrush(Qt.NoBrush)
        y1 = 15
        y2 = self.height() - 15
        painter.drawLine(10, y1, self.width() - 10, y1)
        painter.drawLine(10, y2, self.width() - 10, y2)
        
        # Draw Magen David (Star of David)
        painter.setPen(QPen(Qt.white, 1.5))  # Thinner white outline
        painter.setBrush(Qt.NoBrush)  # No fill, just outline
        center_x = self.width() // 2
        center_y = self.height() // 2 + 4
        r = 18
        # Upward triangle
        points_up = [
            QPointF(center_x, center_y - r),
            QPointF(center_x - r * 0.866, center_y + r * 0.5),
            QPointF(center_x + r * 0.866, center_y + r * 0.5)
        ]
        painter.drawPolygon(QPolygonF(points_up))
        # Downward triangle
        points_down = [
            QPointF(center_x, center_y + r),
            QPointF(center_x - r * 0.866, center_y - r * 0.5),
            QPointF(center_x + r * 0.866, center_y - r * 0.5)
        ]
        painter.drawPolygon(QPolygonF(points_down))

def myFunc(self):
    pass

class MainWindow(QMainWindow):  # חלון ראשי של האפליקציה
    def __init__(self):  # אתחול החלון
        super().__init__()  # קריאה למחלקת האב
        self.setWindowTitle("מערכת השכרת רכב")  # כותרת החלון
        self.setMinimumSize(1200, 800)  # גודל מינימלי
        self.setStyleSheet(QSS)  # הגדרת סגנון
        
        # יצירת תפריט עליון
        self.menu_bar = self.menuBar()  # יצירת סרגל תפריט
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background: #fff;
                border-bottom: 1px solid #b3c6e0;
                padding: 4px 0;
            }
            QMenuBar::item {
                padding: 6px 12px;
                color: #0038B8;
            }
            QMenuBar::item:selected {
                background: #e6f0ff;
                border-radius: 4px;
            }
        """)
        
        # תפריט לקוחות
        self.customer_menu = self.menu_bar.addMenu("לקוחות")
        self.customer_menu.addAction("הוסף לקוח", self.add_customer)
        self.customer_menu.addAction("ערוך לקוח", self.edit_customer)
        self.customer_menu.addAction("מחק לקוח", self.delete_customer)
        
        # תפריט רכבים
        self.car_menu = self.menu_bar.addMenu("רכבים")
        self.car_menu.addAction("הוסף רכב", self.add_car)
        self.car_menu.addAction("ערוך רכב", self.edit_car)
        self.car_menu.addAction("מחק רכב", self.delete_car)
        
        # תפריט השכרות
        self.rental_menu = self.menu_bar.addMenu("השכרות")
        self.rental_menu.addAction("הוסף השכרה", self.add_rental)
        self.rental_menu.addAction("ערוך השכרה", self.edit_rental)
        self.rental_menu.addAction("מחק השכרה", self.delete_rental)
        
        # יצירת אזור תוכן ראשי
        self.central_widget = QWidget()  # יצירת ווידג'ט מרכזי
        self.setCentralWidget(self.central_widget)  # הגדרת הווידג'ט המרכזי
        self.main_layout = QHBoxLayout(self.central_widget)  # סידור אופקי
        
        # יצירת סרגל צד
        self.sidebar = QWidget()  # יצירת ווידג'ט לסרגל צד
        self.sidebar.setObjectName("Sidebar")  # הגדרת שם לאובייקט
        self.sidebar.setFixedWidth(220)  # רוחב קבוע
        self.sidebar_layout = QVBoxLayout(self.sidebar)  # סידור אנכי
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)  # ביטול שוליים
        self.sidebar_layout.setSpacing(0)  # ביטול מרווחים
        
        # הוספת שם החברה
        company_label = QLabel("גלגל עומר")
        company_label.setObjectName("CompanyName")
        company_label.setStyleSheet("""
            QLabel#CompanyName {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                text-align: center;
                background: transparent;
            }
        """)
        self.sidebar_layout.addWidget(company_label)
        
        # יצירת כפתורים בסרגל הצד
        nav_buttons = [
            ("תפריט ראשי", self.show_dashboard),
            ("לקוחות", self.show_customers),
            ("רכבים", self.show_cars),
            ("השכרות", self.show_rentals)
        ]
        
        for text, callback in nav_buttons:
            btn = QPushButton(text)
            btn.setObjectName("NavButton")
            btn.setStyleSheet("""
                QPushButton#NavButton {
                    color: #ffffff;
                    background: transparent;
                    border: none;
                    font-size: 18px;
                    padding: 14px 20px;
                    text-align: center;
                    border-radius: 10px;
                    margin: 4px 8px;
                }
                QPushButton#NavButton:hover {
                    background: #e9f1ff;
                    color: #0038B8;
                    border-radius: 10px;
                }
            """)
            btn.clicked.connect(callback)
            self.sidebar_layout.addWidget(btn)
        
        self.sidebar_layout.addStretch()  # הוספת מרווח גמיש
        
        # יצירת אזור תוכן
        self.content_area = QWidget()  # יצירת ווידג'ט לאזור תוכן
        self.content_area.setObjectName("ContentArea")  # הגדרת שם לאובייקט
        self.content_layout = QVBoxLayout(self.content_area)  # סידור אנכי
        
        # הוספת האזורים לחלון הראשי
        self.main_layout.addWidget(self.sidebar)  # הוספת סרגל צד
        self.main_layout.addWidget(self.content_area)  # הוספת אזור תוכן
        
        # הצגת מסך ברירת מחדל
        self.show_dashboard()  # הצגת מסך ראשי במקום מסך לקוחות

    def setup_sidebar(self, main_layout):
        """הגדרת סרגל הצד"""
        self.sidebar = QWidget()  
        self.sidebar.setObjectName("Sidebar")  
        self.sidebar.setFixedWidth(220)  
        sidebar_layout = QVBoxLayout(self.sidebar)  
        sidebar_layout.setContentsMargins(10, 20, 10, 20)  

        # לוגו
        self.setup_logo(sidebar_layout)
        
        # כפתורי ניווט
        self.setup_nav_buttons(sidebar_layout)
        
        # דגל ישראל
        self.setup_flag(sidebar_layout)
        
        main_layout.addWidget(self.sidebar)

    def setup_logo(self, sidebar_layout):
        """הגדרת הלוגו"""
        logo_icon = QLabel()  
        logo_icon.setObjectName("LogoIcon")
        logo_pixmap = QPixmap(os.path.join("icons", "png", "car_logo.png"))
        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(
                44, 44, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_icon.setPixmap(scaled_pixmap)

        logo_label = QLabel("גלגל עומר")
        logo_label.setObjectName("LogoLabel")

        sidebar_layout.addWidget(logo_icon, 0, Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label, 0, Qt.AlignCenter)
        sidebar_layout.addSpacing(20)  

    def setup_nav_buttons(self, sidebar_layout):
        """הגדרת כפתורי הניווט"""
        nav_buttons = [
            ("ראשי", "dashboard.png", self.show_dashboard),
            ("לקוחות", "people.png", self.show_customers),
            ("רכבים", "directions_car.png", self.show_cars),
            ("השכרות", "assignment.png", self.show_rentals)
        ]
        
        for text, icon, callback in nav_buttons:
            btn = QPushButton(f" {text}")
            btn.setObjectName("NavButton")
            icon_path = os.path.join("icons", "png", icon)
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(28, 28))
            btn.clicked.connect(callback)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()  

    def setup_flag(self, sidebar_layout):
        """הגדרת דגל ישראל"""
        self.flag_widget = IsraeliFlagWidget(self.sidebar)
        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(
            self.flag_widget, 0, Qt.AlignHCenter | Qt.AlignBottom
        )
        self.flag_widget.show()

    def setup_content_area(self, main_layout):
        """הגדרת אזור התוכן"""
        self.content = QWidget()
        self.content.setObjectName("ContentArea")
        self.content.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)
        main_layout.addWidget(self.content, 1)

    def clear_content(self):  # פונקציה שמנקה את אזור התוכן
        for i in reversed(range(self.content_layout.count())):  
            widget = self.content_layout.itemAt(i).widget()  
            if widget:  
                widget.setParent(None)  

    def show_dashboard(self):  # פונקציה שמציגה את המסך הראשי
        self.clear_content()  
        
        # הגדרת כותרת
        header_widget = self.setup_dashboard_header()
        self.content_layout.addWidget(header_widget)
        
        # הגדרת כרטיסי סטטיסטיקה
        stats_widget = self.setup_dashboard_stats()
        self.content_layout.addWidget(stats_widget)

    def setup_dashboard_header(self):
        """הגדרת כותרת הדשבורד"""
        header_widget = QWidget()  
        header_layout = QVBoxLayout(header_widget)  
        header_layout.setContentsMargins(0, 0, 0, 0)  
        
        headline = QLabel(
            "ברוכים הבאים למערכת השכרת הרכבים של גלגל עומר בע״מ"
        )  
        headline.setObjectName("HeaderHeadline")  
        headline.setAlignment(Qt.AlignCenter)  
        
        subtitle = QLabel(
            "מערכת השכרת רכבים מקצועית, קלה ונוחה לשימוש"
        )  
        subtitle.setObjectName("HeaderSubtitle")  
        subtitle.setAlignment(Qt.AlignCenter)  
        
        header_layout.addStretch(1)  
        header_layout.addWidget(headline)  
        header_layout.addSpacing(2)  
        header_layout.addWidget(subtitle)  
        header_layout.addStretch(1)  
        
        return header_widget

    def setup_dashboard_stats(self):
        """הגדרת כרטיסי הסטטיסטיקה"""
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setContentsMargins(40, 20, 40, 20)
        stats_layout.setSpacing(30)
        
        # קבלת נתונים סטטיסטיים
        customers, cars, rentals, late = get_stats()
        
        # יצירת כרטיסי סטטיסטיקה
        stat_cards = [
            ("לקוחות", "people.png", str(customers)),
            ("רכבים", "directions_car.png", str(cars)),
            ("השכרות", "assignment.png", str(rentals)),
            ("מאחרים", "warning.png", str(late))
        ]
        
        for label, icon, value in stat_cards:
            card = self.create_stat_card(label, icon, value)
            stats_layout.addWidget(card)
        
        return stats_widget

    def create_stat_card(self, label, icon_name, value):  
        """יצירת כרטיס סטטיסטיקה בודד"""
        card = QWidget()  
        card.setObjectName("StatCard")  
        card.setStyleSheet("")  
        
        layout = QVBoxLayout(card)  
        layout.setAlignment(Qt.AlignCenter)  
        layout.setSpacing(8)  
        
        # הגדרת האייקון
        icon_label = self.create_stat_icon(icon_name)
        layout.addWidget(icon_label)
        
        # הגדרת הערך המספרי
        value_label = self.create_stat_value(value)
        layout.addWidget(value_label)
        
        # הגדרת התווית
        text_label = self.create_stat_text(label)
        layout.addWidget(text_label)
        
        return card

    def create_stat_icon(self, icon_name):
        """יצירת אייקון לכרטיס סטטיסטיקה"""
        icon_label = QLabel()  
        icon_label.setStyleSheet("background: transparent; border: none;")  
        
        icon_path = os.path.join("icons", "png", icon_name)  
        if os.path.exists(icon_path):  
            icon_pixmap = QPixmap(icon_path)  
            scaled_pixmap = icon_pixmap.scaled(
                36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            icon_label.setPixmap(scaled_pixmap)  
        else:  
            icon_label.setText("🛈")  
        
        icon_label.setAlignment(Qt.AlignCenter)  
        return icon_label

    def create_stat_value(self, value):
        """יצירת תווית ערך לכרטיס סטטיסטיקה"""
        value_label = QLabel(value)  
        value_label.setObjectName("StatValue")  
        value_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #fff;
            background: transparent;
            border: none;
        """)  
        value_label.setAlignment(Qt.AlignCenter)  
        return value_label

    def create_stat_text(self, text):
        """יצירת תווית טקסט לכרטיס סטטיסטיקה"""
        text_label = QLabel(text)  
        text_label.setObjectName("StatLabel")  
        text_label.setStyleSheet("""
            font-size: 18px;
            color: #e6f0ff;
            font-weight: 600;
            background: transparent;
            border: none;
        """)  
        text_label.setAlignment(Qt.AlignCenter)  
        return text_label

    def setup_table(self, table):
        """הגדרת עיצוב אחיד לכל הטבלאות"""
        # הגדרות בסיסיות
        self.setup_table_basic_settings(table)
        
        # הגדרות עיצוב
        self.setup_table_style(table)
        
        # קביעת רוחב העמודות
        self.setup_table_column_widths(table)

    def setup_table_basic_settings(self, table):
        """הגדרת הגדרות בסיסיות לטבלה"""
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        table.setLayoutDirection(Qt.RightToLeft)
        
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        table.horizontalHeader().setStretchLastSection(True)
        table.setWordWrap(True)
        table.verticalHeader().setDefaultSectionSize(50)

    def setup_table_style(self, table):
        """הגדרת עיצוב לטבלה"""
        table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1.5px solid #b3c6e0;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background: #e6f0ff;
                color: #0038B8;
            }
            QHeaderView::section {
                background: #0038B8;
                color: white;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-right: 1px solid #ffffff;
            }
            QHeaderView::section:last {
                border-right: none;
                border-top-right-radius: 8px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
        """)

    def setup_table_column_widths(self, table):
        """קביעת רוחב העמודות בטבלה"""
        column_widths = {
            "מספר רכב": 100,
            "יצרן": 120,
            "דגם": 140,
            "שנת ייצור": 80,
            "סטטוס": 80,
            "ת.ז לקוח": 100,
            "שם": 180,
            "טלפון": 120,
            "אימייל": 200,
            "תאריך התחלה": 120,
            "תאריך סיום": 120,
            "מספר השכרה": 100,
            "פעולות": 100
        }
        
        for i in range(table.columnCount()):
            header = table.horizontalHeaderItem(i)
            if header:
                header_text = header.text()
                width = column_widths.get(header_text, 120)
                table.setColumnWidth(i, width)

    def show_customers(self):
        """הצגת מסך ניהול לקוחות"""
        self.clear_content()
        
        # הגדרת כותרת
        header_widget = self.setup_customers_header()
        self.content_layout.addWidget(header_widget)
        
        # כפתור הוספה
        add_btn = self.create_add_button("הוסף לקוח חדש", self.add_customer)
        self.content_layout.addWidget(add_btn, 0, Qt.AlignCenter)
        
        # טבלה
        self.table = QTableWidget()
        self.setup_table(self.table)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ת.ז", "שם", "טלפון", "אימייל", "פעולות"
        ])
        
        self.content_layout.addWidget(self.table)
        self.load_customers()

    def setup_customers_header(self):
        """הגדרת כותרת למסך לקוחות"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 20)
        
        headline = QLabel("ניהול לקוחות")
        headline.setObjectName("HeaderHeadline")
        headline.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("הוספה, עריכה, חיפוש ומחיקה של לקוחות")
        subtitle.setObjectName("HeaderSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(headline)
        header_layout.addWidget(subtitle)
        
        return header_widget

    def create_add_button(self, text, callback):
        """יצירת כפתור הוספה"""
        btn = QPushButton(text)
        btn.setObjectName("AddButton")
        btn.setIcon(QIcon(os.path.join("icons", "png", "add.png")))
        btn.setIconSize(QSize(16, 16))
        btn.clicked.connect(callback)
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def load_customers(self):
        """טעינת נתוני הלקוחות לטבלה"""
        self.table.setRowCount(0)
        customers = get_customers()
        
        for row, customer in enumerate(customers):
            self.table.insertRow(row)
            # הוספת נתוני הלקוח (ת.ז, שם, טלפון, אימייל)
            for col, value in enumerate(customer):
                item = QTableWidgetItem(str(value))
                item.setForeground(Qt.black)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
            # הוספת כפתורי פעולה
            action_widget = self.create_action_buttons(
                row, self.edit_customer, self.delete_customer
            )
            self.table.setCellWidget(row, 4, action_widget)
            self.table.setRowHeight(row, 60)

    def edit_customer(self, row):
        """עריכת לקוח"""
        customer_id = self.table.item(row, 0).text()
        customer_name = self.table.item(row, 1).text()
        customer_phone = self.table.item(row, 2).text()
        customer_email = self.table.item(row, 3).text()
        
        dialog = CustomerDialog(self, (customer_id, customer_name, customer_phone, customer_email))
        if dialog.exec_():
            cid, name, phone, email = dialog.get_data()
            update_customer(cid, name, phone, email)
            self.load_customers()

    def delete_customer(self, row):
        """מחיקת לקוח"""
        customer_id = self.table.item(row, 0).text()
        customer_name = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "אישור מחיקה",
            f"האם אתה בטוח שברצונך למחוק את הלקוח {customer_name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            delete_customer(customer_id)
            self.load_customers()

    def add_customer(self):
        """הוספת לקוח חדש"""
        dialog = CustomerDialog(self)
        if dialog.exec_():
            cid, name, phone, email = dialog.get_data()
            success, message = add_customer(cid, name, phone, email)
            if not success:
                QMessageBox.warning(self, "שגיאה", message)
            else:
                self.load_customers()

    def create_action_buttons(self, row, edit_callback, delete_callback):
        """פונקציה כללית ליצירת כפתורי פעולה"""
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(4, 4, 4, 4)
        action_layout.setSpacing(8)
        
        edit_btn = QPushButton("✎")
        edit_btn.setObjectName("table_btn_edit")
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.setToolTip("ערוך")
        edit_btn.setFixedSize(28, 28)
        edit_btn.clicked.connect(lambda: edit_callback(row))
        
        del_btn = QPushButton("×")
        del_btn.setObjectName("table_btn_delete")
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setToolTip("מחק")
        del_btn.setFixedSize(28, 28)
        del_btn.clicked.connect(lambda: delete_callback(row))
        
        action_layout.addWidget(edit_btn)
        action_layout.addWidget(del_btn)
        action_layout.setAlignment(Qt.AlignCenter)
        
        action_widget.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
            }
            QPushButton {
                min-width: 28px;
                min-height: 28px;
                max-width: 28px;
                max-height: 28px;
                padding: 0px;
                border-radius: 14px;
                font-size: 16px;
                margin: 0px 2px;
                font-weight: bold;
            }
            QPushButton[objectName="table_btn_edit"] {
                background: #ffffff;
                color: #0038B8;
                border: 1.5px solid #0038B8;
            }
            QPushButton[objectName="table_btn_edit"]:hover {
                background: #e6f0ff;
                color: #0057B8;
            }
            QPushButton[objectName="table_btn_delete"] {
                background: #ffffff;
                color: #dc3545;
                border: 1.5px solid #dc3545;
            }
            QPushButton[objectName="table_btn_delete"]:hover {
                background: #ffebee;
                color: #ff4136;
            }
        """)
        
        return action_widget

    def show_cars(self):
        """הצגת מסך ניהול רכבים"""
        self.clear_content()
        
        # הגדרת כותרת
        header_widget = self.setup_cars_header()
        self.content_layout.addWidget(header_widget)
        
        # כפתור הוספה
        add_btn = self.create_add_button("הוסף רכב חדש", self.add_car)
        self.content_layout.addWidget(add_btn, 0, Qt.AlignCenter)
        
        # טבלה
        self.table = QTableWidget()
        self.setup_table(self.table)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "מספר רכב", "יצרן", "דגם", "שנת ייצור", "סטטוס", "פעולות"
        ])
        
        self.content_layout.addWidget(self.table)
        self.load_cars()

    def setup_cars_header(self):
        """הגדרת כותרת למסך רכבים"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 20)
        
        headline = QLabel("ניהול רכבים")
        headline.setObjectName("HeaderHeadline")
        headline.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("הוספה, עריכה, חיפוש ומחיקה של רכבים")
        subtitle.setObjectName("HeaderSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(headline)
        header_layout.addWidget(subtitle)
        
        return header_widget

    def load_cars(self):
        """טעינת נתוני הרכבים לטבלה"""
        self.table.setRowCount(0)
        cars = get_cars()
        
        for row, car in enumerate(cars):
            self.table.insertRow(row)
            
            # הוספת נתוני הרכב
            for col, value in enumerate(car):
                if col == 4:  # עמודת סטטוס
                    value = STATUS_HE_TO_EN.get(str(value).lower(), str(value))
                if col < 5:  # לא כולל את עמודת הפעולות
                    item = QTableWidgetItem(str(value))
                    item.setForeground(Qt.black)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row, col, item)
            
            # הוספת כפתורי פעולה
            action_widget = self.create_action_buttons(
                row, self.edit_car, self.delete_car
            )
            self.table.setCellWidget(row, 5, action_widget)
            self.table.setRowHeight(row, 60)

    def create_car_dialog(self, title, license_plate="", brand="", model="", year="", status=""):
        """יצירת דיאלוג לרכב"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # שדות הקלט
        dialog.plate_edit = QLineEdit(license_plate, dialog)
        dialog.plate_edit.setPlaceholderText("הכנס מספר רישוי")
        
        dialog.brand_edit = QLineEdit(brand, dialog)
        dialog.brand_edit.setPlaceholderText("הכנס יצרן")
        
        dialog.model_edit = QLineEdit(model, dialog)
        dialog.model_edit.setPlaceholderText("הכנס דגם")
        
        dialog.year_edit = QLineEdit(str(year), dialog)
        dialog.year_edit.setPlaceholderText("הכנס שנת ייצור")
        
        dialog.status_edit = QLineEdit(status, dialog)
        dialog.status_edit.setPlaceholderText("הכנס סטטוס")
        
        # הוספת השדות לטופס
        layout.addRow("מספר רכב:", dialog.plate_edit)
        layout.addRow("יצרן:", dialog.brand_edit)
        layout.addRow("דגם:", dialog.model_edit)
        layout.addRow("שנת ייצור:", dialog.year_edit)
        layout.addRow("סטטוס:", dialog.status_edit)
        
        # כפתורי פעולה
        btn_box = self.create_dialog_buttons(dialog)
        layout.addRow(btn_box)
        
        return dialog

    def add_car(self):
        """פתיחת דיאלוג להוספת רכב חדש"""
        dialog = self.create_car_dialog("הוספת רכב חדש")
        
        if dialog.exec() == QDialog.Accepted:
            # קבלת הנתונים מהדיאלוג
            license_plate = dialog.plate_edit.text().strip()
            brand = dialog.brand_edit.text().strip()
            model = dialog.model_edit.text().strip()
            year = dialog.year_edit.text().strip()
            status = dialog.status_edit.text().strip()
            
            # בדיקת תקינות
            if not all([license_plate, brand, model, year, status]):
                self.show_error("שגיאה", "יש למלא את כל השדות")
                return
            
            # הוספת הרכב למסד הנתונים
            success, message = add_car(license_plate, brand, model, year, status)
            if success:
                self.show_success("הצלחה", "הרכב נוסף בהצלחה")
                self.load_cars()
            else:
                self.show_error("שגיאה", message)

    def edit_car(self, row):
        """פתיחת דיאלוג לעריכת רכב קיים"""
        # קבלת נתוני הרכב הנוכחי
        plate = self.table.item(row, 0).text()
        brand = self.table.item(row, 1).text()
        model = self.table.item(row, 2).text()
        year = self.table.item(row, 3).text()
        status = self.table.item(row, 4).text()
        
        # יצירת הדיאלוג
        dialog = self.create_car_dialog(
            "עריכת רכב",
            plate, brand, model, year, status
        )
        
        if dialog.exec() == QDialog.Accepted:
            # קבלת הנתונים החדשים
            new_plate = dialog.plate_edit.text().strip()
            new_brand = dialog.brand_edit.text().strip()
            new_model = dialog.model_edit.text().strip()
            new_year = dialog.year_edit.text().strip()
            new_status = dialog.status_edit.text().strip()
            
            # בדיקת תקינות
            if not all([new_plate, new_brand, new_model, new_year, new_status]):
                self.show_error("שגיאה", "יש למלא את כל השדות")
                return
            
            # עדכון הרכב במסד הנתונים
            update_car(plate, new_brand, new_model, new_year, new_status)
            self.load_cars()
            self.show_success("הצלחה", "פרטי הרכב עודכנו בהצלחה")

    def delete_car(self, row):
        """מחיקת רכב מהמערכת"""
        plate = self.table.item(row, 0).text()
        brand = self.table.item(row, 1).text()
        
        msg = f"האם למחוק את הרכב {brand} ({plate})?"
        if self.show_confirm("אישור מחיקה", msg):
            delete_car(plate)
            self.load_cars()
            self.show_success("הצלחה", "הרכב נמחק בהצלחה")

    def create_rental_dialog(self, parent=None):
        """יצירת דיאלוג להוספת השכרה חדשה"""
        dialog = QDialog(parent)
        dialog.setWindowTitle("הוספת השכרה חדשה")
        dialog.setStyleSheet(self.get_dialog_style())
        
        layout = QFormLayout(dialog)
        
        # שדות קלט
        customer_id = QLineEdit()
        customer_id.setPlaceholderText("הכנס מספר לקוח")
        layout.addRow("מספר לקוח:", customer_id)
        
        vehicle_id = QLineEdit()
        vehicle_id.setPlaceholderText("הכנס מספר רכב")
        layout.addRow("מספר רכב:", vehicle_id)
        
        start_date = self.create_date_input(dialog, "", "תאריך התחלה")
        layout.addRow("תאריך התחלה:", start_date)
        
        end_date = self.create_date_input(dialog, "", "תאריך סיום")
        layout.addRow("תאריך סיום:", end_date)
        
        total_price = QLineEdit()
        total_price.setPlaceholderText("הכנס מחיר כולל")
        layout.addRow("מחיר כולל:", total_price)
        
        status = QComboBox()
        status.addItems(["פעיל", "הושלם", "בוטל"])
        layout.addRow("סטטוס:", status)
        
        # כפתורי אישור וביטול
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        return dialog

    def add_rental(self):
        """פתיחת דיאלוג להוספת השכרה חדשה"""
        dialog = self.create_rental_dialog()
        
        if dialog.exec() == QDialog.Accepted:
            # קבלת הנתונים מהדיאלוג
            customer_id = dialog.findChild(QLineEdit, "customer_id").text().strip()
            vehicle_id = dialog.findChild(QLineEdit, "vehicle_id").text().strip()
            start_date = dialog.findChild(QLineEdit, "start_date").text().strip()
            end_date = dialog.findChild(QLineEdit, "end_date").text().strip()
            total_price = dialog.findChild(QLineEdit, "total_price").text().strip()
            status = dialog.findChild(QComboBox, "status").currentText().strip()
            
            # בדיקת תקינות
            if not all([customer_id, vehicle_id, start_date, end_date, total_price, status]):
                self.show_error("שגיאה", "יש למלא את כל השדות")
                return
            
            # הוספת ההשכרה למסד הנתונים
            result = add_rental(
                customer_id=customer_id,
                vehicle_id=vehicle_id,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status=status
            )
            
            if result:
                self.show_success("הצלחה", "ההשכרה נוספה בהצלחה")
                self.load_rentals()  # רענון הטבלה
            else:
                self.show_error("שגיאה", "לא ניתן להוסיף את ההשכרה")

    def edit_rental(self, row):
        """עריכת השכרה קיימת"""
        # קבלת נתוני ההשכרה מהטבלה
        rental_id = self.table.item(row, 0).text()
        customer_id = self.table.item(row, 1).text()
        vehicle_id = self.table.item(row, 2).text()
        start_date = self.table.item(row, 3).text()
        end_date = self.table.item(row, 4).text()
        total_price = self.table.item(row, 5).text()
        status = self.table.item(row, 6).text()
        
        # יצירת דיאלוג עריכה
        dialog = self.create_rental_dialog()
        
        # מילוי הנתונים הקיימים
        dialog.findChild(QLineEdit, "customer_id").setText(customer_id)
        dialog.findChild(QLineEdit, "vehicle_id").setText(vehicle_id)
        dialog.findChild(QLineEdit, "start_date").setText(start_date)
        dialog.findChild(QLineEdit, "end_date").setText(end_date)
        dialog.findChild(QLineEdit, "total_price").setText(total_price)
        dialog.findChild(QComboBox, "status").setCurrentText(status)
        
        if dialog.exec() == QDialog.Accepted:
            # קבלת הנתונים החדשים
            new_customer_id = dialog.findChild(QLineEdit, "customer_id").text().strip()
            new_vehicle_id = dialog.findChild(QLineEdit, "vehicle_id").text().strip()
            new_start_date = dialog.findChild(QLineEdit, "start_date").text().strip()
            new_end_date = dialog.findChild(QLineEdit, "end_date").text().strip()
            new_total_price = dialog.findChild(QLineEdit, "total_price").text().strip()
            new_status = dialog.findChild(QComboBox, "status").currentText().strip()
            
            # בדיקת תקינות
            if not all([new_customer_id, new_vehicle_id, new_start_date, new_end_date, new_total_price, new_status]):
                self.show_error("שגיאה", "יש למלא את כל השדות")
                return
            
            # עדכון ההשכרה במסד הנתונים
            result = update_rental(
                rental_id=rental_id,
                customer_id=new_customer_id,
                vehicle_id=new_vehicle_id,
                start_date=new_start_date,
                end_date=new_end_date,
                total_price=new_total_price,
                status=new_status
            )
            
            if result:
                self.show_success("הצלחה", "ההשכרה עודכנה בהצלחה")
                self.load_rentals()  # רענון הטבלה
            else:
                self.show_error("שגיאה", "לא ניתן לעדכן את ההשכרה")

    def delete_rental(self, row):
        """מחיקת השכרה"""
        # קבלת מזהה ההשכרה
        rental_id = self.table.item(row, 0).text()
        
        # בקשת אישור מהמשתמש
        reply = QMessageBox.question(
            self,
            "אישור מחיקה",
            f"האם אתה בטוח שברצונך למחוק את ההשכרה מספר {rental_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # מחיקת ההשכרה ממסד הנתונים
            result = delete_rental(rental_id)
            
            if result:
                self.show_success("הצלחה", "ההשכרה נמחקה בהצלחה")
                self.load_rentals()  # רענון הטבלה
            else:
                self.show_error("שגיאה", "לא ניתן למחוק את ההשכרה")

    def show_rentals(self):
        """הצגת מסך השכרות"""
        # ניקוי המסך הנוכחי
        self.clear_screen()
        
        # יצירת כותרת
        title = QLabel("ניהול השכרות")
        title.setStyleSheet("""
            QLabel {
                color: #0038B8;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        self.main_layout.addWidget(title)
        
        # יצירת טבלת השכרות
        self.rental_table = QTableWidget()
        self.rental_table.setColumnCount(8)
        self.rental_table.setHorizontalHeaderLabels([
            "מספר השכרה",
            "מספר לקוח",
            "מספר רכב",
            "תאריך התחלה",
            "תאריך סיום",
            "מחיר כולל",
            "סטטוס",
            "פעולות"
        ])
        
        # הגדרת סגנון הטבלה
        self.rental_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #b3c6e0;
                border-radius: 8px;
                gridline-color: #e6e6e6;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e6e6e6;
            }
            QHeaderView::section {
                background-color: #f7fafd;
                color: #0038B8;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #b3c6e0;
                font-weight: bold;
            }
            QPushButton {
                background: #0038B8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                margin: 2px;
            }
            QPushButton:hover {
                background: #0057B8;
            }
        """)
        
        # הגדרת התנהגות הטבלה
        self.rental_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.rental_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.rental_table.horizontalHeader().setStretchLastSection(True)
        self.rental_table.verticalHeader().setVisible(False)
        
        # הוספת הטבלה למסך
        self.main_layout.addWidget(self.rental_table)
        
        # יצירת כפתור הוספה
        add_button = QPushButton("הוסף השכרה חדשה")
        add_button.setStyleSheet("""
            QPushButton {
                background: #0038B8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background: #0057B8;
            }
        """)
        add_button.clicked.connect(self.add_rental)
        self.main_layout.addWidget(add_button)
        
        # טעינת נתוני ההשכרות
        self.load_rentals()

    def get_dialog_style(self):
        return """
            QDialog {
            QCalendarWidget QAbstractItemView:enabled {
                color: #333;
                background-color: white;
                selection-background-color: #007bff;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #999;
            }
        """

# עדכון הפעלת האפליקציה להציג את דף הכניסה
if __name__ == "__main__":
    app = QApplication(sys.argv)  # יצירת אפליקציה
    app.setLayoutDirection(Qt.RightToLeft)  # יישור לימין
    init_db()  # יצירת טבלאות במסד הנתונים
    window = MainWindow()  # יצירת חלון ראשי
    window.show()  # הצגת החלון הראשי
    sys.exit(app.exec())  # הרצת לולאת האפליקציה