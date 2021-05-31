from django import template
from django.utils import timezone
import math
register = template.Library()



# For Discount 
@register.filter(name="is_discount")
def is_discount(product):
    if(product.Discount_In_Percentage):
            if(product.Discount_In_Percentage>0):
                return True
            return False

@register.filter(name = "discount_calculater")
def discount_calculater(product,cart):
    difference = (product.Food_Price)*((product.Discount_In_Percentage)/(100))
    return (product.Food_Price - difference)

# Penilty functions
@register.filter(name="is_penilty")
def it_penilty(product):
        if(product):
            product = int(product)
            product = math.ceil(product)
            if(product>0):
                return True
            return False
        return False

# Cart filters

@register.filter(name="is_in_cart")
def is_in_cart(product,cart):
    keys= cart.keys()
    for id in keys:
        if(int(id)==product.id):
            return True
    return False


@register.filter(name="cart_count")
def cart_count(product,cart):
    keys= cart.keys()
    for id in keys:
        if(int(id)==product.id):
            return cart.get(id)
    return 0

@register.filter(name="price_total")
def price_total(product,cart):
    food_price = product.Food_Price
    if(is_discount(product)):
        food_price = discount_calculater(product,cart)
    return food_price* cart_count(product,cart) 

@register.filter(name="Total_Price")
def Total_Price(lis,product):
    sum = 0
    for p in product:
        sum+=final_amount(lis,p)
    return round(sum,4)

@register.filter(name="final_amount")
def final_amount(lis,food_items):
    amount = price_total(food_items,lis[3])
    if(lis[4][len(lis[4])-1].id==food_items.id):
        amount = price_total(food_items,lis[3])
        if(lis[2]):   
            return round(amount + lis[2] + amount*(lis[0]*0.01) + amount*(lis[1]*0.01),4)
    return round(amount + amount*(lis[0]*0.01) + amount*(lis[1]*0.01),4)

@register.filter(name="first_count")
def first_count(lis,food_items):
    if(lis[4][len(lis[4])-1].id==food_items.id):
       return False
    return True
    
# Is Equal
@register.filter(name="is_equal")
def is_equal(msg):
    if("Successfully Booked" == msg):
        return True
    else:
        return False

@register.filter(name="is_empty")
def is_empty(product,cart):
    if(cart=={}):
        return False
    return True
# Penilty 
@register.filter(name="is_it_penilty")
def is_it_penilty(order):
    current_time = timezone.now()
    time = current_time - order.date_time
    time = time.total_seconds()
    if(time<300):
        return False
    return True


# For Booking Table
@register.filter(name="calculate_lenth_of_bookings")
def calculate_lenth_of_bookings(Bookings):
    return len(list(Bookings))
