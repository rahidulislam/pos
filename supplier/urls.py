from django.urls import path
from supplier import views
app_name = 'supplier'

urlpatterns = [
    path('', views.SupplierHomeView.as_view(), name='supplier_home'),
    path('create_supplier/', views.CreateSupplierView.as_view(), name='create_supplier'),
    path('update_supplier/<int:pk>/', views.UpdateSupplierView.as_view(), name='update_supplier'),
    path('delete_supplier/<int:pk>/', views.DeleteSupplierView.as_view(), name='delete_supplier'),
    path('detail_supplier/<int:pk>/', views.DetailSupplierView.as_view(), name='detail_supplier'),
]
