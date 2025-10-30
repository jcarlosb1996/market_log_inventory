from django.db import models
from django.utils import timezone

class Item(models.Model):
    title = models.CharField(max_length=150)
    # Treat these as PER-UNIT values
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ask_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to="items/", blank=True, null=True)

    # Inventory
    quantity = models.PositiveIntegerField(default=1)

    # Derived/UX fields
    is_sold = models.BooleanField(default=False)
    sold_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class Marketplace(models.TextChoices):
    FACEBOOK = "FACEBOOK", "Facebook"
    EBAY = "EBAY", "eBay"

class Sale(models.Model):
    # Allow MULTIPLE sales per item
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="sales")
    channel = models.CharField(max_length=20, choices=Marketplace.choices)

    # Quantity in this transaction
    quantity = models.PositiveIntegerField(default=1)

    # Total sale price for this transaction (not per-unit)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Fees
    fee_rate_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # e.g., 13.00
    fee_flat = models.DecimalField(max_digits=10, decimal_places=2, default=0)     # e.g., 0.30
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Profit for this transaction
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def compute_fees_and_profit(self):
        pct_fee = (self.fee_rate_pct / 100) * self.sale_price
        self.fee_amount = pct_fee + self.fee_flat
        # cost is per-unit, so multiply by quantity
        total_cost = (self.item.cost or 0) * self.quantity
        self.net_profit = self.sale_price - self.fee_amount - total_cost

    def save(self, *args, **kwargs):
        self.compute_fees_and_profit()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.title} — {self.channel} x{self.quantity}"
