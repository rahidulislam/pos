from django.urls import path
from customers import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomerHomeView.as_view(), name='customer_home'),
    path('add_customer/', views.CustomerCreateView.as_view(), name='create_customer'),
    path('edit_customer/<int:pk>/', views.CustomerUpdateView.as_view(), name='edit_customer'),
    path('detail_customer/<int:pk>/', views.CustomerDetailView.as_view(), name='detail_customer'),
    path('delete_customer/<int:pk>/', views.CustomerDeleteView.as_view(), name='delete_customer'),
    
]