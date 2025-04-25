from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import departement,Employee,sickNotes,Vacation
from .forms import addDep,addEmp,requestSick,requestVacation
from FaceGate.utils import is_ajax
from django.core.files.base import ContentFile
from profiles.models import Profile
import base64
from django.http import JsonResponse
import socket
import os
# Create your views here.

def HomePage(request):
    return render(request,"home.html")

@login_required(login_url='login')
def HomeAdmin(request):
    if request.user.is_superuser:
        emp=Employee.objects.all()
        return render(request,"home_admin.html",{"emps":emp})
    else:
        return render(request,"403.html")

def authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('home-admin')
            else:
                return redirect('consultation')
        else:
            messages.error(request, 'Invalid employee number or password.')
    return render(request,"login.html") 

def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def services(request):
    if request.user.is_superuser==False:
        return render(request,"services.html")
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def consultation(request):
    if request.user.is_superuser==False:
        us=request.user.username
        emp=Employee.objects.get(empnum=us)
        if emp.isnew==True:
            return render(request,"facial_recognition.html")
        else:
                return render(request,"consultation.html")      
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def DepartementList(request):
    if request.user.is_superuser:
        dep=departement.objects.all()
        return render(request,'departements-list.html',{"deps":dep})
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def AddEmployee(request):
    if request.user.is_superuser:
        if request.method=='POST':
            form=addEmp(request.POST)
            if form.is_valid():
                d=form.cleaned_data['dep']
                dep=departement.objects.get(name=d)
                en=form.cleaned_data['empnum']
                fn=form.cleaned_data['fname']
                ln=form.cleaned_data['lname']
                ad=form.cleaned_data['adress']
                em=form.cleaned_data['email']
                pw=form.cleaned_data['password']

                u=User.objects.create_user(email=em,username=en,password=pw,first_name=fn,last_name=ln,is_staff=True)
                u.save()
                e=Employee(dep=dep,empnum=en,fname=fn,lname=ln,adress=ad,email=em,password=pw)
                e.save()
                messages.info(request,"New Employee has been added successfully!")
                return redirect('Add Employee')
        else:
            form=addEmp()
        return render(request,'add-employee.html',{"form":form})
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def AddDepartement(response):
    if response.user.is_superuser:
        if response.method=='POST':
            form=addDep(response.POST)
            if form.is_valid():
                form.save()
                messages.info(response,'Your new Departement is successfully added')
                return redirect('Add Departement')
        else:
            form=addDep()
        return render(response,'add-departement.html',{"form":form})
    else:
        return render(response,"403.html")

@login_required(login_url='login')
def face_id(request):
    if request.user.is_superuser==False:
        us=request.user.username
        emp=Employee.objects.get(empnum=us)
        
        if emp.isnew==True:
            return render(request,"facial_recognition.html")
        else:
            return render(request,"403.html")
    else:
            return render(request,"403.html")

@login_required(login_url='login')
def sick(request):
    if request.user.is_superuser==False:
        if request.method=='POST':
            form=requestSick(request.POST,request.FILES)
            if form.is_valid():
                em=Employee.objects.get(empnum=request.user.username)
                sd=form.cleaned_data['startdate']
                ed=form.cleaned_data['startdate']
                pr=form.cleaned_data['proof']
                s=sickNotes(emp=em,startdate=sd,enddate=ed,proof=pr)
                s.save()
                messages.info(request,"Your Request has been sent successfully!")
                return redirect('Upload sick note')
            else:
                messages.error(request,"Something is wrong with the dates you entered")
        else:
            form=requestSick()
        return render(request,"uploadsicknote.html",{"form":form,"user":request.user})
    else:
            return render(request,"403.html")

