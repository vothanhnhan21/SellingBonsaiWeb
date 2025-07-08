from django.urls import path
from . import views
from .forms import UserPasswordResetForm,CustomSetPasswordForm
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index,name = 'home'),
    path('login/',views.login_view,name = 'login'),
    path('logout/',views.logout_view,name = 'logout'),
    path('register/',views.register_view,name = 'register'),
    path('introduction',views.introduction, name = 'introduction'),
    path('news/',views.news, name = 'news'),
    path('connection/',views.connection, name = 'connection'),
    path('policy/',views.policy, name = 'policy'),
    path('cart/',views.cart_view, name = 'cart'),
    path('cart_mini_update/',views.cart_mini_update, name = 'cart_mini_update'),
    path('add/', views.add, name='add'),
    path('update-cart-item/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path('delete_cart_item/',views.delete_cart_item, name='delete_cart_item'),
    path('delete_all/',views.delete_all, name='delete_all'),
    path('payment/',views.payment, name='payment'),
    path('payment_list/',views.payment_list, name='payment_list'),
    path('payment_page/',views.payment_page, name='payment_page'),
    path('payment_submit/',views.payment_submit, name='payment_submit'),
    path('careCTS/',views.careCTS, name = 'careCTS'),
    path('careCVP/',views.careCVP, name = 'careCVP'),
    path('careSD/',views.careSD, name = 'careSD'),
    path('CCT/',views.CCT, name = 'CCT'),
    path('CDB/',views.CDB, name = 'CDB'),
    path('CNN/',views.CNN, name = 'CNN'),
    path('CPT/',views.CPT, name = 'CPT'),
    path('CSD/',views.CSD, name = 'CSD'),
    path('CTN/',views.CTN, name = 'CTN'),
    path('CTS/',views.CTS, name = 'CTS'),
    path('findPage/',views.find_page, name = 'findPage'),
    path('change_password/',views.change_password, name = 'change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name='registration/password_reset.html',
    form_class=UserPasswordResetForm,
    email_template_name = 'registration/password_reset_email.txt'),name='password_reset'),

    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = "registration/set-password.html",form_class=CustomSetPasswordForm), name ='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'registration/password_complete.html'), name ='password_reset_complete'),
]
