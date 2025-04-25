from django.db import models

class locations(models.Model):
    city=models.CharField(max_length=50)

    def __str__(self):
        return self.city


class departement(models.Model):
    location=models.ForeignKey(locations,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    adress=models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Employee(models.Model):
    dep=models.ForeignKey(departement,on_delete=models.CASCADE)
    empnum=models.CharField(max_length=50)    
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    adress=models.CharField(max_length=100)
    email=models.EmailField(max_length=200)
    password=models.CharField(max_length=100)
    isnew=models.BooleanField(default=True)

    def __str__(self):
        return self.empnum
    
class Vacation(models.Model):
    emp=models.ForeignKey(Employee,on_delete=models.CASCADE)
    startdate=models.DateField()
    enddate=models.DateField()

    def __str__(self):
        return f"Vacation Request of {self.emp.empnum}"


class sickNotes(models.Model):
    emp=models.ForeignKey(Employee,on_delete=models.CASCADE)
    startdate=models.DateField()
    enddate=models.DateField()
    proof=models.ImageField()

    def __str__(self):
        return f"Rest days Request of {self.emp.empnum}"