from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.register_attemp,name='register'),
    path('login/',views.login_attemp,name='login'),
    path('token/',views.token_send,name='token_send'),
    path('success/',views.success,name='success'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('error/',views.error_page,name='error'),
    
    
]