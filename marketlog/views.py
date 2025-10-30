from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError, transaction
from .models import Item, Sale, Marketplace
from .forms import ItemForm, QuickSaleForm
from django.db.models import Sum,Q


def sales_history(request):
    sales = Sale.objects.select_related("item").order_by("-created_at")
    totals = sales.aggregate(
        gross=Sum("sale_price"),
        fees=Sum("fee_amount"),
        net=Sum("net_profit"),
    )
    return render(request, "marketlog/sales_history.html", {
        "sales": sales,
        "totals": totals,
    })

def inventory(request):
    items = Item.objects.order_by("-id")

    # Item-level counts (based on what's shown here)
    distinct_items = items.count()
    in_stock_items = items.filter(quantity__gt=0).count()
    sold_out_items = items.filter(quantity=0).count()
    units_in_stock = items.aggregate(total=Sum("quantity"))["total"] or 0

    # Sales breakdown (all-time; adjust if you want date filtering)
    sales_agg = Sale.objects.aggregate(
        sold_units=Sum("quantity"),
        sold_fb=Sum("quantity", filter=Q(channel=Marketplace.FACEBOOK)),
        sold_ebay=Sum("quantity", filter=Q(channel=Marketplace.EBAY)),
    )
    stats = {
        "distinct_items": distinct_items,
        "in_stock_items": in_stock_items,
        "sold_out_items": sold_out_items,
        "units_in_stock": units_in_stock,
        "sold_units": sales_agg["sold_units"] or 0,
        "sold_fb": sales_agg["sold_fb"] or 0,
        "sold_ebay": sales_agg["sold_ebay"] or 0,
    }

    return render(request, "marketlog/inventory.html", {
        "items": items,
        "stats": stats,
    })


def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    if request.method == "POST":
        sale.delete()
        messages.success(request, "Sale deleted successfully.")
    return redirect("sales_history")

def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        item.delete()
        messages.success(request, "item deleted successfully.")
    return redirect("inventory")

def add_item(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        item = form.save()
        # keep UX flags in sync
        if item.quantity > 0:
            item.is_sold = False
            item.sold_at = None
            item.save(update_fields=["is_sold", "sold_at"])
        return redirect("inventory")
    return render(request, "marketlog/add_item.html", {"form": form})

def sell(request, item_id, channel):
    item = get_object_or_404(Item, pk=item_id)

    if item.quantity == 0:
        messages.error(request, "This item is sold out.")
        return redirect("inventory")

    channel = channel.upper()
    # defaults assume selling 1 unit
    defaults = {
        "quantity": 1,
        "sale_price": (item.ask_price or 0),  # total for this sale; will multiply in UI if you change quantity
        "fee_rate_pct": 0 if channel == "FACEBOOK" else 13.0,
        "fee_flat": 0 if channel == "FACEBOOK" else 0.30,
    }

    form = QuickSaleForm(request.POST or None, initial=defaults, max_qty=item.quantity)

    if request.method == "POST" and form.is_valid():
        qty = form.cleaned_data["quantity"]
        if qty > item.quantity:
            messages.error(request, f"Not enough stock. Available: {item.quantity}.")
            return redirect("inventory")

        sale = form.save(commit=False)
        sale.item = item
        sale.channel = Marketplace.FACEBOOK if channel == "FACEBOOK" else Marketplace.EBAY

        unit_price = form.cleaned_data["sale_price"]
        sale.sale_price = unit_price * qty

        with transaction.atomic():
            sale.save()
            # decrement stock
            item.quantity -= qty
            if item.quantity <= 0:
                item.quantity = 0
                item.is_sold = True
                item.sold_at = timezone.now()
            item.save(update_fields=["quantity", "is_sold", "sold_at"])

        messages.success(request, f"Sold {qty} of '{item.title}' on {sale.channel}. Net: ${sale.net_profit}")
        return redirect("inventory")

    return render(request, "marketlog/sell.html", {"item": item, "form": form, "channel": channel})


