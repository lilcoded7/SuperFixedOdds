from setup.basemodel import BaseModel
from PIL import Image
from django.db import models

class Betslip(BaseModel):
    image = models.ImageField()
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    odd = models.CharField(max_length=100)
    booking_code = models.CharField(max_length=100, null=True, blank=True)
   

    is_active=models.BooleanField(default=False)

    def __str__(self):
        return f"Name {self.name} - Odds: {self.odd} booking Code: {self.booking_code}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            from PIL import Image
            img = Image.open(self.image.path)

            max_size = (800, 800)
            img.thumbnail(max_size, Image.LANCZOS)

            img.save(self.image.path, optimize=True, quality=85)



class Transaction(BaseModel):
    slip = models.ForeignKey(Betslip, on_delete=models.PROTECT, null=True, blank=True)
    phone = models.CharField(max_length=10)
    status= models.CharField(max_length=100, choices=[('pending', 'pending'), ('sccess', 'success'), ('failed', 'failed')], null=True, blank=True)
    network = models.CharField(null=True, blank=True)
    channel = models.CharField(max_length=100, choices=[('ussd', 'ussd'), ('web', 'web')], null=True,blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Slip: {self.slip.name} | Phone: {self.phone} | Amount: {self.amount}"