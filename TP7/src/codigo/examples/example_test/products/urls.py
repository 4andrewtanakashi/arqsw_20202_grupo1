from django.urls import path
from .views import list_products, delete_product

urlpatterns = [
    path('', list_products, name='list_products'),
    path('delete/<int:id>/', delete_product, name='delete_product'),
]
