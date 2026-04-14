from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),  # Change '' to 'login/'
    path('', views.login_view),                      # Optional: also catch the base URL
    path('logout/', views.logout_view, name="logout"),
    path('admin-dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('manager-dashboard/', views.manager_dashboard, name="manager_dashboard"),
    path('user-dashboard/', views.user_dashboard, name="user_dashboard"),
    path('add-user/', views.add_user, name="add_user"),
    path("assign-manager/<int:id>/", views.assign_manager, name="assign_manager"),
    path("edit-user/<int:id>/", views.edit_user, name="edit_user"),
    path("delete-user/<int:id>/", views.delete_user, name="delete_user"),
]