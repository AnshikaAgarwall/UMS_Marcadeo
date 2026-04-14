from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import User

# 🔐 LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_deleted:
                return render(request, "login.html", {"error": "Account deleted."})
            
            login(request, user)
            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "manager":
                return redirect("manager_dashboard")
            return redirect("user_dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials."})
            
    return render(request, "login.html")

# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('/login/')

# 👑 ADMIN DASHBOARD
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin': 
        return redirect('login')
    
    users = User.objects.filter(is_deleted=False)
    managers = User.objects.filter(role="manager", is_deleted=False)
    return render(request, "admin_dashboard.html", {"users": users, "managers": managers})


# 👨‍💼 MANAGER DASHBOARD
@login_required
def manager_dashboard(request):
    if request.user.role != 'manager': 
        return redirect('login')
    
    # CHANGE THIS LINE:
    # From: users = User.objects.filter(created_by=request.user, is_deleted=False)
    # To this:
    users = User.objects.filter(manager=request.user, is_deleted=False)
    
    return render(request, "manager_dashboard.html", {"users": users})

# ➕ ADD USER
@login_required
def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        # FIX: Ensure email is never None to avoid IntegrityError
        email = request.POST.get("email", "")  
        password = request.POST.get("password")
        role = request.POST.get("role")

        if username and password:
            # Hierarchy Logic: Managers can only create 'user' or 'manager'
            if request.user.role == 'manager' and role == 'admin':
                role = 'user'

            User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=role,
                created_by=request.user
            )
    return redirect(request.META.get('HTTP_REFERER', 'login'))

# 📝 EDIT USER
@login_required
def edit_user(request, id):
    user_to_edit = get_object_or_404(User, id=id)
    
    # Permission check: Admin can edit anyone, Managers can edit their own
    if request.user.role != 'admin' and user_to_edit.created_by != request.user and request.user != user_to_edit:
        return redirect('login')

    if request.method == "POST":
        user_to_edit.username = request.POST.get("username", user_to_edit.username)
        # FIX: Ensure email update doesn't crash if field is empty
        user_to_edit.email = request.POST.get("email", user_to_edit.email)
        user_to_edit.save()
        
        # Redirect back based on role
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'manager':
            return redirect('manager_dashboard')
        return redirect('user_dashboard')

    return render(request, "edit_user.html", {"user": user_to_edit})

# ❌ SOFT DELETE
@login_required
def delete_user(request, id):
    if request.method == "POST":
        user_to_delete = get_object_or_404(User, id=id)
        
        # Requirement: Managers cannot modify other managers’ users
        if request.user.role == 'admin' or user_to_delete.created_by == request.user:
            user_to_delete.is_deleted = True
            user_to_delete.save()
            
    return redirect(request.META.get('HTTP_REFERER', 'login'))

# 🔁 ASSIGN MANAGER
@login_required
def assign_manager(request, id):
    if request.user.role != 'admin':
        return redirect('login')

    if request.method == "POST":
        user_to_update = get_object_or_404(User, id=id)
        manager_id = request.POST.get("manager_id")

        if manager_id:
            manager_obj = get_object_or_404(User, id=manager_id, role="manager")
            user_to_update.manager = manager_obj
            user_to_update.save()
        else:
            # Logic to unassign manager if "None" selected
            user_to_update.manager = None
            user_to_update.save()

    return redirect("admin_dashboard")

# 👤 USER DASHBOARD
@login_required
def user_dashboard(request):
    # This view simply shows the logged-in user's own profile
    return render(request, "user_dashboard.html", {"user": request.user})