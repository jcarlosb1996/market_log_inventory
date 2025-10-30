from django import forms
from .models import Item, Sale

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "cost", "ask_price", "notes", "image", "quantity"]

class QuickSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["quantity", "sale_price", "fee_rate_pct", "fee_flat"]
        labels = {
            "sale_price": "Unit price",   # clarify meaning
        }

    def __init__(self, *args, **kwargs):
        max_qty = kwargs.pop("max_qty", None)
        super().__init__(*args, **kwargs)
        self.fields["quantity"].min_value = 1
        if max_qty:
            self.fields["quantity"].max_value = max_qty
