from django import template
from django.contrib import messages
import math
from reportlab.pdfgen import canvas
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render
from .templatetags.cart import final_amount, discount_calculater,cart_count
from django.utils import timezone
from .models import Food,Review, orders, Bill,Table,Booking,ContactUs
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Avg, Count
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string,get_template
from pathlib import Path

# For generating pdf invoice
from io import BytesIO
from xhtml2pdf import pisa
import os

# Paytm Check_Sum file







# Home page Backand Coding
def Home(request):
    return render(request,'Home.html')
 
# Reset Password functions
def reset_password(request):
    return render(request , 'user/Reset_Password.html')

#profile page Backand Coding
@login_required(login_url='/') 
def Profile(request):
    context = {}
    data = User.objects.get(id = request.user.id)
    context["data"] = data
    if(request.method == 'POST'):
        Name = request.POST['name']
        Email = request.POST['email']
        Address = request.POST['address']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        user = User.objects.get(id = request.user.id)
        user.Name = Name
        user.email = Email
        user.Address = Address
        user.phone = phone
        user.city = city
        user.state = state
        user.pincode = pincode
        user.save()

        if("profile" in request.FILES):
            img = request.FILES['profile']
            user.profile_pic = img
            user.save()
        messages.info(request,"Changes Saved Successfully")
        return render(request,'profile_page.html',context)
        
    else:
       return render(request,'profile_page.html')

# FeedBack
@login_required(login_url='/') 
def FeedBack(request,food_id):
    user = User.objects.get(id = request.user.id)
    time = timezone.now()
    food = Food.objects.get(id = food_id)
    if(request.method =='POST'):
        comment = request.POST['feedback']
        rating=  request.POST['rating']
        user_feedback = Review(user = user,food = food, content = comment, rate = rating,date_time = time)
        user_feedback.save()
        return redirect('FoodOrder',food_id = food_id)
    else:
        return redirect('FoodOrder',food_id = food_id)


#Registration and Login form 
User = get_user_model()
def Register(request):
    if(request.method == 'POST'):
        Name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        address  = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        
        if(password==confirm_password):
            if(User.objects.filter(email=email).exists()):
                messages.info(request,'Email Taken')
                return render(request,'Login_Registration.html')
            elif(User.objects.filter(phone = phone_number).exists()):
                messages.info(request,'Phone Number Taken')
                return render(request,'Login_Registration.html')
            else:
                user  = User.objects.create_user(Name = Name,email = email,password = password,phone = phone_number,Address = address,city = city,state = state,pincode = pincode)
                user.save()
                messages.add_message(request,messages.SUCCESS,'You have registered successfully')
                return render(request,'Login_Registration.html')
        else:
            messages.info(request,'Password Does Not Match')
            return redirect('Register')
    else:
        return render(request,'Login_Registration.html')


def Login(request):
    if(request.method=='POST'):
        password = request.POST['password']
        email  =  request.POST['email']
        user = auth.authenticate(request, email=email, password=password)
        if(user is not None):
            auth.login(request,user)
            return redirect('/',user= 'user')
        else:
            messages.info(request,'Login Failed! ')
            return render(request,'Login_Registration.html')
    else:
        return render(request,'Login_Registration.html')

def Logout(request):
    auth.logout(request)
    return redirect('/')
    

# Food Menu
@login_required(login_url='Login')
def FoodMenu(request):
    user = User.objects.get(id = request.user.id)
    ord = orders.objects.filter(user = user)
    ord = list(ord)
    qty = 0
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    filter_bar = ""
    food_type   = request.GET.get('ca ')
    if(food_type):
        food = Food.objects.filter(Food_Type = food_type)
    else:
        food = Food.objects.all()
    cate = []
    filter = Food.objects.all()
    for i in filter:
        cate.append(i.Food_Type)
    cate= set(cate)
    if(request.method =='POST'):
        search = request.POST["box"]
        food = Food.objects.filter(Q(Food_Name__icontains=search))
        filter = Food.objects.all()
        cate = []
        for i in filter:
            cate.append(i.Food_Type)
        cate= set(cate)
    return render(request,'Food_menu.html',{'food':food,"cate":cate,"qty":qty,"ord":ord})

