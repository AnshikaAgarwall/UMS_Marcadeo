🧠 PROJECT SUMMARY (User Management System – Django)
🎯 What you are building

A Role-Based User Management System with:

Roles: Admin / Manager / User
Features:
Login system
Role-based dashboards
Add user (Admin)
Assign manager to users
Soft delete users
Search & filter users
Last login tracking (planned/partial)

🏗️ PROJECT SETUP
Project:
usersystem/
App:
usermanagementsystem/
Custom User Model:
AUTH_USER_MODEL = 'usermanagementsystem.User'

⚙️ TECHNOLOGY STACK
Django 6.0.4
Django REST Framework
SimpleJWT authentication
SQLite database
Bootstrap UI


👤 USER MODEL (IMPORTANT LOGIC)

You created a custom user model with:

role (admin / manager / user)
created_by (ownership hierarchy)
manager (assignment relationship)
is_deleted (soft delete)
last_login_time



🔐 AUTH SYSTEM
Uses authenticate() + login()
Redirects based on role:
admin → admin_dashboard
manager → manager_dashboard
user → user_dashboard

📊 DASHBOARDS
👑 Admin Dashboard
Shows all users
Can:
Add users
Delete users (soft delete)
Assign managers
Search/filter users
👨‍💼 Manager Dashboard

Shows only:
User.objects.filter(created_by=request.user)

👤 User Dashboard
Shows only personal profile