
# בוט טלגרם להוספת Thumbnail לקבצים (PDF/EPUB)

## 🚀 הוראות לפריסה ב‑Render

1. עבור ל‑[https://render.com](https://render.com) והירשם
2. לחץ על **New > Web Service**
3. חבר את הריפו החדש
4. ודא את ההגדרות הבאות:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Runtime: Python 3.x
5. הגדר משתנה סביבה:
   - `TELEGRAM_TOKEN`: הטוקן של הבוט שלך

## 📸 שימוש
- `/set_thumbnail` – שלח תמונה כדי להגדיר Thumbnail ברירת מחדל
- שלח קובץ PDF או EPUB – הבוט יחזיר אותו עם ה-Thumbnail

> תוודא שתיקיית thumbs קיימת. הבוט יוצר אותה אוטומטית אם צריך.
