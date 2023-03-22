from django import forms 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
# from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime,timedelta, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from twilio.rest import Client
import os
from django.core.validators import MinLengthValidator


# Create your models here.
class MyAccount(BaseUserManager):
    def create_user(self, first_name, last_name, email,contact,regno,dpmnt,sem, password=None):
        if not email:
            raise ValueError('User must have an email address')

    

        user = self.model(
            email = self.normalize_email(email),
            # username = username,
            first_name = first_name,
            last_name = last_name,
            contact = contact,
            regno=regno,
            dpmnt=dpmnt,
            sem=sem,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self,password,email,**extra_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            # username = username,
            **extra_fields,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser,PermissionsMixin):
    id              = models.AutoField(primary_key=True)
    first_name      = models.CharField(max_length=50, default='')
    last_name       = models.CharField(max_length=50, default='')
    email           = models.EmailField(max_length=100, unique=True)
    contact         = models.BigIntegerField(default=0)
    address         = models.CharField(max_length=50, default='')
    pin             = models.BigIntegerField(default=0)
    regno           = models.BigIntegerField(default=0 , unique=True)
    dpmnt           = models.CharField(max_length=50, default='')
    sem             = models.CharField(max_length=50, default='')
    img             = models.ImageField(upload_to='pics', default=0)
    gender_choices = [('N','None'),('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default='N',null=True)
    room = models.OneToOneField(
        'Room',
        blank=True,
        on_delete= models.SET_NULL,
        null=True)
    room_allotted = models.BooleanField(default=False)
    no_dues = models.BooleanField(default=True)

    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_user         = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_libry        = models.BooleanField(default=False)
    is_warden       = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','contact','regno','dpmnt','sem']
    # REQUIRED_FIELDS = ['password']




    objects = MyAccount()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    


class LastFace(models.Model):
    last_face = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.last_face



######################################Library########################################

class librarian(models.Model):
    libid           = models.AutoField(primary_key=True)
    First_name      = models.CharField(max_length=50, default='')
    Last_name       = models.CharField(max_length=50, default='')
    email           = models.EmailField(max_length=100, unique=True)
    Phone_number    = models.BigIntegerField(default=0)
    is_libr         = models.BooleanField(default=True)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)



class Category_Book(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.category_name)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100)
    book_category = models.ForeignKey(Category_Book, verbose_name="Category_Book", on_delete=models.PROTECT)
    book_quantity = models.BigIntegerField(default=0)
    book_price = models.BigIntegerField(default=0)
    book_author = models.CharField(max_length=50)
    book_year = models.BigIntegerField(default=0)
    book_language = models.CharField(max_length=50)
    book_publisher = models.CharField(max_length=100)
    book_status = models.BooleanField(default=True)
    book_desc = models.TextField()
    isbn = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics', default=0)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)



class Files(models.Model):
    filename = models.CharField(max_length=100)
    descrip = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='media')
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)

        


def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    enrollment=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return self.enrollment


##############################Hostel####################################################


class Leave(models.Model):
    sem_choices=(('First','First'),('Second','Second'),('Third','Third'),('Fourth','Fourth'),('Fifth','Fifth'),('Sixth','Sixth'),('Seventh','Seventh'),('Eighth','Eighth'),('None','None'))
    status_choices=(('Approved','Approved'),('Pending','Pending'),('None','None'))
    id  =  models.AutoField(primary_key=True)
    name  = models.CharField(max_length=100)
    dept  =  models.CharField(max_length=100)
    mobno = models.BigIntegerField(default=0)
    sem   =  models.CharField(max_length=100, choices=sem_choices)
    ldate =  models.DateTimeField(auto_now_add=False)
    idate =  models.DateTimeField(auto_now_add=False)
    purpose= models.CharField(max_length=100)
    dest  = models.CharField(max_length=100)
    status= models.IntegerField(default=0)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    parents_email  = models.EmailField(max_length=100, default=0)
    parents_contact  = models.BigIntegerField(default=0)


    def __str__(self):
        return self.name
    
    def __str__(self):
        return self.parents_contact
    
    def __str__(self):
        return self.purpose

    def save(self, *args, **kwargs):
        if self.status == 1:
            account_sid = 'AC7e1b12f105b868c334e9923e237a3e2a'
            auth_token = '080cc05e21e9313086823c94f15094a7'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                     body="Heloo ",
                     from_='+13215946647',
                     to={self.parents_contact}
            )
        else:
            account_sid = 'AC7e1b12f105b868c334e9923e237a3e2a'
            auth_token = '080cc05e21e9313086823c94f15094a7'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f"Dear Parent,{self.name}, applying Outpass for {self.purpose}",
                from_='+13215946647',
                to={self.parents_contact}
            )

        print(message.sid)
        return super().save(*args, **kwargs)



class addmessfee(models.Model):
    id  =  models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    feestatus=models.BooleanField(default=False)
    amount = models.FloatField(blank=True,null=True)
    date_paid = models.DateField(auto_now=True)


  

class ComplaintStudent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    complaint = models.TextField(max_length=500)
    complaint_reply = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

#############################################################


class Course(models.Model):
    # if a student has enrollment number iit2017001 then the course code is iit2017
    code = models.CharField(max_length=100, default=None)
    room_choice = [('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('P', 'Reserved for Research Scholars'), ('B', 'Both Single and Double Occupancy')]
    room_type = models.CharField(choices=room_choice, max_length=1, default='D')

    def __str__(self):
        return self.code
    

class Hostel(models.Model):
    name = models.CharField(max_length=5)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    course = models.ManyToManyField('Course', default=None, blank=True)
    caretaker = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_choice = [('S', 'Single Room'), ('D', 'Double Room'), ('T', 'Triple Room'),('P', 'Reserved for Research Scholars'),('B', 'Both Single and Double Occupancy')]
    room_type = models.CharField(choices=room_choice, max_length=1, default=None)
    room_image = models.ImageField(upload_to='room_image/',default='')
    price          = models.IntegerField(default=0)
    available          = models.IntegerField(default=0)
    description    = models.TextField(max_length=1000,default='')

    

    def delete(self, *args, **kwargs):
        stud = Account.objects.filter(room=self)
        print('pppppppppppppppppppppppppppppppppppppppp')
        for s in stud:
            s.room_allotted = False
            s.save()
            print('***********')
        super(Room, self).delete(*args, **kwargs)


