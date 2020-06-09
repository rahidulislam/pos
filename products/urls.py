from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductHomeView.as_view(), name='product_home'),
    path('create_product/', views.CreateProductView.as_view(), name='create_product'),
    path('product_detail/<int:pk>/', views.ProductDetailView.as_view(), name='detail_product'),
    path('update_product/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete_product/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('add_transfer/', views.ProductAddTransfer.as_view(), name='add_transfer'),
    path('transfer_product/', views.TransferProduct.as_view(), name='transfer_product'),
    path('set_transfer_to/', views.SetTransferTO.as_view(), name='set_transfer_to'),
    path('delete_cart_product/<int:product_id>/', views.DeleteCartProduct.as_view(), name='delete_cart_product'),
    path('clear_list/', views.ClearList.as_view(), name='clear_list'),
]
