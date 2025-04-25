from django import forms
from .models import departement,Employee
import datetime



class addDep(forms.ModelForm):
    class Meta:
        model=departement
        fields=('location','name','adress')

class addEmp(forms.ModelForm):
    class Meta:
        model=Employee
        fields=('dep','empnum','fname','lname','adress','email','password')

    

class requestVacation(forms.Form):
    startdate=forms.DateField(required=True)
    enddate=forms.DateField(required=True)
    
    def clean(self):
        startdate=self.cleaned_data['startdate']
        enddate=self.cleaned_data['enddate']
        if startdate < datetime.date.today():
            raise forms.ValidationError("The start date can't be earlier than today's date ")
        elif startdate > enddate:
         raise forms.ValidationError("End date must be later than start date")   
        return super(requestVacation, self).clean()


class requestSick(forms.Form):
    startdate=forms.DateField(required=True)
    enddate=forms.DateField(required=True)
    proof=forms.ImageField(required=True)

    def clean(self):
        startdate=self.cleaned_data['startdate']
        enddate=self.cleaned_data['enddate']
        if startdate < datetime.date.today():
            raise forms.ValidationError("The start date can't be earlier than today's date ")
        elif startdate > enddate:
         raise forms.ValidationError("End date must be later than start date")   
        return super(requestSick, self).clean()