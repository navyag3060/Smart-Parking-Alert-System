# Smart-Parking-Alert-System
AI-powered Web Application for Detecting Improperly Parked Vehicles

Smart Parking Alert is a web-based application that helps prevent double parking, vehicle blocking, and small-scale traffic jams. Users can upload an image of a vehicle’s number plate, the system extracts the plate number using OCR (Tesseract), verifies ownership details from an SQL database, and instantly sends an alert message to the registered phone number using Twilio.

This project aims to improve urban mobility by empowering people to report wrongly parked vehicles in real time.

📌 Features

✔ Image Upload System
Users can upload a photo of a vehicle’s number plate.

✔ OCR-Based Number Plate Detection
Uses Tesseract OCR to extract the text from the image.

✔ Registered Vehicle Lookup
Matches the detected number plate with entries stored in an SQL database.

✔ SMS Notifications
Automatically alerts the vehicle owner via Twilio:

🚫 Double Parking

🚧 Traffic Blocking

🚙 Incorrect Parking Position

✔ Responsive Frontend
A clean UI with gradients, image preview, and dynamic results.

✔ Flask Backend
Handles uploads, OCR processing, and database operations.

🛠️ Tech Stack
Backend

Python (Flask)

Tesseract OCR

SQLite / MySQL (your database choice)

Twilio API

Frontend

HTML5

CSS3 (custom + gradient UI)

JavaScript Fetch API
