from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.
class Food(models.Model):
    Food_Name = models.CharField(max_length = 100)
    Food_Price = models.IntegerField()
    Discount_In_Percentage = models.IntegerField(blank=True,null = True)
    Food_Avg_Rating = models.FloatField(null = True)
    Food_Type = models.CharField(max_length = 100)
    Description = models.CharField(max_length  = 5000)
    food_pic = models.ImageField(upload_to='Food/', blank = True, null = True)
    users = models.IntegerField(null = True)
    def __str__(self):
        return self.Food_Name

class Foodtype(models.Model):
    food_type = models.CharField(max_length=60)
    def __str__(self):
        return self.food_type
        

# Creating custom  user models here.
class MyUserManager(BaseUserManager):
    def profile_pic(self,profile_pic):
        user = self.model(
            profile_pic = profile_pic
        )
    def create_user(self,email,Name,phone,Address,pincode,city,state,password = None):
        if not email:
            raise ValueError("Email is required")
        if not Name:
            raise ValueError("Name is required")
        if not phone:
            raise ValueError("Please provide an active phone number")
        if not Address:
            raise ValueError("Please Provide Address")
        user = self.model(
            email = self.normalize_email(email),
            Name = Name,
            phone = phone,
            Address = Address,
            pincode = pincode,
            city = city,
            state = state
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,email,Name,phone,Address,pincode = 302031,city = "Jaipur",state ="Rajasthan",password = None):
        user = self.create_user(
            email = email,
            Name = Name,
            phone = phone,
            password = password,
            Address  = Address,
            pincode = pincode,
            city = city,
            state = state,

        )
        user.is_admin = True
        user.is_staff =True
        user.is_superuser = True
        user.save(using = self._db)
        return user
       
class MyUser(AbstractBaseUser, PermissionsMixin): 
    Name = models.CharField(verbose_name = "Name",max_length = 50)
    email = models.EmailField(verbose_name = "email address",max_length = 60,unique = True,blank = True)
    Address = models.CharField(verbose_name = "Address",max_length = 200)
    state = models.CharField(verbose_name = "state",max_length = 100,null=True)
    city = models.CharField(verbose_name = "city",max_length = 100,null=True)
    pincode = models.CharField(verbose_name = "Pincode",max_length = 50,null=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank = True, null = True)
    phone = models.CharField(max_length = 20,verbose_name = "phone number")
    last_login = models.DateTimeField(verbose_name = "last login",auto_now = True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    penilty = models.FloatField(null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['Address','phone','Name']

    objects = MyUserManager()

    def __str__(self):
        return self.Name

    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True


# order model
class orders(models.Model):
    user = models.ForeignKey(MyUser,default=None,on_delete = models.CASCADE)
    food = models.ForeignKey(Food,default=None, on_delete = models.CASCADE)
    date_time = models.DateTimeField('date published')
    order_address = models.CharField(max_length=5000)
    state = models.CharField(max_length=5000,null=True)
    city = models.CharField(max_length=5000,null=True)
    pincode = models.CharField(max_length=5000,null=True)
    quantity = models.IntegerField()
    deliver_status = models.BooleanField(default=False)
    total_amount = models.FloatField(null=True)
    

    def __str__(self):
        return self.user.email

#Bill Model
class Bill(models.Model):
    order_no = models.ForeignKey(orders,default=None,on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser,default=None,on_delete = models.CASCADE)
    food = models.ForeignKey(Food,default=None, on_delete = models.CASCADE)
    payment_status = models.BooleanField(default=False)
    discount = models.PositiveIntegerField()
    tex = models.PositiveIntegerField()
    penilty = models.PositiveIntegerField(null = True)
    total_amount = models.FloatField(null= True)

    def __str__(self):
        return self.user.Name
# FeedBack Model
class Review(models.Model):
    user = models.ForeignKey(MyUser,default=None,on_delete = models.CASCADE)
    food = models.ForeignKey(Food,default=None, on_delete = models.CASCADE)
    content = models.CharField(max_length=5000)
    rate = models.PositiveIntegerField()
    date_time = models.DateTimeField(null=True)
    def __str__(self):
        return self.user.Name


# Book Table 
class Table(models.Model):
    capicity = models.PositiveIntegerField()
    Table_pic = models.ImageField(upload_to='Tables/', blank = True, null = True)


class Booking(models.Model):
    user = models.ForeignKey(MyUser,default=None,on_delete = models.CASCADE)
    table = models.ForeignKey(Table,default=None, on_delete = models.CASCADE)
    date_time = models.DateTimeField()
    capicity = models.PositiveIntegerField()
    Conform = models.BooleanField(null= True,default=False)
    Booking_time = models.DateTimeField(null= True)

    def __str__(self):
        return self.user.email

class ContactUs(models.Model):
    Name = models.CharField(max_length=5000, null= True)
    Email = models.CharField(max_length=6000,null  = True)
    message = models.CharField(max_length = 7000)
    def __str__(self):
        return self.Email

    
