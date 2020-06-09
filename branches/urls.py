from django.urls import path
from branches import views

app_name = 'branches'

urlpatterns = [
    path('', views.BranchHomeView.as_view(), name='branch_home'),
    path('create_branch/', views.CreateBranchView.as_view(), name='create_branch'),
    path('update_branch/<int:pk>/', views.UpdateBranchView.as_view(), name='update_branch'),
    path('delete_branch/<int:pk>/', views.DeleteBranchView.as_view(), name='delete_branch'),
]
