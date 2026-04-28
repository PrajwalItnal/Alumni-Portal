# 🎓 Alumni Portal  
### A Comprehensive Alumni Management System built with Django

![Django](https://img.shields.io/badge/Django-4.2-darkgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Alumni Portal** is a sophisticated platform designed to bridge the gap between educational institutions, current students, and alumni. It facilitates networking, career opportunities, event management, and resource sharing.

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

**Alumni Portal** provides a centralized hub for an institution's community. It streamlines administrative tasks like student registration and graduation tracking while offering students and alumni a platform to grow their professional networks.

✔ Professional Directory & Search  
✔ Job & Internship Boards  
✔ Event Coordination & RSVP  
✔ Donation Management & Tracking  

---

## ✨ Features

- **User Authentication**: Secure login system with role-based redirection.
- **Student Onboarding**: Support for both single and bulk registration (Excel/CSV).
- **Alumni Transition**: Automated conversion of graduating students to alumni status.
- **Career Hub**: Posting and filtering for jobs and internships with skill matching.
- **Event Management**: Create and track institutional events with image uploads.
- **Achievement Gallery**: Showcasing alumni and student successes with certificate uploads.
- **Resource Support**: Integrated donation system for alumni to support their alma mater.
- **Profile Management**: Detailed user profiles including resumes, social links, and skills.
- **Modern UI**: Clean, "Light & Airy" design with glassmorphism and smooth animations.

---

## 👥 User Roles

| Role | Capabilities |
|-----|-------------|
| **Student** | Browse directory, view events, apply for jobs/internships, track achievements |
| **Alumni** | Post jobs/internships, create events, donate, professional networking |
| **Admin** | Manage departments, bulk student registration, alumni conversion, full system control |

---

## 🗂 Project Structure

```text
Alumni-Portal/
│
├── alumni_portal/             # Project configuration (settings, urls, wsgi)
│
├── user/                      # Core application logic
│   ├── migrations/            # Database schema history
│   ├── templates/             # App-specific HTML templates
│   │   └── user/              # Modularized UI components
│   ├── models.py              # Data structures (User, Student, Alumni, Event, etc.)
│   ├── views.py               # Request handling & business logic
│   ├── urls.py                # App-level routing
│   └── admin.py               # Admin panel configuration
│
├── static/                    # Global assets
│   ├── css/                   # Modernized styling (modern.css)
│   └── images/                # UI illustrations and icons
│
├── media/                     # User-uploaded content (Photos, Resumes, etc.)
│
├── templates/                 # Global layout templates (base, home, login)
│
├── manage.py                  # Django CLI entry point
├── requirements.txt           # Project dependencies
├── db.sqlite3                 # Local database storage
└── README.md                  # Project documentation
```
---

## 🧰 Technology Stack

| Technology | Purpose |
|:---|:---|
| **Python** | Core Programming Language |
| **Django 4.2** | High-level Web Framework |
| **Pandas / Openpyxl** | Excel/CSV Processing for Bulk Registration |
| **SQLite** | Efficient Relational Database |
| **HTML5 / CSS3** | Semantic Structure & Glassmorphic Styling |
| **JavaScript** | Real-time Validation & UI Interactions |
| **Git & GitHub** | Distributed Version Control |

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
**Linux / macOS:**
```bash
source .venv/bin/activate
```
## 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
## 5️⃣ Apply Migrations
```bash
python manage.py migrate
```
## 6️⃣ Run the Development Server
```bash
python manage.py runserver
```
## 🌐 Open in Browser

Once the server is running, you can access the application at:

👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

### 🛠 Troubleshooting Connection
If the page doesn't load, ensure that:
1. Your virtual environment is still **activated**.
2. You have run the `python manage.py runserver` command without errors.
3. No other application is using port **8000**.

---

## 🔁 Usage

### 🛡 Admin
* **Bulk Import**: Quickly register an entire batch of students using Excel.
* **Convert Alumni**: Seamlessly transition students to alumni status upon graduation.
* **Manage Departments**: Configure academic divisions within the portal.

### 🎓 Alumni
* **Give Back**: Post job opportunities or internships for juniors.
* **Networking**: Connect with fellow alumni and organize events.
* **Profile**: Maintain a professional portfolio with links and achievements.

### 📖 Student
* **Explore**: Search for alumni in specific companies or departments.
* **Prepare**: View job requirements and apply through institutional links.
* **Engage**: Participate in alumni-led events and track professional milestones.

---

## 📺 Validation Logic

### ✅ Smart Onboarding
The system validates Register IDs to ensure they are exactly 12 characters and alphanumeric, preventing duplicate or malformed entries during both single and bulk registration.

### 🔄 Date of Birth Rules
The profile update system enforces a minimum age of 15 for safety while allowing alumni of all ages to maintain active records without restrictive upper limits.

> [!TIP]
> **Pro Tip:** When uploading bulk data, ensure your Excel headers match: `register id`, `name`, `email`, `phone`, and `gender`.

---

## ⚠️ Limitations
* Custom user model is not integrated with Django's built-in auth backend.
* SMTP credentials are stored in plain text in `settings.py`.
* No payment gateway integration for donations.

---

## 👥 Collaborators

This project was made possible by the following contributors:

- **Prajwal Itnal** ([@PrajwalItnal](https://github.com/PrajwalItnal))
- **Deepa BL** ([@deepabl](https://github.com/deepabl))
- **Juned Fattekhan** ([@junedfattekhan5](https://github.com/junedfattekhan5))

---

## 🚧 Future Enhancements
- [ ] **Advanced Filtering**: Search by graduation year range or industry sector.
- [ ] **Real-time Messaging**: Direct chat between students and alumni.
- [ ] **Automated Emails**: Newsletter and event notifications.
- [ ] **Mobile App**: Dedicated Android/iOS client for the portal.
- [ ] **PostgreSQL**: Scaling to a robust production database.

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 👤 Author

**Prajwal Itnal** *Computer Applications Student | Data Enthusiast*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/prajwal-itnal/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PrajwalItnal)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:prajwalitnal20@gmail.com)

---
