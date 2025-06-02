-- טבלת לקוחות - שומרת את כל המידע על הלקוחות שלנו
CREATE TABLE IF NOT EXISTS Customer (
    id TEXT PRIMARY KEY,          -- תעודת זהות של הלקוח
    name TEXT NOT NULL,           -- שם מלא
    phone TEXT,                   -- מספר טלפון
    email TEXT                    -- כתובת מייל
);

-- טבלת רכבים - כל הרכבים שיש לנו להשכרה
CREATE TABLE IF NOT EXISTS Vehicle (
    licensePlate TEXT PRIMARY KEY,    -- מספר רישוי
    brand TEXT NOT NULL,              -- יצרן (טויוטה, הונדה וכו')
    model TEXT NOT NULL,              -- דגם ספציפי
    status TEXT DEFAULT 'available'    -- האם הרכב פנוי או מושכר
        CHECK (status IN ('available', 'rented'))
);

-- טבלת השכרות - מתי מי השכיר איזה רכב
CREATE TABLE IF NOT EXISTS Rental (
    rentalId INTEGER PRIMARY KEY AUTOINCREMENT,  -- מספר מזהה להשכרה
    customerId TEXT,                             -- מי השכיר (מספר ת"ז)
    vehicleId TEXT,                              -- איזה רכב (מספר רישוי)
    startDate DATE NOT NULL,                     -- מתי ההשכרה מתחילה
    endDate DATE NOT NULL,                       -- מתי ההשכרה מסתיימת
    totalPrice FLOAT,                            -- כמה עולה ההשכרה
    status TEXT DEFAULT 'active'                 -- מצב ההשכרה (פעילה, הסתיימה, ממתינה)
        CHECK (status IN ('active', 'completed', 'pending')),
    FOREIGN KEY (customerId) REFERENCES Customer(id),
    FOREIGN KEY (vehicleId) REFERENCES Vehicle(licensePlate)
); 