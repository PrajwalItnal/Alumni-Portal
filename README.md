# 🎓 Alumni Portal  
### A Comprehensive Alumni Management System built with Django

![Django](https://img.shields.io/badge/Django-4.2-darkgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Alumni Portal** is a robust platform designed to connect institutions, current students, and alumni, enabling networking, career opportunities, event management, and resource sharing.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [User Roles](#-user-roles)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Validation Logic](#-validation-logic)
- [Collaborators](#-collaborators)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Author](#-author)

---

## 🚀 Overview

**Alumni Portal** provides a centralized hub for an institution's community. It streamlines administrative tasks such as student registration and graduation tracking while offering students and alumni a platform to grow their professional networks.

---

## ✨ Features

- **User Authentication**: Secure login with role‑based redirection.
- **Student Onboarding**: Single and bulk registration (Excel/CSV).
- **Alumni Transition**: Automatic conversion of graduating students.
- **Career Hub**: Job and internship posting with skill matching.
- **Event Management**: Create and track events with image uploads.
- **Achievement Gallery**: Showcase successes with certificates.
- **Donation System**: Manage alumni donations and tracking.
- **Profile Management**: Detailed user profiles with resumes, social links, and skills.
- **Modern UI**: Light & Airy design with glassmorphism and smooth animations.

---

## 👥 User Roles

| Role | Capabilities |
|------|--------------|
| **Student** | Browse directory, view events, apply for jobs/internships, track achievements |
| **Alumni** | Post jobs/internships, create events, donate, professional networking |
| **Admin** | Manage departments, bulk registration, alumni conversion, full system control |

---

## 🗂 Project Structure

```text
Alumni-Portal/
│
├── alumni_portal/            # Project configuration (settings, urls, wsgi)
│
├── user/                     # Core application
│   ├── migrations/
│   ├── templates/user/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── static/                    # Global assets
│   ├── css/
│   └── images/
│
├── media/                     # Uploaded content (photos, resumes, certificates)
│
├── templates/                 # Global layout templates (base, home, login)
│
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

---

## 🧰 Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Python** | Core language |
| **Django 4.2** | Web framework |
| **SQLite** | Database |
| **Pandas / Openpyxl** | Bulk data processing |
| **HTML5 / CSS3** | Structure & styling |
| **JavaScript** | Interactivity |
| **Git & GitHub** | Version control |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/PrajwalItnal/Alumni-Portal.git
cd Alumni-Portal
```
### 2️⃣ Create a Virtual Environment
```bash
python -m venv .venv
```
### 3️⃣ Activate the Virtual Environment
**Windows:**
```bash
.venv\Scripts\activate
```
**Linux/macOS:**
```bash
source .venv/bin/activate
```
### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 5️⃣ Apply Migrations
```bash
python manage.py migrate
```
### 6️⃣ Run the Development Server
```bash
python manage.py runserver
```
### 🌐 Open in Browser
Visit **http://127.0.0.1:8000/**

---

## 🔁 Usage

- **Admin** can bulk import students and convert graduates to alumni.
- **Alumni** can post jobs/internships, create events, and manage donations.
- **Students** can search directories, apply for opportunities, and track achievements.

---

## 📺 Validation Logic

### ✅ Smart Onboarding
Enforces a 12‑character alphanumeric Register ID for both single and bulk registrations.

### 🔄 Date of Birth Rules
Minimum age of **15** years is required; no upper age limit.

---

## 👥 Collaborators

- **Prajwal Itnal** – [@PrajwalItnal](https://github.com/PrajwalItnal)
- **Deepa BL** – [@deepabl](https://github.com/deepabl)
- **Juned Fattekhan** – [@junedfattekhan5](https://github.com/junedfattekhan5)

---

## 🚧 Future Enhancements
- Advanced filtering by graduation year, industry, etc.
- Real‑time messaging between students and alumni.
- Automated email newsletters and event notifications.
- Mobile app for Android/iOS.
- PostgreSQL support for production scaling.

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 👤 Author

**Prajwal Itnal** – Programmer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/prajwal-itnal/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PrajwalItnal)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:prajwalitnal20@gmail.com)
