from django.contrib import admin
from .models import Student, Company, Offer

admin.site.register(Company)
admin.site.register(Student)
admin.site.register(Offer)
