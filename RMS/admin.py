from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Food,Review,Foodtype,orders,Bill,Table,Booking,ContactUs
# Register your models here.
admin.site.register(get_user_model())

# Register your models here.
admin.site.register(Food)

# Register your models here.
admin.site.register(Review)

# Register your models here.
admin.site.register(Bill)

# Register your models here.
admin.site.register(orders)

# Register your models here.
admin.site.register(Table)

#Register your models here.
admin.site.register(Booking)

#Register your models here.
admin.site.register(ContactUs)