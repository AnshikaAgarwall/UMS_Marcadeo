# 🛡️ TeamGuard: Role-Based Management System

A clean, centered, and professional User Management System built with **Django**. This application allows for hierarchical control where Admins manage the platform, Managers oversee assigned teams, and Users manage their own profiles.

---

## 🚀 Quick Setup Guide

Follow these steps to get the application running on your local machine:

1.  **Clone & Navigate:** Open your terminal and enter your project folder:
    ```bash
    cd usersystem
    ```

2.  **Environment Setup:**
    Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install django
    ```

4.  **Initialize Database:**
    Prepare the SQLite filing cabinet and create the first Admin account:
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5.  **Run the Engine:**
    ```bash
    python manage.py runserver
    ```
    Visit `http://127.0.0.1:8000/login/` to start.

---

## 🗄️ Database Schema (The User Model)

The heart of this project is a **Custom User Model** that extends Django's `AbstractUser`. Below is how the data is organized:

| Field | Type | Description |
| :--- | :--- | :--- |
| **username** | String | Unique identifier for login. |
| **role** | Choice | `admin`, `manager`, or `user`. |
| **created_by** | ForeignKey | Tracks which user created this account. |
| **manager** | ForeignKey | Links a `user` to a specific `manager`. |
| **is_deleted** | Boolean | Used for **Soft Deletes** (hides user without erasing data). |
| **email** | Email | User's contact address. |

---

## 🧠 Application Logic

### 1. The "Smart" Redirect
Upon a successful login using `authenticate()` and `login()`, the system checks the user's `role` attribute.
* **Admins** are sent to a global overview.
* **Managers** are sent to their team dashboard.
* **Users** are sent to their personal profile page.



### 2. Hierarchical Privacy
* **Global Access:** Admins can see every user in the database.
* **Scoped Access:** Managers use a specific filter: `User.objects.filter(manager=request.user)`. They only see people specifically assigned to them by the Admin.
* **Self Access:** Regular users can only see and edit their own `request.user` data.

### 3. Soft Delete Implementation
Instead of using `user.delete()`, which wipes data permanently, we use:
```python
user.is_deleted = True
user.save()
```
This ensures that the "TeamGuard" system maintains a historical record of all employees while preventing deactivated accounts from logging in.

---

## 🎨 UI & Aesthetics
The interface was built using **Bootstrap 5** with a focus on **SaaS-style minimalism**:
* **Centered Layout:** Content is restricted to a `max-width` container and centered vertically/horizontally to improve focus.
* **Marcadeo Brand Palette:** Uses a high-contrast deep blue (`#0056b3`) against a clean white and gray background.
* **Interactive Modals:** Adding users is handled via pop-up modals to keep the dashboard clean and fast.

---

## 🛠️ Built With
* **Django 6.0.4** - The core Python framework.
* **SQLite** - For lightweight, reliable data storage.
* **Inter Font** - For professional, readable typography.
* **Logic:** Custom Middleware-like role checks and Soft-Delete filtering.
