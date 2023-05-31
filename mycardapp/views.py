from audioop import reverse
from contextvars import Token
from importlib.metadata import files
# from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.http import HttpResponseRedirect, JsonResponse

from mycardapp.utils import send_twilio_message
from .models import Account, ComplaintStudent,Leave,Book,Category_Book,Files,Room,Payment,OrderPlaced,ComplaintStudent,LastFace,tbl_BookIssues,SearchHistory
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.views import generic



from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from datetime import date
from twilio.rest import Client

from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime,calendar
from .forms import *
from datetime import date
from mycardapp.encryption_util import *
# from .utils import render_to_pdf
# from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import razorpay 
import datetime
from django.shortcuts import render, HttpResponse, redirect


import numpy as np
from django.db.models import Q
import os
from django.db import connection
from decimal import Decimal


# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def Student_Home(request):
    is_hosteler = False
    if request.user.is_authenticated and request.user.choice == 'H':
        is_hosteler = True

    context = {
        'is_hosteler': is_hosteler,
    }

    return render(request, 'Student_Home.html', context)

def Lib_Home(request):
    return render(request,'Lib_Home.html')


def Service(request):
    return render(request,'Service.html')

def Hostel_home(request):
    payment = Payment.objects.filter(user=request.user, paid=True).first()
    can_access_outpass = payment is not None
    
    context = {
        'can_access_outpass': can_access_outpass
    }
    return render(request, 'Hostel_home.html', context)

def Library_home(request):
    return render(request,'Library_home.html')

def addbook(request):
    return render(request,'addbook.html')






def login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('pass')
        print(email, pswd)
        user = auth.authenticate(email=email, password=pswd)
        print(user)

        if user is not None:
            auth.login(request, user)
            # save email in session
            request.session['email'] = email
            if user.is_admin:
                return redirect('admin/')
            if user.is_libry:
                return redirect('Librarianhome')
            if user.is_staff:
                return redirect('Wardenhome')
            else:
                return redirect('Student_Home')
          
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')


