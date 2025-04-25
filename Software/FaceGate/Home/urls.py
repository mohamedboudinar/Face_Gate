from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name="home"),
    path('contact_us/',views.contact,name='contact us'),
    path('about_us/',views.about,name='about us'),
    path('contact_us/contact_form/',views.contactform,name='contact form'),
    path('contact_us/sendform/',views.sendform,name='send form')
    ]