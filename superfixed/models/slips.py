from setup.basemodel import BaseModel
from PIL import Image
from django.db import models
from superfixed.models.brandaccounts import BrandAccount

class SlipCategory(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 
    
class SlipType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class Betslip(BaseModel):
    STATUS = [
        ('pending', 'pending'),
        ('won', 'won'),
        ('lost', 'lost')
    ]

    brand = models.ForeignKey(BrandAccount, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField()
    name = models.CharField(max_length=100)
    dec = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    type = models.ForeignKey(SlipType, on_delete=models.SET_NULL, null=True, blank=True)
    odd = models.CharField(max_length=100)
    booking_code = models.CharField(max_length=100, null=True, blank=True)
    category= models.ForeignKey(SlipCategory, on_delete=models.SET_NULL, null=True, blank=True)
   

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
    TRANS_TYPE = [
        ('withdrawal', 'withdrawal'),
        ('collection', 'collection'),
    ]
    brand = models.ForeignKey(BrandAccount, on_delete=models.SET_NULL, null=True, blank=True)
    slip = models.ForeignKey(Betslip, on_delete=models.PROTECT, null=True, blank=True)
    phone = models.CharField(max_length=10)
    status= models.CharField(max_length=100, choices=[('pending', 'pending'), ('sccess', 'success'), ('failed', 'failed')], null=True, blank=True)
    network = models.CharField(null=True, blank=True)
    channel = models.CharField(max_length=100, choices=[('ussd', 'ussd'), ('web', 'web')], null=True,blank=True)
    trans_type = models.CharField(max_length=100, choices=TRANS_TYPE, null=True, blank=True, default='collection')
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Slip: {self.slip.name} | Phone: {self.phone} | Amount: {self.amount}"
    





