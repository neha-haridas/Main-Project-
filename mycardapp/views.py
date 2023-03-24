from audioop import reverse
from contextvars import Token
from importlib.metadata import files
# from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse

from mycardapp.utils import send_twilio_message
from .models import Account, ComplaintStudent,Leave,addmessfee,Book,Category_Book,Files,Room
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


# from datetime import date
# from twilio.rest import Client

import datetime,calendar
from .forms import *
from datetime import date
from mycardapp.encryption_util import *
# from .utils import render_to_pdf
# from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import razorpay 




# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def Student_Home(request):
    return render(request,'Student_Home.html')

def Lib_Home(request):
    return render(request,'Lib_Home.html')


def Service(request):
    return render(request,'Service.html')

def Hostel_home(request):
    return render(request,'Hostel_home.html')

def Library_home(request):
    return render(request,'Library_home.html')

def addbook(request):
    return render(request,'addbook.html')

def Librarianhome(request):
    return render(request,'Librarianhome.html')




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






# @login_required(login_url='login')
# def add(request):
#     user = request.user

#     categories = user.category_set.all()

#     if request.method == 'POST':
#         data = request.POST
#         images = request.FILES.getlist('images')
#         upload = request.FILES.getlist('upload')

#         if data['category'] != 'none':
#             category = Category.objects.get(id=data['category'])
#         elif data['category_new'] != '':
#             category, created = Category.objects.get_or_create(
#                 user=user,
#                 name=data['category_new'])
#         else:
#             category = None

#         for image in images:
#             photo = Document.objects.create(
#                 category=category,
#                 description=data['description'],
#                 image=image,
#                 upload=upload,
                
#             )

#         return redirect('Doc')
#     return render(request,'add.html',{'categories': categories})


# @login_required(login_url='login')
# def Doc(request):
#     user = request.user
#     category = request.GET.get('category')
#     if category == None:
#         photos = Document.objects.filter(category__user=user)
#     else:
#         photos = Document.objects.filter(
#             category__name=category, category__user=user)

#     categories = Category.objects.filter(user=user)
#     context = {'categories': categories, 'photos': photos}
 
#     return render(request,'Doc.html',context)


# @login_required(login_url='login')
# def viewPhoto(request, pk):
#     photo = Document.objects.get(id=pk)
#     return render(request, 'photo.html', {'photo': photo})


def profile(request):
    return render(request,'profile.html')

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

def searchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(book_name__icontains=query) | Q(book_author__icontains=query) | Q(book_language__icontains=query))
            products = Book.objects.filter(multiple_q) 
            return render(request, 'searchbar.html', {'datas':products})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
    return render(request, 'searchbar.html', {}) 


# def issuebook(request):
#     ibook = Book.objects.all()
#     category = Category_Book.objects.all()
#     return render(request,'issuebook.html',{'products':ibook,'category':category})


# @login_required(login_url='login')
# def issue_book(request):
#     user = request.user
#     if request.method == "POST":
#             obj = models.issuedBooks()
#             obj.bookname = request.POST['bookname']
#             obj.issued_date = request.POST['issuedate']
#             obj.expiry_date=request.POST['expridate']
#             obj.save()
#             alert = True
#             return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
#     return render(request, "issue_book.html")

#############################################


def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'bookissued.html')
    return render(request,'issuebook.html',{'form':form})



@login_required(login_url='login')
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'view_issued_book.html',{'li':li})





