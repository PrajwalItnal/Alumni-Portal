# 🎓 Alumni Portal  
### A Sophisticated Alumni Management & Networking Ecosystem built with Django

![Django](https://img.shields.io/badge/Django-4.2-darkgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Alumni Portal** is more than just a directory; it's a dynamic ecosystem designed to foster lifelong connections between an institution, its students, and its graduates. Built with a focus on scalability, security, and premium user experience.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Core Modules](#-core-modules)
- [Key Features](#-key-features)
- [User Roles](#-user-roles)
- [Project Structure](#-project-structure)
- [Technical Highlights](#-technical-highlights)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage Workflow](#-usage-workflow)
- [Validation & Security](#-validation--security)
- [Collaborators](#-collaborators)
- [Future Roadmap](#-future-roadmap)
- [License](#-license)
- [Author](#-author)

---

## 🚀 Overview

The **Alumni Portal** serves as the digital backbone for institutional community engagement. It bridges the gap between academic learning and professional success by providing a platform for mentorship, career advancement, and resource sharing.

✔ **Dynamic Networking**: Real-time search and filtering of professional records.  
✔ **Career Acceleration**: Integrated job and internship boards with skill-matching logic.  
✔ **Institutional Growth**: Streamlined donation and event management modules.  

---

## 📦 Core Modules

### 👤 Profile & Identity
Detailed user profiles supporting resume uploads, social links (LinkedIn/GitHub), and dynamic skill tagging.

### 💼 Career Hub
A dual-purpose board for Jobs and Internships. Alumni can post opportunities, and students can view them with "Skill Match" indicators.

### 📅 Events & Engagement
Full-lifecycle event management including scheduling, location tracking, and RSVP management with visual media support.

### 🏆 Achievement Gallery
A dedicated space to celebrate institutional excellence, allowing users to upload certificates and share professional milestones.

### 💰 Donation Management
A transparent system for alumni to support institutional projects, featuring secure record-keeping and contribution history.

---

## ✨ Key Features

- **Automated Onboarding**: Bulk student registration via Excel/CSV with intelligent error reporting.
- **Graduation Workflow**: One-click transition from "Student" to "Alumni" status, preserving history while unlocking new permissions.
- **Glassmorphic UI**: A premium, modern interface featuring smooth CSS animations and a "Light & Airy" aesthetic.
- **Smart Validation**: Real-time backend validation for Register IDs, Age requirements, and File formats.
- **Responsive Design**: Fully optimized for Desktop, Tablet, and Mobile viewing.

---

## 👥 User Roles

| Role | Capabilities |
|-----|-------------|
| **Student** | Search directory, view events, apply for jobs, track personal achievements |
| **Alumni** | Post jobs/internships, create community events, donate, professional mentorship |
| **Admin** | Bulk data management, department configuration, system-wide analytics |

---

## 🗂 Project Structure

```text
Alumni-Portal/
│
├── alumni_portal/             # Core System (settings, global URLs, configuration)
│
├── user/                      # Business Logic Layer
│   ├── migrations/            # Version-controlled schema updates
│   ├── templates/             # App-specific UI components
│   ├── models.py              # Relational Database Schema
│   ├── views.py               # Functional controllers & processing
│   └── urls.py                # Intelligent routing
│
├── static/                    # Design System
│   ├── css/                   # modern.css (Glassmorphism & Layout)
│   └── images/                # Branding & Vector Assets
│
├── media/                     # User Assets (Encrypted/Validated storage)
│
├── templates/                 # Global UI layouts (base, home, login)
│
├── manage.py                  # Orchestration CLI
├── requirements.txt           # Dependency management
├── db.sqlite3                 # Portable database
└── README.md                  # System Documentation
```

---

## 💡 Technical Highlights

- **Data Processing**: Leverages `Pandas` for high-performance bulk data parsing and `Openpyxl` for Excel integration.
- **Security**: Implements Django’s secure session management and CSRF protection.
- **Validation**: Strict server-side logic for Register IDs (12-char alphanumeric) and Age (15+ years).
- **State Management**: Uses Django’s Session engine to handle role-based access control (RBAC).

---

## 🧰 Technology Stack

| Technology | Purpose |
|:---|:---|
| **Python** | Backend Engineering |
| **Django 4.2** | Enterprise Web Framework |
| **SQLite** | Efficient Relational Storage |
| **HTML5 / CSS3** | Structural Semantics & Modern Styling |
| **JavaScript** | Client-side Interactivity |
| **Pandas** | Bulk Data Manipulation |
| **Git / GitHub** | Version Control & Collaboration |

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
### 3️⃣ Activate and Install
**Windows:**
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```
**Linux / macOS:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```
### 4️⃣ Database Setup & Run
```bash
python manage.py migrate
python manage.py runserver
```

---

## 🔁 Usage Workflow

1. **Admin** logs in and uploads the student list via Excel.
2. **Students** register, update profiles, and explore the directory.
3. Upon graduation, **Admin** converts students to **Alumni**.
4. **Alumni** post career opportunities and engage in events.

---

## 🛡 Validation & Security

- **Register ID**: Enforced 12-character unique alphanumeric format.
- **File Safety**: Uploads are restricted by size (2MB) and type (.jpg, .png, .pdf).
- **Age Logic**: Minimum 15-year threshold for student/alumni records.
- **Session Security**: Role-based redirection prevents unauthorized access to Admin modules.

---

## 👥 Collaborators

This project was built with collaboration from:

- **Prajwal Itnal** ([@PrajwalItnal](https://github.com/PrajwalItnal))
- **Deepa BL** ([@deepabl](https://github.com/deepabl))
- **Juned Fattekhan** ([@junedfattekhan5](https://github.com/junedfattekhan5))

---

## 🚧 Future Roadmap
- [ ] **AI-Powered Mentorship**: Automated matching of students with alumni mentors.
- [ ] **Job Referrals**: Internal referral system for job postings.
- [ ] **Verified Badges**: Admin-verified alumni profiles.
- [ ] **Email Notifications**: Automated alerts for new jobs and events.
- [ ] **Data Export**: PDF/CSV exports for administrative reporting.

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 👤 Author

**Prajwal Itnal** – Programmer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/prajwal-itnal/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PrajwalItnal)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:prajwalitnal20@gmail.com)

---
