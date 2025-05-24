import ttkbootstrap as tb  # מייבא ספריית עיצוב משופרת לממשק
from ttkbootstrap.constants import *  # מייבא את כל הקבועים מהספרייה
import tkinter as tk  # מייבא את ספריית הממשק הבסיסית
from tkinter import ttk, messagebox  # מייבא רכיבים נוספים לממשק
import sqlite3  # מייבא את הספרייה שעובדת עם מסד נתונים
from vehicle import Vehicle  # מייבא את מחלקת הרכב
from vehicle_monitoring import MaintenanceAlert  # מייבא את מחלקת התראות התחזוקה

DB_PATH = "rental_system.db"  # נתיב למסד הנתונים

# פונקציות מסד נתונים
def register_customer(customer_id, name, phone, email):  # פונקציה שרושמת לקוח חדש
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    try:  # מנסה להוסיף את הלקוח
        c.execute("INSERT INTO Customer (id, name, phone, email) VALUES (?, ?, ?, ?)", 
                 (customer_id, name, phone, email))  # מכניס את פרטי הלקוח לטבלה
        conn.commit()  # שומר את השינויים
        return True, "הלקוח נוסף בהצלחה."  # מחזיר הודעת הצלחה
    except sqlite3.IntegrityError:  # תופס שגיאה אם הלקוח כבר קיים
        return False, "הלקוח כבר קיים."  # מחזיר הודעת שגיאה
    finally:  # בכל מקרה
        conn.close()  # סוגר את החיבור למסד


def rent_vehicle(customer_id, license_plate, start_date, end_date, log_func=None):  # פונקציה להשכרת רכב
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    try:  # מנסה להשכיר את הרכב
        if log_func:  # אם קיבלנו פונקציית תיעוד
            log_func(f"[DEBUG] Checking if customer {customer_id} exists...")  # רושם לתיעוד
        c.execute("SELECT id FROM Customer WHERE id = ?", (customer_id,))  # בודק אם הלקוח קיים
        if not c.fetchone():  # אם הלקוח לא קיים
            if log_func:  # אם יש פונקציית תיעוד
                log_func(f"[שגיאה] הלקוח {customer_id} לא קיים במערכת.")  # רושם שגיאה לתיעוד
            conn.close()  # סוגר חיבור
            return False, "הלקוח לא קיים במערכת."  # מחזיר הודעת שגיאה

        if log_func:  # אם יש פונקציית תיעוד
            log_func(f"[DEBUG] Checking if vehicle {license_plate} exists and is available...")  # רושם לתיעוד
        c.execute("SELECT status FROM Vehicle WHERE licensePlate = ?", (license_plate,))  # בודק אם הרכב קיים
        row = c.fetchone()  # מקבל את התוצאה
        if not row:  # אם הרכב לא קיים
            if log_func:  # אם יש פונקציית תיעוד
                log_func(f"[שגיאה] הרכב {license_plate} לא נמצא.")  # רושם שגיאה לתיעוד
            conn.close()  # סוגר חיבור
            return False, "הרכב לא נמצא."  # מחזיר הודעת שגיאה
        if row[0] != "available":  # אם הרכב לא פנוי
            if log_func:  # אם יש פונקציית תיעוד
                log_func(f"[שגיאה] הרכב {license_plate} אינו זמין (סטטוס: {row[0]}).")  # רושם שגיאה לתיעוד
            conn.close()  # סוגר חיבור
            return False, "הרכב אינו זמין."  # מחזיר הודעת שגיאה

        if log_func:  # אם יש פונקציית תיעוד
            log_func(f"[DEBUG] Inserting rental for customer {customer_id}, car {license_plate}, {start_date} to {end_date}")  # רושם לתיעוד
        c.execute("""
            INSERT INTO Rental (customerId, vehicleId, startDate, endDate) 
            VALUES (?, ?, ?, ?)
        """, (customer_id, license_plate, start_date, end_date))  # מכניס את ההשכרה למסד

        if log_func:  # אם יש פונקציית תיעוד
            log_func(f"[DEBUG] Updating vehicle {license_plate} status to 'rented'")  # רושם לתיעוד
        c.execute("""
            UPDATE Vehicle 
            SET status = 'rented' 
            WHERE licensePlate = ?
        """, (license_plate,))  # מעדכן את סטטוס הרכב ל'מושכר'
        conn.commit()  # שומר את השינויים
        if log_func:  # אם יש פונקציית תיעוד
            log_func(f"[הצלחה] הרכב הושכר בהצלחה!")  # רושם הצלחה לתיעוד
        return True, "הרכב הושכר בהצלחה."  # מחזיר הודעת הצלחה
    except sqlite3.Error as e:  # תופס שגיאות SQL
        conn.rollback()  # מבטל את השינויים
        if log_func:  # אם יש פונקציית תיעוד
            log_func(f"[שגיאת SQL] {str(e)}")  # רושם את השגיאה לתיעוד
        return False, f"שגיאה בהשכרת הרכב: {str(e)}"  # מחזיר הודעת שגיאה
    finally:  # בכל מקרה
        conn.close()  # סוגר את החיבור למסד


