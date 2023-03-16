from django import forms
from django.contrib.auth.models import User
from .models import *
import datetime

YEARS= [x for x in range(2023,2024)]
# class BookForm(forms.ModelForm):
#     class Meta:
#         model=models.Book
#         fields=['name','isbn','author','category']
# class IssuedBookForm(forms.Form):
#     #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
#     isbn2=forms.ModelChoiceField(queryset=models.Book.objects.all(),empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn')
#     enrollment2=forms.ModelChoiceField(queryset=models.Account.objects.all(),empty_label="Name and enrollment",to_field_name='regno',label='Name and enrollment')


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['room']


class DuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=addmessfee.objects.all().filter(feestatus=True))


class NoDuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=addmessfee.objects.all().filter(feestatus=False))

class DateForm(forms.ModelForm):
    checkIn = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years=YEARS))
    checkOut = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Reservation
        fields = ['checkIn', 'checkOut', ]


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'contact',
            'email',
            'dpmnt', ]


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', ]



class LeaveForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
    end_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
    reason = forms.CharField(max_length=100, help_text='100 characters max.',
                             widget=forms.TextInput(attrs={'placeholder': 'Enter Reason here'}))
    class Meta:
        model = Leaves
        fields = [
            'start_date',
            'end_date',
            'reason']
        
class RepairForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['repair']

        

class RebateForm(forms.Form):
    rebate = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))

