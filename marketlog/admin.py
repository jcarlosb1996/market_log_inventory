from django.contrib import admin
from .models import Item, Sale
from .models import Item



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "cost", "ask_price", "is_sold", "sold_at")
    list_filter = ("is_sold",)
    search_fields = ("title",)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("item", "channel", "sale_price", "fee_amount", "net_profit", "created_at")
    list_filter = ("channel",)
    search_fields = ("item__title",)