def return_vehicle(license_plate):  # פונקציה להחזרת רכב מושכר
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    c.execute("SELECT status FROM Vehicle WHERE licensePlate = ?", (license_plate,))  # בודק את הסטטוס של הרכב
    row = c.fetchone()  # מקבל את התוצאה
    if not row:  # אם הרכב לא קיים
        conn.close()  # סוגר חיבור
        return False, "הרכב לא נמצא."  # מחזיר הודעת שגיאה
    if row[0] != "rented":  # אם הרכב לא מושכר
        conn.close()  # סוגר חיבור
        return False, "הרכב לא מושכר."  # מחזיר הודעת שגיאה
    c.execute("UPDATE Vehicle SET status = 'available' WHERE licensePlate = ?", 
             (license_plate,))  # מעדכן את סטטוס הרכב ל'פנוי'
    conn.commit()  # שומר את השינויים
    conn.close()  # סוגר חיבור
    return True, "הרכב הוחזר בהצלחה."  # מחזיר הודעת הצלחה


def get_rentals():  # פונקציה שמביאה את כל ההשכרות
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    c.execute("""
        SELECT r.rentalId, c.name, v.licensePlate, r.startDate, r.endDate 
        FROM Rental r
        JOIN Customer c ON r.customerId = c.id
        JOIN Vehicle v ON r.vehicleId = v.licensePlate
        ORDER BY r.startDate DESC
    """)  # מביא את כל ההשכרות עם פרטי הלקוח והרכב, ממוינות לפי תאריך
    rows = c.fetchall()  # מקבל את כל התוצאות
    conn.close()  # סוגר חיבור
    return rows  # מחזיר את ההשכרות


def get_stats():  # פונקציה שמביאה נתונים סטטיסטיים
    conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
    c = conn.cursor()  # יוצר סמן
    c.execute("SELECT COUNT(*) FROM Vehicle")  # סופר כמה רכבים יש
    cars = c.fetchone()[0]  # מקבל את המספר
    c.execute("SELECT COUNT(*) FROM Customer")  # סופר כמה לקוחות יש
    customers = c.fetchone()[0]  # מקבל את המספר
    c.execute("SELECT COUNT(*) FROM Rental WHERE endDate >= date('now')")  # סופר כמה השכרות פעילות יש
    active_rentals = c.fetchone()[0]  # מקבל את המספר
    c.execute("SELECT COUNT(*) FROM Vehicle WHERE status = 'available'")  # סופר כמה רכבים פנויים יש
    available = c.fetchone()[0]  # מקבל את המספר
    conn.close()  # סוגר חיבור
    return cars, customers, active_rentals, available  # מחזיר את כל הנתונים

