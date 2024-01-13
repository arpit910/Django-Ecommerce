from django.urls import path
from website import views
from website.authviews import*
from django.contrib.auth import views as auth_views

authFunctionsList = [
    path('signup',user_signup),
    path('signin',user_login,name='signin'),
    path('signout',user_logout),
    path('changepass',change_password, name='change_password'),
    path('changeprof',change_profile, name='change_profile'),
    path('activate/<uidb64>[0-9A-Za-z_\-]+/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}',user_activation, name='activate'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='auth/password_reset/form.html'),name='password_reset_complete')
]

urlpatterns = [
    path('',views.home),
    path('gallery/',views.gallery),
    path('shop/',views.product),
    path('cctv/',views.product),
    path('about/',views.about),
    path('profile/',views.profile),
    path('showproduct/<str:name>',views.showproduct),
    path('addtowishlist/<str:parent>/<int:id>',views.add2wl),
    
]+authFunctionsList
