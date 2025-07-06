from django.urls import path
from . import views
from . import views_pdf

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('list/', views.invoice_list, name='invoice_list'),
    path('<int:invoice_id>/pdf/', views_pdf.download_invoice_pdf, name='download_invoice_pdf'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),

    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
