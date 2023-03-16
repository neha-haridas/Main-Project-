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
from .models import Account, Category, ComplaintStudent,Leave,addmessfee,Book,Category_Book,Files,Leaves
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
from .utils import render_to_pdf
from django.core.exceptions import ObjectDoesNotExist





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
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')



    
# def Viewbookindex(request):
#     tblBook = Book.objects.all()
#     category = Category_Book.objects.all()
#     return render(request,'Viewbookindex.html',{'datas':tblBook,'category':category})


    
def Viewbookindex(request):
    tblBook = Book.objects.values('id','book_name','book_category','book_language','book_desc','img','user')
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


###############################################################333333333

def bookhome(request):
    print(request.method)
    if request.method == "POST":
        form = DateForm(request.POST)
        # response = HttpResponse()  # Created a HttpResponse
        # response['Cache-Control'] = 'no-cache'  # Set Cache-Control Header
        if form.is_valid():
            start_date = form.cleaned_data['checkIn']

            end_date = form.cleaned_data['checkOut']
            print(start_date, end_date)
            delta = end_date - start_date
            if delta.days > 0 and (start_date-datetime.date.today()).days >= 0:
                cnt = 0
                x = Room.objects.none()
                print(Room.objects.all())
                for room in Room.objects.all():
                    RoomsBooked = Reservation.objects.filter(room=room,room_alloted=True,accept=True).\
                        filter(checkIn__lte=end_date,checkOut__gte=start_date)
                    print(RoomsBooked)
                    count = RoomsBooked.count()
                    count = int(count)
                    if count == 0:
                        cnt += 1
                        x = x | Room.objects.filter(pk = room.pk)
                print(cnt)
                print(x)
                res = form.save(commit=False)
                if cnt > 0:

                    res.save()
                    request.session['booking_id'] = res.booking_id
                    # form.save(form.save(commit=False))
                    # form = SelectionForm(instance=request.reservation)
                    # form.fields["room"].queryset = x
                    args = {'rooms': x, 'count': cnt, 'res': res}
                    return render(request, 'details.html', args)
                else:
                    return HttpResponse("<h1> No Rooms </h1> <br> <br> <a href =  '' >"
                                        " Book Again! </a> ")
            else:

                return HttpResponse("<h1> Invalid request </h1> <br> <br> <a href = '' >"
                                        " Book Again! </a> ")
        else:
            form = DateForm()
            print(request.method)
            return render(request, 'home.html', {'form': form})

    else:
        form = DateForm()
        print(request.method)
        return render(request, 'home.html', {'form': form})
    
@login_required
def select(request, res_id):

    if request.method == 'POST':
        form = SelectionForm(request.POST, instance=Reservation.objects.get(pk=res_id))
        if form.is_valid():
            res_now = form.save(commit=False)
            # res_now.save()
            request.session['room'] = res_now.room.no
            # kwargs = {"room": res_now.room}
            return redirect('guest:edit', res_id =res_id)
    else:
        print('res_id',res_id)
        res = Reservation.objects.get(pk=res_id)
        form = SelectionForm(instance=res)
        start_date = res.checkIn
        end_date = res.checkOut
        x = Room.objects.none()
        print(Room.objects.all())
        cnt = 0
        for room in Room.objects.all():
            RoomsBooked = Reservation.objects.filter(room=room,room_alloted=True,accept=True).\
                filter(checkIn__lte=end_date, checkOut__gte=start_date)
            print(RoomsBooked.values())
            count = RoomsBooked.count()
            count = int(count)
            if count == 0:
                cnt += 1
                x = x | Room.objects.filter(pk=room.pk)
        if res.room:
            x = x | Room.objects.filter(pk=res.room.pk)
            cnt = cnt +1
        print(cnt)
        print(x)
        form.fields["room"].queryset = x
        return render(request, 'select.html', {'form': form,'res':res})



@login_required
def bookings(request):
    try:
        guest = request.user.guest
        print(guest.first_name)
    except ObjectDoesNotExist:
        guest = Guest.objects.none()

    if guest:
        all_bookings = Reservation.objects.none()
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest,room_alloted = True,accept=True)
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest, room_alloted=True, reject=True)
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest, room_alloted=True, accept=False,reject=False)
        print(all_bookings.count)
        return render(request,'bookings.html',{"bookings":all_bookings,"guest":guest})
    elif request.user:

        return render(request, 'bookings.html',{"bookings":Reservation.objects.none(),"guest":guest})


@login_required
def confirm(request,res_id):
    res = Reservation.objects.get(pk=res_id)

    res.room_alloted = True
    res.save()
    return render(request,'guest/confirm.html',{"res_id":res_id} )


@login_required
def generate_pdf(request,res_id):
    booking = Reservation.objects.get(pk = res_id)
    data = {
        'res': booking
    }
    pdf = render_to_pdf('guest/invoice.html', data)
    if pdf is None:
        booking.guest.delete()
        booking.delete()
        return HttpResponse("<h1>Error While Loading!! <br> Try Again</h1>")
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def cancel(request,res_id):
    booking = Reservation.objects.get(pk=res_id)
    booking.delete()

    return HttpResponse('<h1> Booking Cancelled </h1> <br> <a href=\"../../home\"> Book Again! </a>')


