from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Plant(models.Model):
    # Basic fields for a plant
    plant_name = models.CharField(max_length=100)  # Name of the plant
    plant_type = models.CharField(max_length=50)  # Type of plant (e.g., flower, tree, shrub)
    description = models.TextField()  # Description of the plant
    image = models.CharField(max_length=50, null=True, blank=True)  # Optional image of the plant
    orgin = models.CharField(max_length=50)
    price = models.FloatField()
    quality = models.IntegerField()

    def __str__(self):
        return (f"name: {self.plant_name}, type: {self.plant_type}, description: {self.description}, orgin: {self.orgin}, price: {self.price}, quality: {self.quality}")

class UserContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contact')  # Liên kết với User mặc định
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    product = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.plant_name}'
        
    def total_price(self):
        # Giả sử model Product có trường price để lưu giá của sản phẩm
        return self.product.price * self.quantity

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')  # Người mua
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Tổng tiền hóa đơn
    status = models.CharField(max_length=20, choices=[('pending', 'Đang chờ'), ('paid', 'Đã thanh toán'), ('cancelled', 'Hủy')], default='pending')  # Trạng thái hóa đơn
    created_at = models.DateTimeField(default=timezone.now)  # Thời gian tạo
    updated_at = models.DateTimeField(auto_now=True)  # Thời gian cập nhật
    
    def __str__(self):
        return f"Hóa đơn #{self.id} - {self.status}"
    
    def update_total_amount(self):
        """Cập nhật tổng số tiền hóa đơn dựa trên các mục trong hóa đơn."""
        self.total_amount = sum(item.total_price() for item in self.items.all())
        self.save()

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)  # Hóa đơn liên kết
    product = models.ForeignKey(Plant, on_delete=models.CASCADE)  # Sản phẩm đã mua
    quantity = models.PositiveIntegerField(default=1)  # Số lượng sản phẩm mua
    price_at_time_of_purchase = models.DecimalField(max_digits=10, decimal_places=2)  # Giá tại thời điểm mua
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Tổng tiền sản phẩm trong hóa đơn
    
    def save(self, *args, **kwargs):
        """Tự động tính tổng tiền khi lưu mục hóa đơn."""
        self.total_price = self.quantity * self.price_at_time_of_purchase
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"