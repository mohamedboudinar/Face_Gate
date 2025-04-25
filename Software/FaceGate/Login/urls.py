from . import views
from django.urls import path


urlpatterns = [
    path('',views.HomePage,name="home"),
    path('home-admin/',views.HomeAdmin,name='home-admin'),
    path('home-admin/modify/<int:id>',views.ModifyEmp,name='modify Employee'),
    path('home-admin/delete/<int:id>',views.DeleteEmp,name='delete Employee'),
    path('departement/',views.DepartementList,name='departement list'),
    path('departement/modify/<int:id>',views.ModifyDep,name='modify Departement'),
    path('departement/delete/<int:id>',views.DeleteDep,name='delete Departement'),
    path('add-employee/',views.AddEmployee,name='Add Employee'),
    path('add-departement/',views.AddDepartement,name='Add Departement'),
    path('employee/', views.authentication, name="login"),
    path('services/',views.services,name='services'),
    path('consultation/',views.consultation,name='consultation'),
    path('logout/',views.LogoutPage,name="logout"),
    path('services/face_id/',views.face_id,name='face id'),
    path('services/sicknote/',views.sick,name='Upload sick note'),
    path('services/vacation_request/',views.vacation,name='vacation request'),
    path('savepic/',views.saveFaceId,name='save Face ID')
    ]