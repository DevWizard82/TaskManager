# 📝 TaskMaster — Professional Task Management System

TaskMaster is a high-performance, role-based task management application built with **Django** and **MySQL**. Designed for teams and individuals who value productivity, it offers a streamlined interface for tracking, assigning, and completing tasks with automated notifications and smart deadline management.

---

## 🚀 Key Features

### 🔹 Unified Task Workspace
- **Dynamic CRUD**: Seamlessly create, update, and delete tasks with rich metadata.
- **Smart Status Management**: Quickly toggle between *To Do*, *In Progress*, and *Completed*.
- **Categorization**: Organize work into color-coded categories for better visual hierarchy.

### 🔹 Advanced Intelligence & Filtering
- **Contextual Search**: Find any task instantly using full-text search.
- **Deadline Analytics**: Filter tasks by proximity (Today, This Week, This Month) or view all overdue items.
- **Visual Urgency Indicators**: Automatic highlighting of overdue tasks and those approaching deadlines within 48 hours.

### 🔹 Team & Admin Oversight
- **Role-Based Access (RBAC)**: Users manage their personal workload; Administrators gain a bird's-eye view of the entire organization.
- **Automated Assignments**: Admins can delegate tasks to any user.
- **Email Notifications**: Instant SMTP-driven email alerts when a user is assigned a new responsibility.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Django 4.2+ (Python) |
| **Database** | MySQL |
| **Authentication** | Django Auth System |
| **Notifications** | SMTP (Gmail Integration) |
| **Security** | `python-dotenv` for environment isolation |

---

## 🔧 Installation & Setup

### 1. Prerequisites
- Python 3.8+
- MySQL Server
- Gmail Account (for SMTP notifications)

### 2. Clone & Environment Setup
```bash
git clone https://github.com/your-repo/taskmaster.git
cd taskmaster
```

### 3. Install Dependencies
```bash
pip install django mysqlclient python-dotenv
```

### 4. Database Configuration
Create a database named `taskmaster_db` in your MySQL instance:
```sql
CREATE DATABASE taskmaster_db;
```

### 5. Environment Variables
Create a `.env` file in the root directory and configure your credentials:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
> **Note:** Use a Gmail "App Password" if you have 2FA enabled.

### 6. Initialize the Application
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to start managing your tasks.

---

## 📁 Project Structure

```text
├── TaskManager/         # Core project settings and configuration
├── tasks/               # Main application logic, models, and views
│   ├── templates/       # Professional HTML interfaces
│   ├── forms.py         # Advanced form validation and styling
│   └── models.py        # Database schema and business logic
├── manage.py            # Django management CLI
└── .env                 # Sensitive configuration (excluded from Git)
```

---

## 🔒 Security & Compliance
- **CSRF Protection**: Enabled on all forms.
- **Password Hashing**: Industry-standard PBKDF2.
- **Environment Isolation**: No secrets stored in the codebase.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed with focus on efficiency and scalability.*
