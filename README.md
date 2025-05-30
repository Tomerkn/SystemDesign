# מערכת ניהול השכרת רכבים

מערכת לניהול השכרת רכבים המאפשרת ניהול לקוחות, רכבים, השכרות ותחזוקה.

## תכונות עיקריות

- ניהול לקוחות (הוספה, עריכה, מחיקה)
- ניהול רכבים (הוספה, עריכה, מחיקה, עדכון סטטוס)
- ניהול השכרות (יצירה, החזרה, ביטול)
- ניהול תחזוקה (התראות, מעקב)
- לוח בקרה עם סטטיסטיקות
- הזמנה מהירה

## טכנולוגיות

- Frontend: React, React Router, Axios
- Backend: Flask, Flask-SQLAlchemy
- Database: SQLite

## התקנה

1. התקן את הדרישות:
```bash
pip install -r requirements.txt
```

2. הפעל את השרת:
```bash
python app.py
```

3. התקן את הדרישות של ה-Frontend:
```bash
cd frontend
npm install
```

4. הפעל את ה-Frontend:
```bash
npm start
```

## מבנה הפרויקט

```
.
├── app.py                 # קובץ השרת הראשי
├── requirements.txt       # דרישות Python
├── frontend/             # תיקיית ה-Frontend
│   ├── src/             # קוד המקור
│   │   ├── components/  # קומפוננטות
│   │   ├── pages/      # דפים
│   │   ├── services/   # שירותי API
│   │   └── utils/      # פונקציות עזר
│   └── public/         # קבצים סטטיים
└── README.md           # תיעוד
```

## שימוש

1. פתח את הדפדפן בכתובת `http://localhost:3000`
2. התחבר למערכת
3. השתמש בתפריט הצד כדי לנווט בין הדפים השונים

## פיתוח

- ה-Frontend מפותח ב-React ומשתמש ב-React Router לניתוב
- ה-Backend מפותח ב-Flask ומשתמש ב-SQLAlchemy לניהול בסיס הנתונים
- התקשורת בין ה-Frontend ל-Backend מתבצעת באמצעות REST API

## רישיון

MIT 