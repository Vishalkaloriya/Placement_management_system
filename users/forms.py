from django import forms
from .models import Student, Company, Offer

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['Email', 'Roll', 'Name', 'Mobile', 'Graduation_Year', 'Course', 'Branch', 'Resume']
        
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['Name', 'Year', 'Website', 'Type', 'Email', 'Mobile', 'Postal_Code', 'Address']
        
class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['Mobile', 'Graduation_Year', 'Branch', 'Resume']
        

class OfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Starting_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd ',
                'class': 'form-control'
                }
            )
    class Meta:
        model = Offer
        fields = ['Title', 'Eligiblity', 'Salary', 'Responsiblities','Benefits','Starting_date','Location','Experience', 'link']