# Add To Cart
@login_required(login_url='Login') 
def Cart(request):
    if(request.method=="POST"):
        food = request.POST['food_id']
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(food)
            if(quantity):
                if(remove):
                    if(quantity<=1):
                        cart.pop(food)
                    else:
                        cart[food] = quantity - 1
                else:
                    cart[food] = quantity + 1
            else:
                cart[food] = 1
        else:
            cart = {}
            cart[food] = 1
        request.session['cart'] = cart
    return redirect('FoodMenu')



@login_required(login_url='Login')     
def AddCart(request):
    ids = list(request.session.get('cart'))
    product = Food.objects.filter(id__in = ids)
    user = User.objects.get(id = request.user.id)
    odr = orders.objects.filter(user = user)
    SGST = 5
    CGST  = 5
    penilty = user.penilty
    cart = request.session.get('cart')
    lis = [SGST,CGST,penilty,cart,product]
    if(request.method=='POST'):
        Address = request.POST.get('Address')
        City = request.POST.get('city')
        State = request.POST.get('state')
        Pincode = request.POST.get('pincode')
        payment_method = request.POST.get('paymentmethod')
        if(payment_method=='COD'):
            count = 0
            for p in product:
                discount_amount = discount_calculater(p,cart)
                Amount = final_amount(lis,p)
                qty = cart_count(p,cart)
                ord = orders(user = user,food = p,date_time = timezone.now(),state = State,city = City,order_address = Address,pincode = Pincode,quantity =qty ,deliver_status = False,total_amount =Amount )
                ord.save()
                bill = Bill(order_no = ord,user = user,food = p,payment_status =False,discount = discount_amount,tex = 10,penilty = penilty,total_amount = Amount)
                bill.save()
                count+=1
                success(request,ord.id,bill.id)
            messages.add_message(request,messages.SUCCESS,'Your have ordered successfully!')
            request.session['cart'] = {}
            user.penilty = 0
            user.save()
            
            return redirect('AddCart')
    return  render(request,'cart_product.html',{'product':product,"order":odr, "user":user,'TEX':CGST + SGST,"lis":lis})

#Order Page
@login_required(login_url='Login') 
def FoodOrder(request,food_id):
    discount = False
    food = Food.objects.get(id = food_id)
    new_food_price = food.Food_Price
    user = User.objects.get(id = request.user.id)
    ord = orders.objects.filter(user = user)
    ord = list(ord)
    if(food.Discount_In_Percentage):
        if(food.Discount_In_Percentage>0):
            discount = True
            difference = (food.Food_Price)*((food.Discount_In_Percentage)/(100))
            new_food_price = int(food.Food_Price - difference)

    qty = 1
    if(request.method =='POST'):
        value = request.POST['qty']
        remove = request.POST.get('remove')
        value = int(value)
        if(qty>0):
            if(remove):
                qty = value-1
            else:
                qty = value + 1
        else:
            qty = 1
    rating = Review.objects.filter(food_id = food_id).order_by('-date_time')
    rate = Review.objects.filter(food_id= food_id).aggregate(Avg('rate'))
    num = Review.objects.filter(food_id= food_id).aggregate(Count('user'))
    food.users = num["user__count"]
    food.Food_Avg_Rating = rate["rate__avg"]
    food.save()
    return render(request,'Food_Order.html',{"food":food,"rating":rating,"Discount":discount,"new_food_price":new_food_price,"qty":qty,"ord":ord})