def user_reg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = email.split('@')[0]
        contact = request.POST.get('contact')
        regno = request.POST.get('regno')
        dpmnt = request.POST.get('dpmnt')
        sem =request.POST.get('sem')
        password = request.POST.get('password')
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('user_reg')
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, contact=contact,regno=regno,dpmnt=dpmnt,sem=sem, password=password)
        user.is_user = True
        user.save()
        messages.info(request, 'Thank you for registering with us. Please Login')
        messages.success(request, 'Please verify your email for login!')

        current_site = get_current_site(request)
        message = render_to_string('account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })

        send_mail(
                    'Please activate your account',
                    message,
                    'mycardshelp@gmail.com',
                    [email],
                    fail_silently=False,
                )

        # return redirect('/login/?command=verification&email=' + email)

        return redirect('login')
    return render(request, 'user_reg.html')

def logout(request):
    auth.logout(request)
    return redirect('Student_Home')



@login_required
def changepassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            messages.info(request, 'Password updated successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('changepassword')
    return render(request, 'changepassword.html')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email


            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'mycardshelp@gmail.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'Forgot_Password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['pass']
        confirm_password = request.POST['repass']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.info(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')





def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('user_reg')        





def profile(request):
    choices = Account.hdchoices
    if not request.user.is_staff and not request.user.profile_updated:
        messages.info(request, 'Please update your profile.')
        request.user.profile_updated = True
        request.user.save()
    context = {
        'choices': choices,
    }
    return render(request,'profile.html',context)

def profile_update(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        regno = request.POST.get('regno')
        dpmnt = request.POST.get('dpmnt')
        sem = request.POST.get('sem')
        img= request.FILES.get('img', '')
        choice=request.POST.get('choice')
        user_id = request.user.id

        user = Account.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.contact = contact
        user.address = address
        user.pin = pin
        user.regno = regno
        user.dpmnt = dpmnt 
        user.sem = sem  
        user.img = img
        user.choice = choice
        user.profile_updated = True
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')



    
# def Viewbookindex(request):
#     tblBook = Book.objects.all()
#     category = Category_Book.objects.all()
#     return render(request,'Viewbookindex.html',{'datas':tblBook,'category':category})


    
def Viewbookindex(request):
    tblBook = Book.objects.values('id','book_name','book_category','book_language','book_desc','book_author','img','user')
    category = Category_Book.objects.all()
    for i in tblBook:
        i['encrypt_key']=encrypt(i['id'])
        i['id']=i['id']
    return render(request,'Viewbookindex.html',{'datas':tblBook,'category':category})




def onebook(request,id):
    rproduct = Book.objects.all()
    id=decrypt(id)
    single = Book.objects.filter(id=id)
    category = Category_Book.objects.all()
    return render(request, 'onebook.html', {'datas': single,'products':rproduct,'category':category})


# def onebook(request,id):
#     rproduct = Book.objects.all()
#     single = Book.objects.filter(book_id=id)
#     category = Category_Book.objects.all()
#     return render(request, 'onebook.html', {'datas': single,'products':rproduct,'category':category})

def Catagory_Books(request,id):
    if(Category_Book.objects.filter(category_id=id)):
        tblBook = Book.objects.filter(book_category_id=id)
    return render(request,'Catagory_Book.html',{'datas':tblBook})

from django.db.models import Count, Q
from .models import SearchHistory

def searchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            # Search for books that match the query
            multiple_q = Q(Q(book_name__icontains=query) | Q(book_author__icontains=query) | Q(book_language__icontains=query))
            products = Book.objects.filter(multiple_q)

            # Get the user's search history and save the new search
            user = request.user
            search = SearchHistory(user=user, query=query)
            search.save()
            history = SearchHistory.objects.filter(user=user).values('query').annotate(count=Count('query')).order_by('-count')[:3]

            # Exclude books that match the top two queries from the search history
            recommended_books = []
            if len(history) >= 1:
                recommended_books = Book.objects.filter(book_name__icontains=history[0]['query'])
            if len(history) >= 2:
                recommended_books = recommended_books.exclude(id__in=Book.objects.filter(book_name__icontains=history[1]['query']).values_list('id', flat=True))
            if len(history) >= 3:
                recommended_books = recommended_books.exclude(id__in=Book.objects.filter(book_name__icontains=history[2]['query']).values_list('id', flat=True))[:10]

            return render(request, 'searchbar.html', {'datas':products,'recommended_books': recommended_books})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
    return render(request, 'searchbar.html', {})


# from django.db.models import Count, Q
# from .models import SearchHistory

# def searchbar(request):
#     if request.method == 'GET':
#         query = request.GET.get('query')
#         if query:
#             # Search for books that match the query
#             multiple_q = Q(Q(book_name__icontains=query) | Q(book_author__icontains=query) | Q(book_language__icontains=query))
#             products = Book.objects.filter(multiple_q)

#             # Get the user's search history and save the new search
#             user = request.user
#             search = SearchHistory(user=user, query=query)
#             search.save()
#             history = SearchHistory.objects.filter(user=user).values('query').annotate(count=Count('query')).order_by('-count')[:3]
#             return render(request, 'searchbar.html', {'datas':products})
#         else:
#             messages.info(request, 'No search result!!!')
#             print("No information to show")
#     return render(request, 'searchbar.html', {})

##############################Book issue################################################

# from datetime import date, timedelta
# from django.shortcuts import get_object_or_404, render
# from django.http import Http404

# def issuebooklib(request, id):
#     try:
#         book = Book.objects.get(id=id)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")
    
#     user = request.user
#     today = date.today()
#     exp = today + timedelta(days=10)
#     obj = tbl_BookIssue.objects.create(
#         user_id=user.id,
#         book_id=book.id,
#         cat=book.book_category,
#         date_of_issue=today,
#         expiry_date=exp,
#         issuedstatus=True,
#     )
#     book.book_quantity -= 1
#     book.save()
#     return render(request, 'onebook.html', {'result': [obj]})



# def student_issued_books(request):
#     user = request.user
#     bk=tbl_BookIssue.objects.filter(user_id=user)
#     return render(request,'student_issued_books.html',{'bk':bk})


#############################################issue book working properly###################

from datetime import date, timedelta
from django.shortcuts import get_object_or_404, render, redirect
from .models import Book,tbl_BookIssues
from django.contrib.auth.decorators import login_required

@login_required
def issuebooklib(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    today = date.today()
    exp = today + timedelta(days=10)
    if book.book_quantity > 0:
        obj = tbl_BookIssues.objects.create(
            user=request.user,
            book=book,
            cat=book.book_category,
            date_of_issue=today,
            expiry_date=exp,
            issuedstatus=True,
        )
        messages.success(request, f"You have successfully issued '{book.book_name}'")
    else:
        messages.error(request, 'The book is out of stock!')

    return redirect('student_issued_books')

# @login_required
# def return_book_lib(request, id):
#     try:
#         bookissue = tbl_BookIssues.objects.get(id=id, issuedstatus=True)
#     except tbl_BookIssues.DoesNotExist:
#         raise Http404("Book issue does not exist or has already been returned")
    
#     if request.method == 'POST':
#         # Update the book issue object and the corresponding book object
#         bookissue.issuedstatus = False
#         bookissue.return_date = date.today()

#         # Calculate fine if book is returned late
#         if bookissue.return_date > bookissue.expiry_date:
#             days_late = (bookissue.return_date - bookissue.expiry_date).days
#             fine_per_day = 2  # Change this to whatever fine amount you want
#             fine_amount = days_late * fine_per_day
#             bookissue.fine = fine_amount

#         book = get_object_or_404(Book, id=bookissue.book.id)
#         book.book_quantity += 1
#         book.save()

#         bookissue.save()

#         return redirect('mybooks')
    
#     return render(request, 'mybooks.html', {'bookissue': bookissue})



@login_required
def return_book_lib(request, id):
    try:
        bookissue = tbl_BookIssues.objects.get(id=id, issuedstatus=True)
    except tbl_BookIssues.DoesNotExist:
        raise Http404("Book issue does not exist or has already been returned")
    
    if request.method == 'POST':
        # Update the book issue object and the corresponding book object
        bookissue.issuedstatus = False
        bookissue.return_date = date.today()

        # Calculate fine if book is returned late
        if bookissue.return_date > bookissue.expiry_date:
            days_late = (bookissue.return_date - bookissue.expiry_date).days
            fine_per_day = 2  # Change this to whatever fine amount you want
            fine_amount = days_late * fine_per_day
            bookissue.fine = fine_amount

        book = get_object_or_404(Book, id=bookissue.book.id)
        book.book_quantity += 1
        book.save()

        if bookissue.fine is None or bookissue.fine <= 0:
            return HttpResponseBadRequest("Fine not found or invalid for this book issue.")
        
        amount = int(bookissue.fine * 100)  # Converting to smallest currency unit
        if amount > 0:
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
            payment = client.order.create({'amount': amount, 'currency': 'INR'})

            bookissue.payment_id = payment['id']
            bookissue.save()
            return render(request, 'payment_success.html', {'payment': payment})
        else:
            return HttpResponseBadRequest("Fine amount is invalid.")
    
    return render(request, 'mybooks.html', {'bookissue': bookissue})
 
@login_required
def payment_success(request, id):
    bookissue = get_object_or_404(tbl_BookIssues, id=id, issuedstatus=False, payment_id=request.GET.get('payment_id'))
    if request.method == 'POST':
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
        try:
            status = client.payment.fetch(bookissue.payment_id)['status']
            if status == 'captured':
                messages.success(request, f"Your payment of Rs. {bookissue.fine} has been successfully received.")
                bookissue.payment_status = True
                bookissue.save()
            else:
                messages.error(request, "Payment was unsuccessful. Please try again or contact support.")
        except Exception as e:
            messages.error(request, "An error occurred while processing the payment. Please try again or contact support.")
            print(str(e))
        return redirect('mybooks')
    return render(request, 'payment_success.html', {'bookissue': bookissue})





@login_required
def mybooks(request):
    user = request.user
    issued_books = tbl_BookIssues.objects.filter(user=user, issuedstatus=True)
    return render(request, 'mybook.html', {'issued_books': issued_books})


def student_issued_books(request):
    user = request.user
    bk=tbl_BookIssues.objects.filter(user_id=user)
    return render(request,'student_issued_books.html',{'bk':bk})


def files(request):
    user = request.user
    file=Files.objects.filter(user_id=user)
    return render(request, 'file.html',{'files':file})


@login_required(login_url='login')
def uploadForm(request):
	return render(request, 'upload.html')

@login_required(login_url='login')
def uploadFile(request):
    user = request.user
    if request.method == 'POST':
        filename = request.POST['filename']
        descrip = request.POST['descrip']
        pdf = request.FILES['pdf']

        a = Files(user_id=user.id,filename=filename, descrip=descrip, pdf=pdf)
        a.save()
        messages.success(request, 'Files Submitted successfully!')
        return redirect('files')
    

def deletepdf(request,id):
    item  = Files.objects.get(id=id)
    item.delete()
    return redirect('files') 


 
###############################################################################################
@login_required(login_url='view_login')
def Outpass(request):
    user = request.user
    if request.method=="POST":
     name= request.POST.get("name",True)
     dept = request.POST.get("dept",True)
     sem = request.POST.get("sem",True)
     mobno=request.POST.get("mobno",True)
     ldate = request.POST.get("ldate",True)
     idate = request.POST.get("idate",True)
     purpose = request.POST.get("purpose",True)
     dest = request.POST.get("dest",True)
     parents_email= request.POST.get("parents_email",False)
     parents_contact=request.POST.get("parents_contact",False)
    #  sign = request.POST.get("sign",True)
     o = Leave(user_id=user.id,name=name,dept=dept,sem=sem,mobno=mobno,idate=idate,ldate=ldate,purpose=purpose,dest=dest,parents_email=parents_email,parents_contact=parents_contact)
     o.save()
    return render(request,'Outpass.html')

##############################################
# TWILIO_ACCOUNT_SID = 'AC7e1b12f105b868c334e9923e237a3e2a'
# TWILIO_AUTH_TOKEN = '080cc05e21e9313086823c94f15094a7'
# TWILIO_PHONE_NUMBER = '13215946647'

# def outpass_application(request):
#     if request.method == 'POST':
#         # Process form data and save the outpass application to database
#         data = request.POST.copy()
#         data['student'] = request.user.id
#         application = Leave.objects.create(**data.dict())

#         # Send SMS notification to the associated parent's phone number
#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#         parents_contact = application.parents_contact
#         message_body = f"Your child, {application.user.first_name}, has submitted a new outpass application. Please review it on the school's website."
#         message = client.messages.create(to=parents_contact,
#                                          from_=TWILIO_PHONE_NUMBER,
#                                          body=message_body)

#         return HttpResponseRedirect(reverse('outpass_history'))
#     else:
#         # Show the outpass application form to the user
#         return render(request, 'Outpass.html')
#####################################################
@login_required(login_url='view_login')
def outpass_history(request):
    user = request.user
    opass =Leave.objects.filter(user_id=user)
    return render(request,'outpass_history.html',{'opass':opass })  


def deleteoutpass(request,id):
    item  = Leave.objects.get(id=id)
    item.delete()
    return redirect('outpass_history') 

def outpassedit(request,id):
    value = Leave.objects.filter(id=id) 
    return render(request, "outpassedit.html",{'value':value}) 

def outpassupdate(request,id):
    user = request.user
    if request.method=="POST":
        id = request.POST.get('id')
        ldate = request.POST.get("ldate")
        idate = request.POST.get("idate")
        purpose = request.POST.get("purpose")
        dest = request.POST.get("dest")
        parents_email= request.POST.get("parents_email")
        parents_contact=request.POST.get("parents_contact")
        value = Leave.objects.get(id=id)  
        value.ldate = ldate
        value.idate = idate
        value.purpose = purpose
        value.dest = dest
        value.parents_email = parents_email
        value.parents_contact = parents_contact
        value.save()
        return redirect('outpass_history')
    return render(request,'outpassedit.html')

def Wardenhome(request):
    user = Account.objects.filter(is_user=True).count
    order = Payment.objects.all().count()
    amount = Payment.objects.all()
    complaint=ComplaintStudent.objects.all().count
    Revenue = 0
    for i in amount:
        Revenue += i.product.price
    return render(request,'Wardenhome.html',{'user':user,'order':order,'amount':amount,'Revenue':Revenue,'complaint':complaint})



def WardenOutpassView(request):
    outpas =Leave.objects.all()
    return render(request,'WardenOutpassView.html',{'outpas':outpas})


# def outpassapproved(request,leave_id):
#     appout=Leave.objects.get(id=leave_id)
#     appout.status=1
#     appout.save()
#     return redirect('WardenOutpassView')
    

# def outpassdisapprove(request,leave_id):
#     appout=Leave.objects.get(id=leave_id)
#     appout.status=2
#     appout.save()
#     return redirect('WardenOutpassView')
    


def outpassapproved(request,leave_id):
    appout=Leave.objects.get(id=leave_id)
    appout.status=1
    subject = "Your outpass request has been approved"
    message = "Dear Parent, applying Outpass request has been approved.Thank you."
    from_email = "wardenmycard@gmail.com"  # change this to your email address
    recipient_list = [appout.parents_email]  # send the email to the student's parent's email address
    send_mail(subject, message, from_email, recipient_list)
    appout.save()
    return redirect('WardenOutpassView')
    

def outpassdisapprove(request,leave_id):
    appout=Leave.objects.get(id=leave_id)
    appout.status=2
    subject = "Your outpass request has been disapproved"
    message = "Dear Parent, applying Outpass request has been disapproved.Thank you."
    from_email = "wardenmycard@gmail.com"  # change this to your email address
    recipient_list = [appout.parents_email]  # send the email to the student's parent's email address
    send_mail(subject, message, from_email, recipient_list)
    appout.save()
    return redirect('WardenOutpassView')
    
 

def WardenDue(request):
    return render(request,'Warden_Due.html')

############################################################################working properly################################################################
# def calculate_mess_fee(month, year):
#     # Get all the leaves for the given month and year
#     leaves = Leave.objects.filter(ldate__month=month, ldate__year=year)
    
#     # Calculate the total number of days the students have taken leave
#     total_leaves = 0
#     for leave in leaves:
#         total_leaves += (leave.idate - leave.ldate).days + 1
    
#     # Calculate the mess fee amount for the given month and year
#     mess_fee_amount = Decimal(1500) - (Decimal(10) * Decimal(total_leaves))
    
#     # Create a MessFee instance for the given month and year
#     mess_fee = MessFees.objects.create(month=month, year=year, amount=mess_fee_amount)
    
#     # Associate all the leaves with the MessFee instance
#     mess_fee.leaves.set(leaves)
    
#     return mess_fee

# def generate_mess_fee(request):
#     # Get the current month and year
#     current_month = datetime.now().month
#     current_year = datetime.now().year
    
#     # Calculate the mess fee for the current month and year
#     mess_fee = calculate_mess_fee(current_month, current_year)
    
#     # Return a response with the mess fee details
#     return HttpResponse(f"Mess fee for {mess_fee.month} {mess_fee.year}: {mess_fee.amount}")

# def mess_fee_details(request):
#     # Get all the mess fee instances
#     mess_fees = MessFees.objects.all()
    
#     # Render the mess fee details in an HTML template
#     return render(request, 'mess_fee_details.html', {'mess_fees': mess_fees})
    


# def messfee_studentview(request):
#     messfee=MessFees.objects.all()
#     return render(request,'messfee_studentview.html',{'messfee':messfee})
#################################################################################***#######################################################################

############################################################making paymnet ###################################################################
# def calculate_mess_fee(month, year):
#     # Get all the leaves for the given month and year
#     leaves = Leave.objects.filter(ldate__month=month, ldate__year=year)
    
#     # Calculate the total number of days the students have taken leave
#     total_leaves = 0
#     for leave in leaves:
#         total_leaves += (leave.idate - leave.ldate).days + 1
    
#     # Calculate the mess fee amount for the given month and year
#     mess_fee_amount = Decimal(1500) - (Decimal(10) * Decimal(total_leaves))
#     mess_fee_amount_float = float(mess_fee_amount)  # Convert Decimal to float
    
#     # Create a MessFee instance for the given month and year
#     mess_fee = MessFees.objects.create(month=month, year=year, amount=mess_fee_amount_float)
    
#     # Associate all the leaves with the MessFee instance
#     mess_fee.leaves.set(leaves)
    
#     return mess_fee


# razorpay_client = razorpay.Client(auth=("rzp_test_atlnSmR0BK0uGq", "IqCklsj8xA9HxtlN2FziELL1"))
# from django.http import HttpResponseBadRequest

# def generate_mess_fee(request):
#     messfee=MessFees.objects.all()
#     # Get the current month and year
#     current_month = datetime.now().month
#     current_year = datetime.now().year
    
#     # Calculate the mess fee for the current month and year
#     mess_fee = calculate_mess_fee(current_month, current_year)
    
#     # Get the amount from the POST data, or use the mess fee amount as a fallback
#     amount = request.POST.get('amount')
#     if amount is None:
#         amount = mess_fee.amount
#     else:
#         amount = int(amount) * 100  # Convert amount to paise
    
#     # Generate Razorpay order
#     order_data = {
#         "amount": amount,
#         "currency": "INR",
#         "notes": {
#             "order_type": "Mess Fee",
#             "user_id": request.user.id  # Replace with the user ID of the currently logged-in user
#         }
#     }
#     order = razorpay_client.order.create(data=order_data)
    
#     # Store the order ID in the MessFees model
#     mess_fee.payment_id = order["id"]
#     mess_fee.save()
    
#     # Render the payment form with Razorpay parameters
#     razor_amount = amount
#     order_id = order["id"]
#     return render(request, 'messfee_studentview.html', {'razor_amount': razor_amount, 'order_id': order_id,'messfee':messfee})



# def paymentdone(request):
#     payment_id = request.GET.get('payment_id')
    
#     try:
#         # Get the MessFee instance based on the payment ID
#         mess_fee = MessFees.objects.get(payment_id=payment_id)
#     except MessFees.DoesNotExist:
#         # Return an error response if no MessFees object is found for the payment ID
#         return HttpResponseBadRequest("Invalid payment ID")
    
#     # Update the payment status and payment date
#     mess_fee.user=request.user
#     mess_fee.payment = "Paid"
#     mess_fee.payment_date = datetime.now()
#     mess_fee.save()
    
#     # Render a response with the payment details
#     return render(request, 'payment_done.html', {'mess_fee': mess_fee})

def WardenMess(request):
    msfe=MessFees.objects.all()
    return render(request,'WardenMess.html',{'msfe':msfe})


#####################################################****************#######################################################
def messfee_studentview(request):
    mess_fees = MessFees.objects.filter(user=request.user)
    return render(request, 'messfee_studentview.html', {'mess_fees': mess_fees})


import pytz
import razorpay
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import MessFees, Leave

razorpay_client = razorpay.Client(auth=("rzp_test_atlnSmR0BK0uGq", "IqCklsj8xA9HxtlN2FziELL1"))

def calculate_mess_fee(mess_fee_instance):
    # get the start and end date of the month for which the mess fees is being calculated
    start_date = datetime(year=mess_fee_instance.year, month=int(mess_fee_instance.month), day=1).date()
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # get all the approved leaves within the month
    leaves = Leave.objects.filter(status=1, idate__range=(start_date, end_date))

    # calculate the total number of days for which the student was absent in the month
    total_days_absent = 0
    for leave in leaves:
        total_days_absent += (leave.idate - leave.ldate).days

    # calculate the mess fee
    mess_fee_rate = mess_fee_instance.user.mess_fee_rate
    total_days_present = (end_date - start_date).days + 1 - total_days_absent
    mess_fee = round(total_days_present * mess_fee_rate, 2)

    # update the mess fee for the instance
    mess_fee_instance.amount = mess_fee
    mess_fee_instance.save()

def generate_mess_fee(request):
    mess_fees = MessFees.objects.filter(user=request.user)
    # Get the current month and year
    current_month = datetime.now(pytz.timezone('Asia/Kolkata')).month
    current_year = datetime.now(pytz.timezone('Asia/Kolkata')).year

    # Check if the current user has already paid for the current month's mess fee
    if mess_fees.filter(month=current_month, year=current_year, payment="Paid").exists():
        messages.error(request, "You have already paid for this month's mess fee.")
        return redirect(reverse('messfee_studentview'))

    # Get or create the mess fee instance for the current month and year
    mess_fee_instance, created = MessFees.objects.get_or_create(month=current_month, year=current_year, user=request.user)

    # Calculate the mess fee for the current month and year if the instance is newly created
    if created:
        calculate_mess_fee(mess_fee_instance)

    # Get the amount
    amount = int(mess_fee_instance.amount * 100)

    # Create the Razorpay order
    order = razorpay_client.order.create({'amount':amount, 'currency':'INR'})

    # Save the order_id to the mess fee instance
    mess_fee_instance.payment_id = order['id']
    mess_fee_instance.save()

    # Render the payment page with the order details
    return render(request, 'payment.html', {'order': order})

def paymentdone(request):
    payment_id = request.GET.get('payment_id')
    
    try:
        # Get the MessFee instance based on the payment ID
        mess_fee = MessFees.objects.get(payment_id=payment_id)
    except MessFees.DoesNotExist:
        # Return an error response if no MessFees object is found for the payment ID
        return HttpResponseBadRequest("Invalid payment ID")
    
    # Update the payment status and payment date
    mess_fee.user = request.user
    mess_fee.payment = "Paid"
    mess_fee.payment_date = datetime.now()
    mess_fee.save()
    
    # Insert a new instance of MessFeePayment
    MessFees.objects.create(user=request.user, amount=mess_fee.amount)
    
    # Update the leave status for the associated leaves
    start_date = datetime(year=mess_fee.year, month=mess_fee.month, day=1).date()
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    leaves = Leave.objects.filter(status=1, idate__range=(start_date, end_date))
    
    for leave in leaves:
        if leave.user == request.user:
            # Update the leave status for the current user
            leave.status = 'Paid'
            leave.save()
    
    return redirect(reverse('messfee_studentview'))
##################################################################################################################################

def Student_complaint(request):
    stu_id=Account.objects.get(id=request.user.id)
    complaint_data=ComplaintStudent.objects.filter(user=stu_id)
    return render(request,"Student_complaint.html",{"complaint_data":complaint_data})

def Student_complaint_save(request):
    if request.method!="POST":
        return redirect('Student_complaint')
    else:
        complaint_msg=request.POST.get("complaint_msg")

        student_obj=Account.objects.get(id=request.user.id)
        try:
            complaint=ComplaintStudent(user=student_obj,complaint=complaint_msg,complaint_reply="")
            complaint.save()
            messages.success(request, "Successfully Sent Complaint")
            return redirect('Student_complaint')
        except:
            messages.error(request, "Failed To Send Complaint")
            return redirect('Student_complaint')


def WardenComplaintView(request):
    feedbacks=ComplaintStudent.objects.all()
    return render(request,"WardenComplaintView.html",{"feedbacks":feedbacks})


@csrf_exempt
def student_complaint_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")
    try:
        feedback=ComplaintStudent.objects.get(id=feedback_id)
        feedback.complaint_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
    

#######################Add Rooms########################################

def Addroom(request):
    if request.method == 'POST':
        room_type = request.POST['room_type']
        price = request.POST['price']
        available = request.POST['available']
        description = request.POST['description']
        room_image = request.FILES.get('room_image', '')

        room = Room.objects.create(
            room_type=room_type,
            price=price,
            available=available,
            description=description,
            room_image=room_image
        )
        room.save()
        messages.success(request, "Successfully Add room")


    hostels = Hostel.objects.all()
    context = {
        'hostels': hostels,
        'choices': Room.room_choice,
    }

    return render(request, 'Addroom.html', context)



def table(request):
    products = Room.objects.all()
    return render(request, "Warden_Room_tables.html",{'products':products})

def addroomtable(request,id):
    return redirect('table')




def productedit(request,id):
    products = Room.objects.get(id=id)

    context = {
        'products':products
    }
        
    return render(request, "productedit.html",context) 


def productupdate(request):
    if request.method == "POST":
        id = request.POST.get('id')
        # room_type = request.POST['room_type']
        price = request.POST['price']
        available = request.POST['available']
        description = request.POST['description']
        room_image = request.FILES['room_image']
        value = Room.objects.get(id=id)  
        value.room_image = room_image
        value.price = price
        value.available = available
        value.description = description
        value.save()
        return redirect('table')

        # print(cate,pname,pdesc,pimg,price,stock)
    return render(request, "productedit.html")



def WardenViewPaymentDetails(request):
    orders = OrderPlaced.objects.all()
    return render(request,'WardenViewPaymentDetails.html', {'orders': orders})


import csv
def order_detailslog(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_details.csv"'
    writer = csv.writer(response)
    writer.writerow(['user', 'ordered_date','product'])
    order_details = OrderPlaced.objects.all().values_list('user', 'ordered_date','product')
    for i in order_details:
        writer.writerow(i)
    return response


def deleteproduct(request,id):
    item  = Room.objects.get(id=id)
    item.delete()
    return redirect('table') 
    
def Room_view(request):
    single_rooms = Room.objects.filter(room_type='S')
    double_rooms = Room.objects.filter(room_type='D')
    triple_rooms = Room.objects.filter(room_type='T')
    both_rooms = Room.objects.filter(room_type='B')
    return render(request, "Room_view.html",{'single_rooms':single_rooms, 'double_rooms':double_rooms, 'triple_rooms':triple_rooms, 'both_rooms':both_rooms})


######################################Payment for rent and decrement with one year payment###########################################################


import pytz
from datetime import datetime, timedelta

def RoomDetails(request, id):
    room = Room.objects.filter(id=id).first()
    razor_amount = room.price * 100
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
    data = {
        "amount": razor_amount,
        "currency": "INR",
        "receipt": f"order_rcptid_{room.id}"
    }
    payment_response = client.order.create(data=data)
    order_id = payment_response['id']
    request.session['order_id'] = order_id
    order_status = payment_response['status']
    
    if order_status == 'created':
        if not Payment.objects.filter(user=request.user, paid=True).exists():
            payment = Payment(
            user=request.user,
            amount=room.price,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status,
            product=room
             )
            payment.save()
  
        else :
            user = request.user
            payment=Payment.objects.filter(user=user.id,paid=True)
            last_ordered = Payment.objects.filter(user=user).latest('created_at').created_at
            now = datetime.now(pytz.timezone('Asia/Kolkata'))
            if last_ordered and now - last_ordered < timedelta(days=365):
                # User has ordered within the past year, do not allow new order
                return redirect('Room_view')
    return render(request, 'RoomDetails.html', {'room': room, 'razor_amount': razor_amount})



@login_required(login_url='login')
def payment_done(request):
    order_id = request.session['order_id']
    payment_id = request.GET.get('payment_id')
    print(payment_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.razorpay_payment_status = 'paid'
    payment.save()
    if payment.paid == True:
        id=payment.product.id
        rom = Room.objects.filter(id=id) # get all available rooms
        for room in rom:
            room.available -= 1 # decrease the availability by 1
            room.save()
    rooms = Payment.objects.filter(user=request.user,razorpay_payment_status='paid')
    for room in rooms:
        room = payment.product
        student = Account.objects.get(id=room.user.id)
        student.room_allotted = True
        student.room = room
        student.save()
        order=OrderPlaced(user=request.user, product=room, payment=payment, is_ordered=True)
        
        order.save()
        # room.available -= 1
        print(order)
    return redirect('showbill')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def get(request,id,*args, **kwargs,):
        
        place = OrderPlaced.objects.get(id=id)
        date=place.payment.created_at

        orders= OrderPlaced.objects.filter(user_id=request.user.id,ordered_date=place.ordered_date)
        for o in orders:
            total=o.product.price
        addrs=Account.objects.get(id=request.user.id)
     
        #     print(i.user,"#######################")
        data = {
            "total":total,
            "orders":orders,
            "shipping":addrs,
        }
        pdf = render_to_pdf('report.html',data)
        if pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            # filename = "Report_for_%s.pdf" %(data['id'])
            filename = "Bill.pdf"

            content = "inline; filename= %s" %(filename)
            response['Content-Disposition']=content
            return response
        return HttpResponse("Page Not Found") 

@login_required(login_url='login')
def showbill(request):
    orders = OrderPlaced.objects.filter(user=request.user, is_ordered=True).order_by('ordered_date')
    return render(request, "PaymentdetailsStudent.html", {'orders': orders})
    

    
#########################Attendence######################################


################################Libraran####################

def Librarianhome(request):
    user = Account.objects.filter(is_user=True).count
    complaint=ComplaintBookStudent.objects.all().count
    issue=tbl_BookIssues.objects.all().count
    return render(request,'Librarianhome.html',{'user':user,'complaint':complaint,'issue':issue})

def LibrarianAddBook(request):
    cat = Category_Book.objects.all()
    if request.method == 'POST':
        book_name = request.POST['book_name']
        category_id = request.POST.get('category') 
        print("category_id:", category_id)
        book_category = Category_Book.objects.get(category_id=category_id)
        book_language = request.POST['book_language']
        book_author = request.POST['book_author']
        book_desc = request.POST['book_desc']
        book_year = request.POST['book_year']
        book_publisher = request.POST['book_publisher']
        img = request.FILES.get('img', '')
        book_price = request.POST['book_price']
        isbn = request.POST['isbn']
        book_quantity = request.POST['book_quantity']

        book = Book(
            book_category=book_category,
            book_name=book_name,
            book_language=book_language,
            book_author=book_author,
            book_desc=book_desc,
            book_year=book_year,
            book_publisher=book_publisher,
            img=img,
            book_price=book_price,
            isbn=isbn,
            book_quantity=book_quantity
        )
        book.save()
        messages.success(request, "Successfully Add room")
        return redirect('booktable')       
 
    return render(request, 'LibrarianAddBook.html',{'cat':cat})



def booktable(request):
    products = Book.objects.all()
    return render(request, "booktable.html",{'products':products})

def addbooktable(request,id):
    return redirect('booktable')




def bookedit(request,id):

    value = Book.objects.filter(id=id) 
    return render(request, "bookedit.html",{'value':value}) 


def bookupdate(request,id):
    if request.method == "POST":
        book_name = request.POST['book_name']
        book_language = request.POST['book_language']
        book_author = request.POST['book_author']
        book_desc = request.POST['book_desc']
        book_year = request.POST['book_year']
        book_publisher = request.POST['book_publisher']
        book_price = request.POST['book_price']
        isbn = request.POST['isbn']
        book_quantity = request.POST['book_quantity']
        value = Book.objects.get(id=id)  
        value.book_name = book_name
        value.book_language = book_language
        value.book_author = book_author
        value.book_desc = book_desc
        value.book_year = book_year
        value.book_publisher = book_publisher
        value.book_price = book_price
        value.isbn = isbn
        value.book_quantity = book_quantity
        value.save()
        return redirect('booktable')
    return render(request,"bookupdate.html")   

def deletebook(request,id):
    item  = Book.objects.get(id=id)
    item.delete()
    return redirect('booktable') 




def StudentBookScomplaint(request):
    stu_id=Account.objects.get(id=request.user.id)
    complaint_data=ComplaintBookStudent.objects.filter(user=stu_id)
    return render(request,"StudentLib_complaint.html",{"complaint_data":complaint_data})

def StudentBookScomplaint_save(request):
    if request.method!="POST":
        return redirect('StudentBookScomplaint')
    else:
        complaint_msg=request.POST.get("complaint_msg")

        student_obj=Account.objects.get(id=request.user.id)
        try:
            complaint=ComplaintBookStudent(user=student_obj,complaint=complaint_msg,complaint_reply="")
            complaint.save()
            messages.success(request, "Successfully Sent Complaint")
            return redirect('StudentBookScomplaint')
        except:
            messages.error(request, "Failed To Send Complaint")
            return redirect('StudentBookScomplaint')


def LibrarianComplaintView(request):
    feedbacks=ComplaintBookStudent.objects.all()
    return render(request,"LibrarianComplaintView.html",{"feedbacks":feedbacks})


@csrf_exempt
def student_bookcomplaint_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")
    try:
        feedback=ComplaintBookStudent.objects.get(id=feedback_id)
        feedback.complaint_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
    

def Librarian_issuedbooklist(request):
    issuebk=tbl_BookIssues.objects.all()
    return render(request,"Librarian_issuedbooklist.html",{"issuebk":issuebk})



##############################################################################################################################################################################
from django.db.models import Count

# def book_recommendations(request):
#     # Get the user's search history and save the new search
#     user = request.user
#     history = SearchHistory.objects.filter(user=user).values('query').annotate(count=Count('query')).order_by('-count')[:3]

#     # Exclude books that match the top two queries from the search history
#     recommended_books = []
#     if len(history) >= 1:
#         recommended_books = Book.objects.filter(book_name__icontains=history[0]['query'])
#     if len(history) >= 2:
#         recommended_books = recommended_books.exclude(id__in=Book.objects.filter(book_name__icontains=history[1]['query']).values_list('id', flat=True))
#     if len(history) >= 3:
#         recommended_books = recommended_books.exclude(id__in=Book.objects.filter(book_name__icontains=history[2]['query']).values_list('id', flat=True))[:10]

#     return render(request, 'Viewbookindex.html', {'recommended_books': recommended_books})
