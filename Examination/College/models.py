from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class Students(models.Model):
    StudID=models.CharField(unique=True,max_length=20)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed. please specify country code with a '+' ")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
    email=models.EmailField()
    Name=models.CharField(max_length=100)
    rollno=models.PositiveIntegerField()   

    
class Marks(models.Model):
    student=models.ManyToManyField(Students)
    mark=models.PositiveIntegerField()
    grade=models.CharField(max_length=2)
class course(models.Model):
    course_id=models.CharField(max_length=10,unique=True)
    Name=models.CharField(max_length=100)
    Marks_Obtained=models.ManyToManyField(Marks)
class batch(models.Model):
    batch_id=models.CharField(max_length=10,unique=True)
    name=models.CharField(max_length=100)
    dept_name=models.CharField(max_length=100)
    courses=models.ManyToManyField(course)
    studs=models.ManyToManyField(Students)
class dept(models.Model):
    dept_id=models.CharField(max_length=10,unique=True)
    name=models.CharField(max_length=10)
    batches=models.ManyToManyField(batch)
class examination(models.Model):
    marks=models.ManyToManyField(Marks)
    course=models.OneToOneField(course, on_delete=models.CASCADE)

    