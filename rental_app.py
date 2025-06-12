# Version 1.1 - Firmware Update
# מייבא את כל הספריות שאנחנו צריכים בשביל האפליקציה
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify
)
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import sqlite3

# יוצר את האפליקציה
app = Flask(__name__)
# ... existing code ... 