@login_required(login_url='Login') 
def Payment(request,food_id,qty ):
    food = Food.objects.get(id = food_id)
    user = User.objects.get(id = request.user.id)
    discount = False
    difference =0
    penilty = user.penilty
    CGST = 5
    SGST = 5
    new_food_price = food.Food_Price
    # Adding Discount
    if(food.Discount_In_Percentage):
        if(food.Discount_In_Percentage>0):
            discount = True
            difference = (food.Food_Price)*((food.Discount_In_Percentage)/(100))
            new_food_price = (food.Food_Price - difference)
        
    Total_price = round(new_food_price * int(qty),4)
    # Final price
    print(penilty)
    Final_price = round(Total_price + 0 + Total_price*(CGST*0.01) + Total_price*(SGST*0.01),4)
    if(penilty):
        Final_price = round(Total_price + penilty + Total_price*(CGST*0.01) + Total_price*(SGST*0.01),4)
   
    message = ""
    #Order count 
    odr = orders.objects.filter(user = user)
    if request.method == 'POST':
        Address = request.POST.get('Address')
        City = request.POST.get('city')
        State = request.POST.get('state')
        Pincode = request.POST.get('pincode')
        payment_method = request.POST.get('paymentmethod')
        if(payment_method == "COD"):
                ord = orders(user = user,food = food,date_time = timezone.now(),order_address = Address,state = State,city = City,pincode = Pincode,quantity = qty,deliver_status = False,total_amount = Final_price)
                ord.save()
                bill = Bill(order_no =ord,user = user,food  = food,payment_status = False,discount = difference,tex = 10, penilty = penilty,total_amount = Final_price)
                bill.save()
                user.penilty = 0
                user.save()
                messages.add_message(request,messages.SUCCESS,'Your have ordered successfully!')
                success(request,ord.id,bill.id)
        elif(payment_method =="UPI" or payment_method =="CARD"):
            messages.info(request,"This service is not available now")

    return render(request,"Payment.html", {"user":user,"food":food,"Discount":discount,"difference":difference,"new_food_price":new_food_price,"qty":qty,"Total_price":Total_price,"final_price":Final_price,"user":user,'odr':odr,'CGST':CGST,'SGST':SGST})

#MyOrders Page
@login_required(login_url='Login')
def MyOrders(request):
    user = User.objects.get(id = request.user.id)
    order = orders.objects.filter(user_id =user).order_by('-date_time')
    print("orders ",order)
    bills = Bill.objects.filter(user = user)
    lis = [request.session.get('cart')]
    if(request.method == 'POST'):
        if(request.POST.get('cancle')):
                print("start the game")
                oddr = request.POST.get('order_no')
                print("order no ",oddr)
             
                odr = orders.objects.get(id = oddr)
                print("order Name ",odr.food.Food_Name)
                print("oder object ",odr)
                if(user.penilty>0):
                    user.penilty = user.penilty + math.ceil((odr.total_amount)*0.2)
                else:
                    user.penilty = math.ceil((odr.total_amount)*0.1)
                user.save()
                odr.delete()
                messages.add_message(request,messages.SUCCESS,'Your Order has been canceled successfully!')
                return redirect('MyOrders')

        else:
                oddr = request.POST.get('order_no')
                print("order object in no penalty area ", oddr)
                odr = orders.objects.get(id = oddr)
                odr.delete()
                messages.add_message(request,messages.SUCCESS,'Your Order has been canceled successfully!')
                return redirect('MyOrders')
    return render(request,'MyOrders.html',{'user':user,'orders':order,"bills":bills})

