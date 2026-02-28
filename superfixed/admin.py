from django.contrib import admin
from superfixed.models.slips import *
from superfixed.models.brandaccounts import *

# Register your models here.


admin.site.register(Betslip)
admin.site.register(Transaction)

admin.site.register(BrandAccount)
admin.site.register(Colors)
admin.site.register(Customization)
admin.site.register(SlipCategory)
admin.site.register(SlipType)