@login_required(login_url='login')
def vacation(request):
    if request.user.is_superuser==False:
        if request.method=='POST':
            form=requestVacation(request.POST)
            if form.is_valid():
                sd=form.cleaned_data['startdate']
                ed=form.cleaned_data['enddate']
                em=Employee.objects.get(empnum=request.user.username)
                v=Vacation(emp=em,startdate=sd,enddate=ed)
                v.save()
                messages.info(request,"Your Request has been sent successfully!")
                return redirect('vacation request')
            else:
                messages.error(request,"Something is wrong with the dates you entered")
        else:
            form=requestVacation()
        return render(request,"requestvacation.html",{"form":form,"user":request.user})
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def DeleteEmp(request,id):
    if request.user.is_superuser: 
        emp=Employee.objects.get(id=id)
        emp.delete()
        us=User.objects.get(username=emp.empnum)
        us.delete()
        messages.info(request,"The selected Employee has been deleted successfully")
        return redirect('home-admin')
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def ModifyEmp(request,id):
    if request.user.is_superuser: 
        e=Employee.objects.get(id=id)
        form=addEmp(request.POST or None, instance=e)
        if form.is_valid():
            form.save()
            messages.info(request,"Employee is updated successfully!")
        return render(request,"modify-Employee.html",{"form":form})
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def DeleteDep(request,id):
    if request.user.is_superuser:   
        dep=departement.objects.get(id=id)
        dep.delete()
        messages.info(request,"The selected Departement has been deleted successfully")
        return redirect('departement list')
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def ModifyDep(request,id):
    if request.user.is_superuser: 
        d=departement.objects.get(id=id)
        form=addDep(request.POST or None, instance=d)
        if form.is_valid():
            form.save()
            messages.info(request,"Departement is updated successfully!")
        return render(request,"modify-departement.html",{"form":form})
    else:
        return render(request,"403.html")

@login_required(login_url='login')
def saveFaceId(request):
    if is_ajax(request):
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')

        decoded_file = base64.b64decode(str_img)

        x = Profile()
        x.user=request.user
        x.photo.save('upload.png', ContentFile(decoded_file))
        x.save()
        us=request.user.username
        emp=Employee.objects.get(empnum=us)
        emp.isnew=False
        emp.save()
        client=ImageClient()
    return redirect('consultation')



class ImageClient:
    def __init__(self, server_ip='127.0.0.1', server_port=4899, images_dir='C:/Users/Mohamed Boudinar/Downloads/Vorlesungen/Vierte Semester/Fachübergreifendesprojekt/07-facegate/Software/FaceGate/media/photos/'):
        self.server_ip = server_ip
        self.server_port = server_port
        self.images_dir = images_dir
        self.socket = None

    def __str__(self):
        """Return a string representation of the instance."""
        return f"ImageClient(server_ip={self.server_ip}, server_port={self.server_port}, images_dir={self.images_dir})"

    def __repr__(self):
        """Return an unambiguous string representation of the instance."""
        return f"ImageClient(server_ip={self.server_ip!r}, server_port={self.server_port!r}, images_dir={self.images_dir!r})"

    def __enter__(self):
        """Initialize and return the instance for use in a with statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the socket when exiting the with statement."""
        self.close_socket()

    def __del__(self):
        """Destructor to ensure the socket is closed when the instance is deleted."""
        self.close_socket()

    def __eq__(self, other):
        """Check if two instances are equal."""
        if isinstance(other, ImageClient):
            return (self.server_ip == other.server_ip and
                    self.server_port == other.server_port and
                    self.images_dir == other.images_dir)
        return False

    def __ne__(self, other):
        """Check if two instances are not equal."""
        return not self.__eq__(other)

    def __hash__(self):
        """Return a hash value of the instance."""
        return hash((self.server_ip, self.server_port, self.images_dir))

    def __call__(self, name):
        """Send all images for a given person."""
        self.send_images(name)

    def close_socket(self):
        """Close the socket if it's open."""
        if self.socket:
            self.socket.close()
            self.socket = None

    def send_image(self, name, image_path):
        """Send a single image to the server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_ip, self.server_port))
            self.socket = s  # Set the socket as the instance attribute

            # Send the name of the person
            name_bytes = name.encode('utf-8')
            name_length = len(name_bytes)
            s.sendall(str(name_length).zfill(4).encode('utf-8'))
            s.sendall(name_bytes)

            # Send the image name
            image_name = os.path.basename(image_path)
            image_name_bytes = image_name.encode('utf-8')
            image_name_length = len(image_name_bytes)
            s.sendall(str(image_name_length).zfill(4).encode('utf-8'))
            s.sendall(image_name_bytes)

            # Send the image data
            with open(image_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    s.sendall(chunk)

    def send_images(self, name):
        """Send all images in the specified directory."""
        image_files = [f for f in os.listdir(self.images_dir) if f.endswith('.jpg')]
        for image_file in image_files:
            image_path = os.path.join(self.images_dir, image_file)
            self.send_image(name, image_path)

# Usage example
if __name__ == '__main__':
    with ImageClient() as client:
        print(client)
        client('ras_zebi') 