# Sending Conformation email
@login_required(login_url='Login')
def success(request,pk,pk1):
    print("Initial start ")
    lis = getpdf(request,pk,pk1)
    print("starting phase 4")
    bill_no = str(lis[1]['order_id'])
    filename = 'Invoice_' + bill_no + '.pdf'
    print("Entering file name")
    user = User.objects.get(id = request.user.id)
    print('user object')
    template = render_to_string('email_templates.html',{'user':user})
    email  = EmailMultiAlternatives(
        'Thanks for ordering the food',
        template,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    print("progress")
    email.attach(filename,lis[0],'application/pdf')
    print("attached pdf file in email")
    email.fail_silently = False
    print('hurrye we have done it thank you so mutch!!!!!')
    email.send()

# Handeling Time  and penilties
many_table_ids = []
def HandleBooking(capicity,members):
    members = int(members)
    Max = 0
    for i in range(1,capicity+1):
            table_id = Table.objects.get(id = i)
            if(table_id.capicity==members):
                return i
            elif(members<table_id.capicity):
                return i
            else:
                Max = table_id.capicity
    if(members>Max):
        for j in range(1,capicity+1):
            for i in range(j+1,capicity+1):
                table_id = Table.objects.get(id = i)
                table_id_1 = Table.objects.get(id = j)   
                if(members<=table_id.capicity + table_id_1.capicity):
                        many_table_ids.append(i)
                        many_table_ids.append(j)
                        return None
    return 0
                
            
@login_required(login_url='Login')        
def MyBooking(request):
    user = User.objects.get(id = request.user.id)
    book = Booking.objects.filter(user =user).order_by('-date_time')
    print(book)
    if(request.method == 'POST'):
                bok = request.POST.get('booking_no')
                bk = Booking.objects.get(id = bok)
                bk.delete()
                messages.add_message(request,messages.SUCCESS,'Your Booking has been canceled successfully!')
    return render(request,'MyBooking.html',{'user':user,'bookings':book})
   

# Contact page
@login_required(login_url='Login')
def Contact(request):
    user = User.objects.get(id = request.user.id)
    if(request.method == 'POST'):
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        Message = request.POST.get('Message')
        print(email)
        print(name)
        ct = ContactUs(Name = name, Email = email, message = Message)
        ct.save()
        messages.info(request,'We will be in touch with you soon')
    return render(request,'Contact.html',{'user':user})



def About(request):
    return render(request,'About.html')

# Boking Table
@login_required(login_url='Login')
def BookTable(request):
    lis = list(Table.objects.all())
    length = len(lis)
    user = User.objects.get(id = request.user.id)
    bookings = Booking.objects.filter(user = user)
    if(request.method=='POST'):
        Date = request.POST.get("Date")
        Time = request.POST.get("Time")
        Members = request.POST.get("members")
        table_id = HandleBooking(length,Members)
        date_time = Date + " " + Time
        date_object = datetime.strptime(date_time,"%Y-%m-%d %H:%M")
        current_time = timezone.now()
        open_time = Date + " " + "11:00"
        close_time = Date + " " + "20:00"
        future_time_object_one = datetime.strptime(open_time,"%Y-%m-%d %H:%M")
        future_time_object_two = datetime.strptime(close_time,"%Y-%m-%d %H:%M")
        date= current_time +  timezone.timedelta(days=7)
        if(current_time>date_object):
            messages.info(request,"Invlid Input")
            return redirect('BookTable')
        elif(date_object>date):
            messages.info(request,"Sorry! you book for only 7 days in advance.")
            return redirect('BookTable')
        elif(future_time_object_one>date_object or date_object>future_time_object_two):
            messages.info(request,"Restaurant is not open at this time")
            return redirect('BookTable')
        if(table_id):
            table = Table.objects.get(id = table_id)
        elif(table_id == 0):
            messages.info(request,"Table is not available")
            return redirect('BookTable')
        else:
            for tbl in many_table_ids:
                table = Table.objects.get(id =tbl)
                Boking = Booking(user = user,table = table,capicity = Members,date_time = date_object,Booking_time = current_time)
                Boking.save()
            success_booking(request)
            many_table_ids.clear()
            messages.info(request,"Your booking was successful \n  For more details you can go to My Bookings")
            print("I am in here in else of tbl")
            return redirect('BookTable')
        Boking = Booking(user = user,table = table,capicity = Members,date_time = date_object,Booking_time = current_time)
        Boking.save()
        success_booking(request)
        messages.info(request,"Your booking was successful  \n  For more details you can go to My Bookings")
    return render(request,'Book_Table.html',{"bookings":bookings})


def success_booking(request):
    user = User.objects.get(id = request.user.id)
    template = render_to_string('email_templates_for_booking.html',{'user':user})
    email  = EmailMessage(
        'Thanks for booking the table',
        template,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.fail_silently = False
    email.send()


# Generate Invoice

def render_to_pdf(template_src, context_dict={}):
    print("inside the phase 3")
    template = get_template(template_src)
    print("rendering template")
    html  = template.render(context_dict)
    print("transfaring the data in template")
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    print("converting template to pdf")
    if not pdf.err:
        return result.getvalue()
    return None
def getpdf(request, pk,pk1, *args, **kwargs):
        user = User.objects.get(id = request.user.id)
        print("start")
        bill_db = Bill.objects.get(id = pk1)
        order_id = orders.objects.get(id = pk) 
        print("complete phase 1")
        data = {
            'order_id': bill_db,
            'quantity': order_id.quantity,
            'user': user,
            'date':order_id.date_time,
            'user_email': bill_db.user.email,
            'name': bill_db.user.Name,
            'Bill no.': bill_db,
            'Discount':bill_db.discount,
            'Penalty':bill_db.penilty,
            'amount': bill_db.total_amount,
        }
        print("completed phase 2")
        pdf = render_to_pdf('invoice.html', data)
        print("completed phase 3")
        return [pdf,data,]
