from django.db import models
from datetime import datetime
from .fchecker import FileExtensionValidator

TRAIN_STATUS = (
    ('TRAIN', "Training"),
    ('TRAINED', "Trained"),
    ('PLACED', "Placed"),
)

BRANCH_CHOICES = (
    ('CSE', "CSE"),
    ('ECE', "ECE"),
)

YEAR_CHOICES = (
    [(i, i) for i in range(1984, datetime.now().year)]
)

TYPE_CHOICES = (
    ('TECH', "Techanical"),
    ('NOTECH', "Non-Techanical"),
    ('TEL', "Telecom"),
    ('MFN', "Manufacturing"),
    ('RTL', "Retail"),
    ('STP', "StartUp"),
)

GRAD_YEAR = (
    [(datetime.now().year+i, datetime.now().year+i) for i in range(5)]
)

COURSE_CHOICES = (
    ('BTECH', "B.Tech"),
    ('MTECH', "M.Tech"),
)


ELIGIBLITY_CHOICES = (
    ('BTECHGRAD', "B.Tech Graduate"),
    ('MTECHGRAD', "M.Tech Graduate"),
    ('BOTH', "Both"),
)

class Student(models.Model):
    Email = models.EmailField(unique=True)
    Roll = models.SmallIntegerField(unique=True)
    Name = models.CharField(max_length=100)
    Status = models.CharField(max_length=7, choices=TRAIN_STATUS)
    Mobile = models.CharField(max_length=13)
    Graduation_Year = models.IntegerField(choices=GRAD_YEAR)
    Course = models.CharField(max_length=10, choices=COURSE_CHOICES, blank=True)
    Branch = models.CharField(max_length=3, choices=BRANCH_CHOICES)
    Resume = models.FileField(upload_to='media/resume',validators=[FileExtensionValidator(allowed_extensions=['pdf'], max_file_size=2621440) ])
    Is_Created = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.Name
    


class Company(models.Model):
    Name = models.CharField(max_length=50)
    Year = models.IntegerField(choices=YEAR_CHOICES)
    Website = models.CharField(max_length=50)
    Type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    Email = models.EmailField()
    Mobile = models.CharField(max_length=13)
    Postal_Code = models.IntegerField()
    Address = models.TextField(max_length=250)    
    Is_Created = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Name


class Offer(models.Model):
    Title = models.CharField(max_length = 50, blank=False)
    Branch = models.CharField(max_length=3, choices=BRANCH_CHOICES, blank=False, default='CSE')
    Eligiblity = models.CharField(max_length=15, choices=ELIGIBLITY_CHOICES)
    Salary = models.CharField(max_length=14, help_text='in LPA', blank=False)
    Responsiblities = models.TextField(max_length=100)
    Benefits = models.TextField(max_length=100)
    Starting_date = models.DateField(blank=False)
    Location = models.TextField(max_length=50)
    Experience = models.TextField(help_text='Enter any special requirments such as year of experience, etc')
    company = models.ForeignKey(Company, null=True,blank=True,on_delete=models.CASCADE)
    link = models.CharField(max_length=50, blank=True, null=True, help_text='Enter online link to apply for job if any...')
    
    def __str__(self):
        return self.Title