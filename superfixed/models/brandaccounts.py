from setup.basemodel import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BrandAccount(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(null=True, blank=True)
    slip_cover_image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=100)

    index_title = models.CharField(max_length=100, null=True, blank=True)
    dec = models.TextField(null=True, blank=True)

    abbr = models.CharField(max_length=100, null=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    momo_account_number = models.CharField(max_length=20, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Name: {self.name} Balance: {self.balance}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.name:
            self.abbr = self.name.lower()

        if self.logo:
            from PIL import Image

            img = Image.open(self.logo.path)

            max_size = (800, 800)
            img.thumbnail(max_size, Image.LANCZOS)

            img.save(self.logo.path, optimize=True, quality=85)


class Colors(BaseModel):
    name = models.CharField(max_length=100)
    hex_value = models.CharField()

    def __str__(self):
        return self.name


class Customization(BaseModel):
    brand = models.ForeignKey(
        BrandAccount, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    color_choice = models.ForeignKey(
        Colors, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
