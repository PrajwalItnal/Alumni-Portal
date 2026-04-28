# 📺 LearnTube Hub  
### A YouTube-Powered E-Learning Platform built with Django

![Django](https://img.shields.io/badge/Django-6.0-darkgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **LearnTube Hub** is a lightweight Learning Management System (LMS) that allows users to publish, explore, and save **YouTube-based educational courses** with automatic video embedding.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [User Roles](#-user-roles)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [YouTube Embedding Logic](#-youtube-embedding-logic)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Author](#-author)

---

## 🚀 Overview

**LearnTube Hub** is designed for learners and content creators who want a **simple and distraction‑free platform** for sharing educational content hosted on YouTube.

✔ Built‑in Course Certifications  
✔ Progress tracking & resume functionality  
✔ No paid courses  
✔ Focus on accessible learning & sharing

---

## ✨ Features

- User authentication (Signup / Login / Logout)
- Role‑based access (Student & Publisher)
- Publish YouTube‑based courses with unique URL validation
- Automatic YouTube link embedding
- Course enrollment and precise progress tracking
- "Resume where you left off" video functionality
- Automated certificate generation upon completion
- Save courses using AJAX
- Responsive embedded video player

---

## 👥 User Roles

| Role      | Capabilities |
|-----------|--------------|
| **Student** | Browse, enroll, track progress, earn certificates & save courses |
| **Publisher** | Upload & manage courses |
| **Admin** | Full control via Django Admin |

---

## 🗂 Project Structure

```text
LearnTube-Hub/
│
├── LearnTube/                # Project settings
│
├── users/                    # Main app
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── static/
│   └── css/
│       ├── styles.css
│       ├── login.css
│       ├── signup.css
│       ├── profile.css
│       └── upload.css
│
├── templates/
│   └── base.html
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧰 Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Backend logic |
| **Django 6.0** | Web framework |
| **SQLite** | Database |
| **HTML5** | Templates |
| **CSS3** | Styling |
| **JavaScript** | AJAX interactions |
| **Git & GitHub** | Version control |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/PrajwalItnal/LearnTube-Hub.git
cd LearnTube-Hub
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
```

### 3️⃣ Activate the Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```
**Linux / macOS:**
```bash
source venv/bin/activate
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
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** after the server starts.

---

## 🔁 Usage

### 👨🏫 Publisher
* **Register / Login:** Create and manage your account.
* **Upload:** Paste YouTube course links.
* **Automatic Embedding:** Courses are instantly viewable.

### 👨🎓 Student
* **Register / Login:** Create your learning profile.
* **Browse:** Explore all available courses.
* **Enroll & Track:** Enroll in courses and track your watch progress.
* **Earn Certificates:** Complete courses to generate personalized certificates.
* **Save:** Keep favorite courses in your library.
* **Watch:** Seamless "resume where you left off" tracking.

---

## 📺 YouTube Embedding Logic

### ✅ Supported URLs
* `https://www.youtube.com/watch?v=VIDEO_ID`
* `https://youtu.be/VIDEO_ID`

### 🔄 Automatic Conversion
The system converts these links to the embed format:
* `https://www.youtube.com/embed/VIDEO_ID`

> [!CAUTION]
> If a creator has disabled embedding, a "Watch on YouTube" fallback link is shown.

---

## ⚠️ Limitations
* No payment gateway integration.
* Limited by YouTube's embedding settings.

---

## 🚧 Future Enhancements
- [ ] Search & Filters by keywords
- [ ] Category & tag organization
- [ ] Comments & star ratings
- [ ] Deployment on Render or Railway
- [ ] PostgreSQL support for production

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 👤 Author

**Prajwal Itnal** *Computer Applications Student | Data Enthusiast*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/prajwal-itnal/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PrajwalItnal)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:prajwalitnal20@gmail.com)

---

## 👥 Collaborators

- **Prajwal Itnal** ([@PrajwalItnal](https://github.com/PrajwalItnal))
- **Deepa BL** ([@deepabl](https://github.com/deepabl))
- **Juned Fattekhan** ([@junedfattekhan5](https://github.com/junedfattekhan5))

---
