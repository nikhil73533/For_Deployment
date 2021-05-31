from django.urls import path,include
from . import views 
from  django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
urlpatterns = [
    path('',views.Home,name = "Home"),
    path('register',views.Register,name = "Register"),
    path('login',views.Login,name = "Login"),
    path('logout',views.Logout,name = "Logout"),
    path('profile',views.Profile,name = "Profile"),
    path('menu',views.FoodMenu,name = "FoodMenu"),
    path('cart', views.Cart,name = "Cart"),
    path('feedback/<int:food_id>/', views.FeedBack,name = "FeedBack"),
    path('food_order/<int:food_id>/', views.FoodOrder,name = "FoodOrder"),
    path('payment/<int:food_id>/<int:qty>/', views.Payment,name = "Payment"),
    path('add_cart', views.AddCart,name = "AddCart"),
    path('my_orders', views.MyOrders,name = "MyOrders"),
    path('contact_us', views.Contact,name = "Contact"),
    path('bood_table', views.BookTable,name = "BookTable"),
    path('MyBooking', views.MyBooking,name = "MyBooking"),
    path('about', views.About,name = "About"),
     #Password Reset Urls

    path('reset_password/',PasswordResetView.as_view(template_name = "user/Password_email.html"),name = 'reset_password'),
    path('reset_password_sent/',PasswordResetDoneView.as_view(template_name = "user/Password_Reset_done.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name = "user/Password_Reset_confirm.html"), name = "password_reset_confirm"),
    path('reset_password_complete/',PasswordResetCompleteView.as_view(template_name = "user/Password_reset_submit.html"), name = "password_reset_complete"),

] 
