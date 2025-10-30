from django.urls import path
from . import views

urlpatterns = [
    path("", views.inventory, name="inventory"),
    path("add/", views.add_item, name="add_item"),
    path("<int:item_id>/sell/<str:channel>/", views.sell, name="sell"),
    path("sales/", views.sales_history, name="sales_history"),
    path("sales/delete/<int:sale_id>/", views.delete_sale, name="delete_sale"),
    path("item/delete/<int:item_id>/", views.delete_item, name="delete_item"),

]