@login_required(login_url = 'login')
def student_issued_books(request):
    student = Account.objects.filter(request.user.id)
    issuedBooks = issuedBooks.objects.filter(user=student[0].id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(bookname=i.bookname)
        for book in books:
            t=(request.user.id, request.user.first_name, book.book_name,book.book_author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>15:
            day=d-14
            fine=day*5
        t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)

    return render(request,'student_issued_books.html',{'li1':li1, 'li2':li2})



from django.db.models import Q


# class FileView(generic.ListView):
#     # user = request.user
#     model = Files
#     template_name = 'file.html'
#     context_object_name = 'files'
#     paginate_by = 6

#     def get_queryset(self):
#     	return Files.objects.order_by('user_id')

###############################################################

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
 
###############################################################################################

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


# from django.conf import settings
# from twilio.rest import Client
# from django.http import HttpResponse

# def send_sms(request):
#     account_sid = settings.TWILIO_ACCOUNT_SID
#     auth_token = settings.TWILIO_AUTH_TOKEN
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         to=request.POST.get('parents_contact'),
#         from_=settings.TWILIO_FROM_NUMBER,
#         body=request.POST.get('message')
#     )
#     return HttpResponse('SMS sent!')


@login_required(login_url='view_login')
def outpass_history(request):
    user = request.user
    opass =Leave.objects.filter(user_id=user)
    return render(request,'outpass_history.html',{'opass':opass })  


def Wardenhome(request):
    return render(request,'Wardenhome.html')



def WardenOutpassView(request):
    outpas =Leave.objects.all()
    return render(request,'WardenOutpassView.html',{'outpas':outpas})


def outpassapproved(request,leave_id):
    appout=Leave.objects.get(id=leave_id)
    appout.status=1
    appout.save()
    return redirect('WardenOutpassView')
    

def outpassdisapprove(request,leave_id):
    appout=Leave.objects.get(id=leave_id)
    appout.status=2
    appout.save()
    return redirect('WardenOutpassView')
    
   

def WardenDue(request):
    return render(request,'Warden_Due.html')


def WardenMess(request):
    messfee=Account.objects.filter(is_user = True)
    if request.method == 'POST':
        amount = request.POST.get("amount")
        user = Account.objects.get(id=request.user.id)
        pay = addmessfee(user=user,amount=amount)
        pay.save()    
    return render(request,'WardenMess.html',{'messfee':messfee})




# def WardenMess(request):
#     # messfee=Account.objects.filter(is_user = True)
#     user = request.user
#     if user is not None:
#         if not user.is_warden:
#             return HttpResponse('Invalid Login')
#         else:
#             if request.method == 'POST':
#                 amount = request.POST.get("amount")
#                 user = Account.objects.get(id=request.user.id)
#                 pay = addmessfee(user=user,amount=amount)
#                 pay.save()    
#     return render(request,'WardenMess.html')


#####################################################

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
    




###############################################################################################

def present_leaves(request):
    user = request.user
    if user is not None:
        if not user.is_staff:
            return HttpResponse('Invalid Login')
        elif user.is_active:
            warden_hostel = user.is_warden
            stud = Account.objects.filter(room__hostel=warden_hostel)
            leaves = Leave.objects.filter(user__in=stud,status='1',ldate__lte=datetime.date.today(), idate__gte=datetime.date.today()).values_list('user', flat=True).distinct()
            stud = Account.objects.filter(id__in= leaves)
            # print(leaves.query)
            print(stud.query)
            # print(stud)
            return render(request, 'present_leaves.html', {'student': stud})
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


def mess_rebate(request):
    if request.method == 'POST':
        user = request.user
        form = RebateForm(request.POST)
        if user is not None:
            if not user.is_staff:
                return HttpResponse('Invalid Login')
            elif user.is_active and form.is_valid():
                reb = form.cleaned_data['rebate']
                print(reb)
                warden_hostel = user.is_user
                stud = Account.objects.filter(room__hostel=warden_hostel)
                leaves = Leave.objects.filter(user__in=stud, status="1")
                stud_rebate_list = {}
                this_month = reb.month
                first_day = datetime.date(reb.year, this_month, 1)

                for stud_id in stud:
                    cnt = 0
                    for leave in leaves:
                        if leave.user.id == stud_id.id and (leave.ldate.month == this_month or leave.idate.month == this_month)  :
                            if (reb-leave.idate).days > 0:

                                dayz = abs(leave.idate-first_day).days - abs(leave.ldate-first_day).days + 1
                            else:
                                dayz = abs(reb - first_day).days - abs(leave.ldate - first_day).days
                            print(leave.idate,first_day,stud_id.first_name,dayz)
                            cnt = cnt+dayz
                    stud_rebate_list[stud_id.regno] = cnt
                print(stud_rebate_list)
                month_name = calendar.month_name[this_month]
                return render(request, 'mess_rebate.html',{'form': form, 'count_rebate': stud_rebate_list, 'student': stud})
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid Login')
    else:
        form = RebateForm()
        stud_rebate_list={}
        stud=Account.objects.none()

        return render(request, 'mess_rebate.html', {'form': form,'count_rebate': stud_rebate_list,'student': stud})


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
    return render(request, "tables.html",{'products':products})

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


# def RoomDetails(request,id):
#     room =Room.objects.filter(id=id)
#     return render(request,'RoomDetails.html',{'room':room })




def RoomDetails(request,id):
    room =Room.objects.filter(id=id)
    product = Room.objects.all()
    # user = request.user
    # cart=Room.objects.filter(user_id=user)
    for i in room:
        total = i.price
    razoramount = total*100
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET_KEY))
    data = {
        "amount": total,
        "currency": "INR",
        "receipt": "order_rcptid_11"
    }
    payment_response = client.order.create(data=data)
    print(payment_response)
    order_id = payment_response['id']
    request.session['order_id'] = order_id
    order_status = payment_response['status']
    if order_status == 'created':
        payment = Payment(
            user=request.user,
            amount=total,
            razorpay_order_id = order_id,
            razorpay_payment_status = order_status
            )
        payment.save()
    return render(request,'RoomDetails.html',{'room':room,'total':total,'razoramount':razoramount, })



