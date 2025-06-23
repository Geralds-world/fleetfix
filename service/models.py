from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=50)
    service_date = models.DateField()
    kilometers = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class JobMarker(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)  # 👈 This line is critical
    number = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='markers/', blank=True, null=True)
    high_risk = models.BooleanField(default=False)