#############################################


@login_required
def select(request):

    if request.method == 'POST':
        if request.user.student.room:
            room_id_old = request.user.student.room_id

        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                # stud = form.save(commit=False)
                # print(request.user.student.room_id, stud.room_id)
                request.user.student.room_allotted = True
                r_id_after = request.user.student.room_id
                room = Room.objects.get(id=r_id_after)
                room.vacant = False
                room.save()
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            else:
                request.user.student.room_allotted = False
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            student  = form.save()
            print(student.room_id)
            student = request.user.student
            leaves = Leave.objects.filter(student=request.user.student)
            return render(request, 'profile.html', {'student': student, 'leaves': leaves})
    else:
        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(instance=request.user.student)
        student_gender = request.user.student.gender
        student_course = request.user.student.course
        if student_course is None:
            return HttpResponse('No Course Selected <br> '
                                '<h3><a href = \'..\edit\' style = "text-align: center; color: Red ;"> Update Profile </a> </h3> ')
        student_room_type = request.user.student.course.room_type
        hostel = Hostel.objects.filter(
            gender=student_gender, course=student_course).order_by('name')
        print(student_gender, student_course, student_room_type)
        print(hostel)
        x = Room.objects.none()
        if student_room_type == 'B':
            # print(student_room_type)
            # for i in range(len(hostel)):
            #     h_id = hostel[i].id
            x = Room.objects.filter(
                hostel__id=hostel, room_type=['S','D'], vacant=True).order_by('no')

            # x = x | a
        else:
            # for i in range(len(hostel)):
            #     h_id = hostel[i].id
            x = Room.objects.filter(
                hostel_id__in=hostel, room_type=student_room_type, vacant=True).order_by('hostel_id','no')
            print(x)
            # x = x | a
        form.fields["room"].queryset = x
        print('x',x)
        return render(request, 'select_room.html', {'form': form})


def repair(request):

    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid() & request.user.student.room_allotted:

            rep = form.cleaned_data['repair']
            room = request.user.student.room
            room.repair = rep
            room.save()
            return HttpResponse('<h3>Complaint Registered</h3> <br> <a href = \'../../student_profile\''
                                ' style = "text-align: center; color: Red ;"> Go Back to Profile </a>')
        elif not request.user.student.room_allotted:
            return HttpResponse('<h3>First Select a Room </h3> <br> <a href = \'../select\''
                                ' style = "text-align: center; color: Red ;"> SELECT ROOM </a> ')

        else:
            form = RepairForm()
            room = request.user.student.room
            return render(request, 'repair_form.html', {'form': form, 'room': room})
    else:
        if not request.user.student.room_allotted:
            return HttpResponse('<h3>First Select a Room </h3> <br> <a href = \'../select\''
                                ' style = "text-align: center; color: Red ;"> SELECT ROOM </a> ')
        else:
            form = RepairForm()
            room = request.user.student.room
            return render(request, 'repair_form.html', {'form': form,'room': room})





# @login_required
def warden_dues(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            students = Account.objects.all()
            return render(request, 'dues.html', {'students': students})
    else:
        return HttpResponse('Invalid Login')


# @login_required
def warden_add_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = DuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = False
                    student.save()
                    return HttpResponse('Done')
            else:
                form = DuesForm()
                return render(request, 'add_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


# @login_required
def warden_remove_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = NoDuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = True
                    student.save()
                    return HttpResponse('Done')
            else:
                form = NoDuesForm()
                return render(request, 'remove_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


def empty_rooms(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        elif user.is_active:
            room_list = request.user.warden.hostel.room_set.filter(vacant=True).order_by('no')
            context = {'rooms': room_list}
            return render(request, 'empty_rooms.html', context)
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


def guest_requests(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        elif user.is_active:
            guest_request = Reservation.objects.filter(room_alloted = True,accept=False,reject=False)
            accepted_requests = Reservation.objects.filter(room_alloted = True,accept=True).order_by('-booking_id')[:10]
            print('true')
            return render(request, 'guest_requests.html', {'requests': guest_request,'accepted':accepted_requests})
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


def bookings(request,b_id):
    try:
        guest = Reservation.objects.get(booking_id = b_id).guest
        print(guest.first_name)
    except ObjectDoesNotExist:
        guest = Guest.objects.none()

    if guest:
        all_bookings = Reservation.objects.none()
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest,room_alloted = True,accept=True)
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest, room_alloted=True, reject=True)
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest, room_alloted=True, accept=False,reject=False)
        print(all_bookings.count)
        return render(request,'bookings.html',{"bookings":all_bookings,"guest":guest})
    else:

        return render(request, 'bookings.html',{"bookings":Reservation.objects.none(),"guest":guest})


@login_required
def guest_accept(request,res_id):
    res = Reservation.objects.get(booking_id=res_id)

    if res.room_alloted is True:
        res.accept = True
    else:
        res.reject = True

    res.save()
    return redirect('../../guest_requests')


@login_required
def guest_reject(request, res_id):
    res = Reservation.objects.get(booking_id=res_id)

    if res.room_alloted is True:
        res.reject = True
        res.save()
    else:
        res.delete()

    return redirect('../../guest_requests')
