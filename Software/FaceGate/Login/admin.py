from django.contrib import admin
from .models import locations,departement,Employee,Vacation,sickNotes
# Register your models here.

admin.site.register(locations)
admin.site.register(departement)
admin.site.register(Employee)
admin.site.register(Vacation)
admin.site.register(sickNotes)