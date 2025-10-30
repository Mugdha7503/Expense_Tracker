from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),



    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('forgotpassword/',views.forgotpassword, name='forgotpassword'),
    # path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name='resetpassword_validate'),
    # path('resetpassword/',views.resetpassword, name='resetpassword'),

    


]