# def payment_done(request):
#     order_id=request.session['order_id']
#     payment_id = request.GET.get('payment_id')
#     print(payment_id)
#     payment=Payment.objects.get(razorpay_order_id = order_id)
#     payment.paid = True
#     payment.razorpay_payment_id = payment_id
#     payment.save()

#     room = Room.objects.filter(id=id)
#     room.update(available=models.F('available') - 1)

#     OrderPlaced.objects.create(
#         user=request.user,
#         payment=payment,
#         product=room.first(),
#         is_ordered=True
#     ).save() 
#     return redirect('Room_view')

# def payment_done(request):
#     order_id = request.session['order_id']
#     payment_id = request.GET.get('payment_id')

#     payment = Payment.objects.get(razorpay_order_id=order_id)

#     payment.paid = True
#     payment.razorpay_payment_id = payment_id
#     payment.razorpay_payment_status = 'paid' # set payment status to 'paid'
#     payment.save()

#     room_id = payment.orderplaced_set.first().product.id
#     room = Room.objects.get(id=room_id)
#     room.available -= 1
#     room.save()

#     OrderPlaced.objects.create(
#         user=request.user,
#         payment=payment,
#         product=room,
#         status='New',
#         is_ordered=True
#     )

#     return redirect('Room_view')


def payment_done(request):
    order_id=request.session['order_id']
    payment_id = request.GET.get('payment_id')
    print(payment_id)
    payment=Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.razorpay_payment_status = 'paid'
    payment.save()

    cart=Room.objects.filter(user=request.user)
    # item = Product.objects.get(product=product, id=item_id)

    for c in cart:
        OrderPlaced(user=request.user,room_type=c.room_type,available=c.available,payment=payment,is_ordered=True).save()
        c.delete()
        c.cart.available -= 1
        c.cart.save()
    # messages.success(request, 'Payment done successfully you can view the order details on your profile'
    #                           'Continue Shopping')
    return redirect('showbill')



@login_required(login_url='login')
def showbill(request):
    orders = OrderPlaced.objects.filter(
        user=request.user, is_ordered=True).order_by('ordered_date')
    context = {
        'orders': orders
    }
    return render(request, "showbill.html",context)


#########################Attendence######################################

from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
import face_recognition
import cv2
import numpy as np
import winsound
from django.db.models import Q
from playsound import playsound
import os


last_face = 'no_face'
current_path = os.path.dirname(__file__)
sound_folder = os.path.join(current_path, 'sound/')
face_list_file = os.path.join(current_path, 'face_list.txt')
sound = os.path.join(sound_folder, 'beep.wav')


def Warden_AttendenceView(request):
    scanned = LastFace.objects.all().order_by('date').reverse()
    present = Account.objects.filter(present=True).order_by('updated').reverse()
    # absent = Account.objects.filter(present=False).order_by('shift')
    context = {
        'scanned': scanned,
        'present': present,
        # 'absent': absent,
    }
    return render(request, 'Warden_AttendenceView.html', context)


def ajax(request):
    last_face = LastFace.objects.last()
    context = {
        'last_face': last_face
    }
    return render(request, 'ajax.html', context)


def scan(request):

    global last_face

    known_face_encodings = []
    known_face_names = []

    profiles = Account.objects.all()
    for profile in profiles:
        person = profile.image
        image_of_person = face_recognition.load_image_file(f'media/{person}')
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{person}'[:-4])


    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:

        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    profile = Account.objects.get(Q(image__icontains=name))
                    if profile.present == True:
                        pass
                    else:
                        profile.present = True
                        profile.save()

                    if last_face != name:
                        last_face = LastFace(last_face=name)
                        last_face.save()
                        last_face = name
                        winsound.PlaySound(sound, winsound.SND_ASYNC)
                    else:
                        pass

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == 13:
            break

    video_capture.release()
    cv2.destroyAllWindows()
#     return HttpResponse('scaner closed', last_face)
