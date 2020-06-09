from django.urls import path
from staff import views
app_name='staff'

urlpatterns = [
    path('', views.HomeView.as_view(), name='staff_home'),
    path('set_permissions/<int:pk>/', views.SetPermissions.as_view(), name='set_permission'),
    path('change_branch/<int:pk>/', views.ChangeBranch.as_view(), name='change_branch'),
    path('create_staff/', views.CreateStaff.as_view(), name='create_staff'),
    path('update_staff/<int:pk>', views.StaffUpdate.as_view(), name='update_staff'),
    path('delete_staff/<int:pk>', views.DeleteStaff.as_view(), name='delete_staff'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('update_password/<int:pk>', views.UpdatePassword.as_view(), name='update_password'),
    path('staffpage/', views.StaffPageView.as_view(), name='staffpage'),
]
