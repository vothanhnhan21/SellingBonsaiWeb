from django.contrib import admin
from .models import Plant,UserContact,CartItem, Invoice, InvoiceItem
# Register your models here.
admin.site.register(Plant)
admin.site.register(UserContact)
admin.site.register(CartItem)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)