class RentalApp:  # המחלקה הראשית של האפליקציה
    def __init__(self, root):  # פונקציית האתחול שרצה כשיוצרים מופע של המחלקה
        self.root = root  # שומר את החלון הראשי
        self.root.title("גלגל עומר - מערכת השכרת רכבים")  # קובע את כותרת החלון
        self.root.geometry("1250x800")  # קובע את גודל החלון
        self.style = tb.Style("cosmo")  # קובע את ערכת העיצוב
        self.root.option_add('*Font', 'Arial 13')  # קובע פונט ברירת מחדל
        self.root.configure(bg='#f4f7fa')  # קובע צבע רקע

        # מסגרת ראשית
        self.main_frame = tb.Frame(self.root)  # יוצר מסגרת שתכיל את כל האפליקציה
        self.main_frame.pack(fill=BOTH, expand=True)  # מסדר את המסגרת שתמלא את כל החלון

        # סרגל צד עם לוגו ואייקונים
        self.sidebar = tb.Frame(self.main_frame, bootstyle=PRIMARY, width=240)  # יוצר מסגרת לסרגל הצד
        self.sidebar.pack(side=RIGHT, fill=Y)  # מסדר את הסרגל בצד ימין
        self.sidebar.pack_propagate(False)  # מונע מהסרגל להצטמצם

        # אזור הלוגו
        logo_frame = tb.Frame(self.sidebar, bootstyle=PRIMARY)  # יוצר מסגרת ללוגו
        logo_frame.pack(fill=X, pady=(35, 10))  # מסדר את מסגרת הלוגו בחלק העליון
        tb.Label(logo_frame, text="🛞", font=("Arial", 38), bootstyle=PRIMARY, anchor='center').pack(side=RIGHT, padx=(0, 10))  # מוסיף אייקון גלגל
        tb.Label(logo_frame, text="גלגל עומר", font=("Arial", 22, "bold"), bootstyle=(INVERSE, PRIMARY), anchor='e').pack(side=RIGHT)  # מוסיף טקסט לוגו

        self.nav_buttons = {}  # מילון שיכיל את כפתורי הניווט
        nav_items = [  # רשימת פריטי הניווט
            ("דשבורד", "🏠", self.show_dashboard),  # עמוד ראשי
            ("חיפוש/הזמנה", "🔎", self.show_booking),  # עמוד הזמנות
            ("לקוחות", "👤", self.show_customers),  # עמוד לקוחות
            ("רכבים", "🚗", self.show_cars),  # עמוד רכבים
            ("השכרות", "📝", self.show_rentals),  # עמוד השכרות
            ("תחזוקה", "🛠️", self.show_maintenance)  # עמוד תחזוקה
        ]
        for text, icon, cmd in nav_items:  # עובר על כל פריטי הניווט
            btn = tb.Button(self.sidebar, text=f"{icon}  {text}", bootstyle=SECONDARY, command=cmd, width=22, style='TButton')  # יוצר כפתור
            btn.pack(pady=12, padx=18, anchor='e')  # מסדר את הכפתור בסרגל
            self.nav_buttons[text] = btn  # שומר את הכפתור במילון

        # אזור התוכן
        self.content = tb.Frame(self.main_frame, bootstyle=LIGHT)  # יוצר מסגרת לתוכן הראשי
        self.content.pack(side=RIGHT, fill=BOTH, expand=True)  # מסדר את התוכן כך שימלא את השטח הנותר

        self.show_dashboard()  # מציג את העמוד הראשי

    def clear_content(self):  # פונקציה שמנקה את אזור התוכן
        for widget in self.content.winfo_children():  # עובר על כל הרכיבים באזור התוכן
            widget.destroy()  # מוחק את הרכיב

    def show_dashboard(self):  # פונקציה שמציגה את העמוד הראשי
        self.clear_content()  # מנקה את התוכן הקיים
        cars, customers, active_rentals, available = get_stats()  # מקבל את הנתונים הסטטיסטיים
        # כרטיס ברוכים הבאים
        welcome_card = tb.Frame(self.content, bootstyle=INFO, relief=RAISED, borderwidth=2)  # יוצר מסגרת לכרטיס ברוכים הבאים
        welcome_card.pack(pady=30, padx=30, anchor='e', fill=X)  # מסדר את הכרטיס בחלק העליון
        tb.Label(welcome_card, text="ברוך הבא לגלגל עומר!", font=("Arial", 28, "bold"), anchor='e', bootstyle=PRIMARY).pack(pady=(18, 0), anchor='e')  # מוסיף כותרת
        tb.Label(welcome_card, text="מערכת השכרת רכבים מקצועית, קלה ונוחה לשימוש", font=("Arial", 15), anchor='e').pack(pady=(0, 18), anchor='e')  # מוסיף תיאור
        # כרטיסי סטטיסטיקה
        stats_frame = tb.Frame(self.content)  # יוצר מסגרת לכרטיסי הסטטיסטיקה
        stats_frame.pack(pady=10, anchor='e')  # מסדר את המסגרת
        stat_cards = [  # רשימת כרטיסי הסטטיסטיקה
            ("רכבים במערכת", cars, "#007bff", "🚗"),  # סטטיסטיקת רכבים
            ("לקוחות רשומים", customers, "#6610f2", "👤"),  # סטטיסטיקת לקוחות
            ("השכרות פעילות", active_rentals, "#fd7e14", "📝"),  # סטטיסטיקת השכרות
            ("רכבים זמינים", available, "#198754", "✅")  # סטטיסטיקת רכבים זמינים
        ]
        for i, (label, value, color, icon) in enumerate(stat_cards):  # עובר על כל כרטיסי הסטטיסטיקה
            card = tb.Frame(stats_frame, bootstyle=LIGHT, relief=RAISED, borderwidth=2)  # יוצר כרטיס
            card.grid(row=0, column=i, padx=25)  # מסדר את הכרטיס בשורה
            tb.Label(card, text=icon, font=("Arial", 30), anchor='center').pack(padx=10, pady=(15, 0))  # מוסיף אייקון
            tb.Label(card, text=str(value), font=("Arial", 34, "bold"), foreground=color, anchor='center').pack(padx=30, pady=(5, 7))  # מוסיף את המספר
            tb.Label(card, text=label, font=("Arial", 15), anchor='center').pack(padx=10, pady=(0, 18))  # מוסיף את התווית
        # טופס הזמנה/חיפוש
        self.show_booking_form(parent=self.content)  # מציג את טופס ההזמנה בעמוד הראשי

    def show_booking(self):  # פונקציה שמציגה את עמוד ההזמנות
        self.clear_content()  # מנקה את התוכן הקיים
        tb.Label(self.content, text="חיפוש והשכרת רכב", font=("Arial", 24, "bold"), anchor='e', bootstyle=PRIMARY).pack(pady=28, anchor='e')  # מוסיף כותרת
        self.show_booking_form(parent=self.content)  # מציג את טופס ההזמנה

    def show_booking_form(self, parent):  # פונקציה שמציגה את טופס ההזמנה
        form_card = tb.Frame(parent, bootstyle=SECONDARY, relief=RAISED, borderwidth=2)  # יוצר מסגרת לטופס
        form_card.pack(pady=40, padx=40, anchor='e')  # מסדר את הטופס במרכז
        # מיקום איסוף
        tb.Label(form_card, text="📍 מיקום איסוף:", anchor='e', font=("Arial", 13, "bold")).grid(row=0, column=2, sticky='e', padx=12, pady=12)  # מוסיף תווית
        self.pickup_entry = tb.Entry(form_card, justify='right', width=28)  # יוצר תיבת טקסט
        self.pickup_entry.grid(row=0, column=1, padx=12, pady=12)  # מסדר את התיבה
        # מיקום החזרה
        tb.Label(form_card, text="📍 מיקום החזרה:", anchor='e', font=("Arial", 13, "bold")).grid(row=1, column=2, sticky='e', padx=12, pady=12)  # מוסיף תווית
        self.dropoff_entry = tb.Entry(form_card, justify='right', width=28)  # יוצר תיבת טקסט
        self.dropoff_entry.grid(row=1, column=1, padx=12, pady=12)  # מסדר את התיבה
        # תאריך איסוף
        tb.Label(form_card, text="📅 תאריך איסוף:", anchor='e', font=("Arial", 13, "bold")).grid(row=2, column=2, sticky='e', padx=12, pady=12)  # מוסיף תווית
        self.pickup_date = tb.Entry(form_card, justify='right', width=28)  # יוצר תיבת טקסט
        self.pickup_date.grid(row=2, column=1, padx=12, pady=12)  # מסדר את התיבה
        # תאריך החזרה
        tb.Label(form_card, text="📅 תאריך החזרה:", anchor='e', font=("Arial", 13, "bold")).grid(row=3, column=2, sticky='e', padx=12, pady=12)  # מוסיף תווית
        self.dropoff_date = tb.Entry(form_card, justify='right', width=28)  # יוצר תיבת טקסט
        self.dropoff_date.grid(row=3, column=1, padx=12, pady=12)  # מסדר את התיבה
        # סוג רכב
        tb.Label(form_card, text="🚘 סוג רכב:", anchor='e', font=("Arial", 13, "bold")).grid(row=4, column=2, sticky='e', padx=12, pady=12)  # מוסיף תווית
        self.car_type = tb.Combobox(form_card, values=["כל הרכבים", "קטן", "משפחתי", "יוקרתי", "ג'יפ", "מסחרי"], justify='right', width=26)  # יוצר תיבת בחירה
        self.car_type.current(0)  # בוחר את הערך הראשון כברירת מחדל
        self.car_type.grid(row=4, column=1, padx=12, pady=12)  # מסדר את התיבה
        # כפתור חיפוש
        tb.Button(form_card, text="חפש רכבים זמינים", bootstyle=SUCCESS, width=22).grid(row=5, column=1, pady=22, sticky='e')  # מוסיף כפתור

    def show_customers(self):  # פונקציה שמציגה את דף הלקוחות
        self.clear_content()  # מנקה את התוכן הקיים
        tb.Label(self.content, text="לקוחות", font=("Arial", 22, "bold"), anchor='e', bootstyle=PRIMARY).pack(pady=28, anchor='e')  # מוסיף כותרת
        # סרגל חיפוש
        search_frame = tb.Frame(self.content)  # יוצר מסגרת לסרגל החיפוש
        search_frame.pack(anchor='e', pady=(0, 10), padx=20)  # מסדר את המסגרת
        tb.Label(search_frame, text="🔍 חפש לקוח:", anchor='e').pack(side=RIGHT, padx=(0, 8))  # מוסיף תווית
        self.customer_search_var = tb.StringVar()  # יוצר משתנה לטקסט החיפוש
        search_entry = tb.Entry(search_frame, textvariable=self.customer_search_var, width=30, justify='right')  # יוצר תיבת חיפוש
        search_entry.pack(side=RIGHT)  # מסדר את התיבה
        tb.Button(search_frame, text="חפש", bootstyle=INFO, command=self.refresh_customers).pack(side=RIGHT, padx=8)  # מוסיף כפתור חיפוש
        tb.Button(search_frame, text="הוסף לקוח חדש", bootstyle=SUCCESS, command=self.add_customer_dialog).pack(side=RIGHT, padx=8)  # מוסיף כפתור להוספת לקוח
        # טבלה
        columns = ("ת.ז", "שם", "טלפון", "אימייל", "פעולות")  # מגדיר את העמודות
        self.customers_tree = tb.Treeview(self.content, columns=columns, show='headings', height=12, bootstyle=INFO)  # יוצר טבלה
        for col in columns:  # עובר על כל העמודות
            self.customers_tree.heading(col, text=col, anchor='center')  # מגדיר כותרת לעמודה
            self.customers_tree.column(col, anchor='center', width=120)  # מגדיר רוחב ויישור לעמודה
        self.customers_tree.column("פעולות", width=160)  # מגדיר רוחב לעמודת הפעולות
        self.customers_tree.pack(fill=X, padx=20, pady=10)  # מסדר את הטבלה
        self.refresh_customers()  # מרענן את רשימת הלקוחות

    def refresh_customers(self):  # פונקציה שמרעננת את רשימת הלקוחות
        for row in self.customers_tree.get_children():  # עובר על כל השורות בטבלה
            self.customers_tree.delete(row)  # מוחק את השורה
        search = self.customer_search_var.get() if hasattr(self, 'customer_search_var') else ''  # מקבל את טקסט החיפוש
        conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
        c = conn.cursor()  # יוצר סמן
        if search:  # אם יש טקסט חיפוש
            c.execute("SELECT id, name, phone, email FROM Customer WHERE name LIKE ? OR id LIKE ? OR phone LIKE ? OR email LIKE ? ORDER BY name", (f"%{search}%",)*4)  # מחפש בכל השדות
        else:  # אם אין טקסט חיפוש
            c.execute("SELECT id, name, phone, email FROM Customer ORDER BY name")  # מביא את כל הלקוחות
        for cid, name, phone, email in c.fetchall():  # עובר על כל התוצאות
            self.customers_tree.insert('', 'end', values=(cid, name, phone, email, ""))  # מוסיף שורה לטבלה
        conn.close()  # סוגר חיבור
        # מוסיף כפתורי פעולה
        for iid in self.customers_tree.get_children():  # עובר על כל השורות בטבלה
            self.customers_tree.set(iid, "פעולות", "✏️ ערוך   🗑️ מחק")  # מוסיף טקסט לעמודת הפעולות
        self.customers_tree.bind('<Double-1>', self.on_customer_action)  # מגדיר פעולה ללחיצה כפולה

    def on_customer_action(self, event):  # פונקציה שמטפלת בלחיצה על פעולות הלקוח
        item = self.customers_tree.identify_row(event.y)  # מזהה את השורה שנלחצה
        col = self.customers_tree.identify_column(event.x)  # מזהה את העמודה שנלחצה
        if not item:  # אם לא נבחרה שורה
            return  # יוצא מהפונקציה
        values = self.customers_tree.item(item, 'values')  # מקבל את הערכים של השורה
        if col == '#5':  # אם נלחצה עמודת הפעולות
            # מציג תפריט קופץ לעריכה/מחיקה
            menu = tb.Menu(self.root, tearoff=0)  # יוצר תפריט
            menu.add_command(label="✏️ ערוך", command=lambda: self.edit_customer_dialog(values))  # מוסיף אפשרות עריכה
            menu.add_command(label="🗑️ מחק", command=lambda: self.delete_customer_confirm(values[0], values[1]))  # מוסיף אפשרות מחיקה
            menu.tk_popup(event.x_root, event.y_root)  # מציג את התפריט במיקום העכבר

    def add_customer_dialog(self):  # פונקציה שמציגה חלון להוספת לקוח
        dialog = tb.Toplevel(self.root)  # יוצר חלון קופץ
        dialog.title("הוסף לקוח חדש")  # קובע כותרת לחלון
        dialog.geometry("400x320")  # קובע גודל לחלון
        dialog.transient(self.root)  # הופך את החלון לתלוי בחלון הראשי
        dialog.grab_set()  # גורם לחלון להיות מודאלי (חוסם את החלון הראשי)
        # טופס
        tb.Label(dialog, text="ת.ז:", anchor='e').pack(pady=8, anchor='e')  # מוסיף תווית
        id_entry = tb.Entry(dialog, justify='right')  # יוצר תיבת טקסט
        id_entry.pack(pady=4, anchor='e')  # מסדר את התיבה
        tb.Label(dialog, text="שם:", anchor='e').pack(pady=8, anchor='e')  # מוסיף תווית
        name_entry = tb.Entry(dialog, justify='right')  # יוצר תיבת טקסט
        name_entry.pack(pady=4, anchor='e')  # מסדר את התיבה
        tb.Label(dialog, text="טלפון:", anchor='e').pack(pady=8, anchor='e')  # מוסיף תווית
        phone_entry = tb.Entry(dialog, justify='right')  # יוצר תיבת טקסט
        phone_entry.pack(pady=4, anchor='e')  # מסדר את התיבה
        tb.Label(dialog, text="אימייל:", anchor='e').pack(pady=8, anchor='e')  # מוסיף תווית
        email_entry = tb.Entry(dialog, justify='right')  # יוצר תיבת טקסט
        email_entry.pack(pady=4, anchor='e')  # מסדר את התיבה
        def submit():  # פונקציה פנימית שמטפלת בשליחת הטופס
            cid = id_entry.get().strip()  # מקבל את הת.ז
            name = name_entry.get().strip()  # מקבל את השם
            phone = phone_entry.get().strip()  # מקבל את הטלפון
            email = email_entry.get().strip()  # מקבל את האימייל
            if not (cid and name and phone and email):  # אם לא מולאו כל השדות
                tb.Messagebox.show_error("יש למלא את כל השדות", "שגיאה")  # מציג הודעת שגיאה
                return  # יוצא מהפונקציה
            ok, msg = register_customer(cid, name, phone, email)  # מנסה לרשום את הלקוח
            if ok:  # אם ההרשמה הצליחה
                tb.Messagebox.show_info(msg, "הצלחה")  # מציג הודעת הצלחה
                dialog.destroy()  # סוגר את החלון
                self.refresh_customers()  # מרענן את רשימת הלקוחות
            else:  # אם ההרשמה נכשלה
                tb.Messagebox.show_error(msg, "שגיאה")  # מציג הודעת שגיאה
        tb.Button(dialog, text="הוסף", bootstyle=SUCCESS, command=submit).pack(pady=18)  # מוסיף כפתור שליחה

    def edit_customer_dialog(self, values):  # פונקציה שמציגה חלון לעריכת לקוח
        cid, name, phone, email, _ = values  # מחלץ את הערכים של הלקוח
        dialog = tb.Toplevel(self.root)  # יוצר חלון קופץ
        dialog.title("עריכת לקוח")  # קובע כותרת לחלון
        dialog.geometry("400x320")  # קובע גודל לחלון
        dialog.transient(self.root)  # הופך את החלון לתלוי בחלון הראשי
        dialog.grab_set()  # גורם לחלון להיות מודאלי (חוסם את החלון הראשי)
        # טופס
        tb.Label(dialog, text="ת.ז:", anchor='e').pack(pady=8, anchor='e')  # מוסיף תווית
        id_entry = tb.Entry(dialog, justify='right')  # יוצר תיבת טקסט
        id_entry.insert(0, cid)  # מכניס את הת.ז הקיימת
        id_entry.config(state='disabled')  # חוסם את עריכת הת.ז
        id_entry.pack(pady=4, anchor='e')  # מסדר את התיבה
        tb.Label(dialog, text="שם:", anchor='e').pack(pady=8, anchor='e')  # מוסיף תווית
        name_entry = tb.Entry(dialog, justify='right')  # יוצר תיבת טקסט
        name_entry.insert(0, name)  # מכניס את השם הקיים
        name_entry.pack(pady=4, anchor='e')  # מסדר את התיבה
        tb.Label(dialog, text="טלפון:", anchor='e').pack(pady=8, anchor='e')  # מוסיף תווית
        phone_entry = tb.Entry(dialog, justify='right')  # יוצר תיבת טקסט
        phone_entry.insert(0, phone)  # מכניס את הטלפון הקיים
        phone_entry.pack(pady=4, anchor='e')  # מסדר את התיבה
        tb.Label(dialog, text="אימייל:", anchor='e').pack(pady=8, anchor='e')  # מוסיף תווית
        email_entry = tb.Entry(dialog, justify='right')  # יוצר תיבת טקסט
        email_entry.insert(0, email)  # מכניס את האימייל הקיים
        email_entry.pack(pady=4, anchor='e')  # מסדר את התיבה
        def submit():  # פונקציה פנימית שמטפלת בשליחת הטופס
            new_name = name_entry.get().strip()  # מקבל את השם החדש
            new_phone = phone_entry.get().strip()  # מקבל את הטלפון החדש
            new_email = email_entry.get().strip()  # מקבל את האימייל החדש
            if not (new_name and new_phone and new_email):  # אם לא מולאו כל השדות
                tb.Messagebox.show_error("יש למלא את כל השדות", "שגיאה")  # מציג הודעת שגיאה
                return  # יוצא מהפונקציה
            conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
            c = conn.cursor()  # יוצר סמן
            c.execute("UPDATE Customer SET name=?, phone=?, email=? WHERE id=?", (new_name, new_phone, new_email, cid))  # מעדכן את פרטי הלקוח
            conn.commit()  # שומר את השינויים
            conn.close()  # סוגר חיבור
            tb.Messagebox.show_info("הלקוח עודכן בהצלחה", "הצלחה")  # מציג הודעת הצלחה
            dialog.destroy()  # סוגר את החלון
            self.refresh_customers()  # מרענן את רשימת הלקוחות
        tb.Button(dialog, text="עדכן", bootstyle=SUCCESS, command=submit).pack(pady=18)  # מוסיף כפתור עדכון

    def delete_customer_confirm(self, cid, name):  # פונקציה שמבקשת אישור למחיקת לקוח
        if tb.Messagebox.okcancel(f"האם למחוק את הלקוח {name}?", "אישור מחיקה"):  # מציג חלון אישור
            conn = sqlite3.connect(DB_PATH)  # מתחבר למסד
            c = conn.cursor()  # יוצר סמן
            c.execute("DELETE FROM Customer WHERE id=?", (cid,))  # מוחק את הלקוח
            conn.commit()  # שומר את השינויים
            conn.close()  # סוגר חיבור
            self.refresh_customers()  # מרענן את רשימת הלקוחות

    def show_cars(self):  # פונקציה שמציגה את דף הרכבים
        self.clear_content()  # מנקה את התוכן הקיים
        tb.Label(self.content, text="רכבים", font=("Arial", 22, "bold"), anchor='e', bootstyle=PRIMARY).pack(pady=28, anchor='e')  # מוסיף כותרת
        tb.Label(self.content, text="(כאן תוצג רשימת הרכבים)", anchor='e').pack(anchor='e')  # מוסיף תווית זמנית

    def show_rentals(self):  # פונקציה שמציגה את דף ההשכרות
        self.clear_content()  # מנקה את התוכן הקיים
        tb.Label(self.content, text="השכרות", font=("Arial", 22, "bold"), anchor='e', bootstyle=PRIMARY).pack(pady=28, anchor='e')  # מוסיף כותרת
        tb.Label(self.content, text="(כאן תוצג רשימת ההשכרות)", anchor='e').pack(anchor='e')  # מוסיף תווית זמנית

    def show_maintenance(self):  # פונקציה שמציגה את דף התחזוקה
        self.clear_content()  # מנקה את התוכן הקיים
        tb.Label(self.content, text="תחזוקה", font=("Arial", 22, "bold"), anchor='e', bootstyle=PRIMARY).pack(pady=28, anchor='e')  # מוסיף כותרת
        tb.Label(self.content, text="(כאן תוצג רשימת התחזוקה)", anchor='e').pack(anchor='e')  # מוסיף תווית זמנית

if __name__ == "__main__":  # בודק אם הקובץ מופעל ישירות
    root = tb.Window(themename="cosmo")  # יוצר חלון ראשי עם ערכת נושא
    app = RentalApp(root)  # יוצר מופע של האפליקציה
    root.mainloop()  # מפעיל את לולאת האירועים של הממשק 