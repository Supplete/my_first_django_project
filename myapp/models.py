from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# CUSTOMER
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
from django.db import models



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # unread/read status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class MessageReply(models.Model):
    contact_message = models.ForeignKey(ContactMessage, on_delete=models.CASCADE, related_name='replies')
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.contact_message.name} by {self.admin.username}"


# VEHICLE
class Vehicle(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    make_model = models.CharField(max_length=100)
    registration = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='vehicles/')
    last_service = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.make_model} ({self.registration})"

# BOOKING
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    service_type = models.CharField(max_length=100)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.service_type}"
    
class SparePart(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='spareparts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
