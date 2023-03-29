from django.urls import path, include
from .import views
from django.conf import settings
urlpatterns = [

 
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('ureg/', views.user_reg, name='user_reg'),
    path('', views.Student_Home, name='Student_Home'),
    path('Lib_Home', views.Lib_Home, name='Lib_Home'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout, name='logout'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    # path('add/', views.add, name='add'),
    path('Service/', views.Service, name='Service'),
    # path('Doc/', views.Doc, name='Doc'),
    # path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('Hostel_home/', views.Hostel_home, name='Hostel_home'),
    path('Outpass/', views.Outpass, name='Outpass'),
    path('outpass_history/',views.outpass_history,name='outpass_history'),
    path('outpassedit/<int:id>/',views.outpassedit,name='outpassedit'),
    path('deleteoutpass/<int:id>/',views.deleteoutpass,name='deleteoutpass'),
    path('profile/', views.profile, name='profile'),
    path('profile/update',views.profile_update,name='profile_update'),
    path('Library_home/', views.Library_home, name='Library_home'),
    path('Viewbookindex/', views.Viewbookindex, name='Viewbookindex'),
    path('onebook/<str:id>/',views.onebook,name='onebook'),
    path('Catagory_Books/<str:id>/',views.Catagory_Books,name='Catagory_Books'),
    path('searchbar',views.searchbar,name='searchbar'),
    path('form/', views.uploadForm, name='form'),
    path('files/', views.files, name='files'),
    path('upload/', views.uploadFile, name='upload'),
    path("issuebook_view/", views.issuebook_view, name="issuebook_view"),
    path("view_issued_book/", views.viewissuedbook_view, name="view_issued_book"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path('Wardenhome/', views.Wardenhome, name='Wardenhome'),
    path('WardenOutpassView/',views.WardenOutpassView,name='WardenOutpassView'),
    path('outpassapproved/<str:leave_id>',views.outpassapproved,name='outpassapproved'),
    path('outpassdisapprove/<str:leave_id>', views.outpassdisapprove,name="outpassdisapprove"),
    path('WardenDue/', views.WardenDue, name='WardenDue'),
    path('WardenMess/', views.WardenMess, name='WardenMess'),
    path('Student_complaint/', views.Student_complaint, name='Student_complaint'),
    path('Student_complaint_save', views.Student_complaint_save, name="Student_complaint_save"),
    path('WardenComplaintView', views.WardenComplaintView, name="WardenComplaintView"),
    path('student_complaint_message_replied/', views.student_complaint_message_replied, name="student_complaint_message_replied"),
    path('Librarianhome', views.Librarianhome, name="Librarianhome"),
    # path('warden_dues/', views.warden_dues, name='warden_dues'),
    # path('warden_add_due/', views.warden_add_due, name='warden_add_due'),
    # path('warden_remove_due/', views.warden_remove_due, name='warden_remove_due'),
    # path('send-sms/', views.send_sms, name='send_sms'),
    path('present_leaves/', views.present_leaves, name='present_leaves'),
    path('mess_rebate/', views.mess_rebate, name='mess_rebate'),
    path('Addroom', views.Addroom, name='Addroom'),
    path('table/',views.table,name='table'),
    path('addroomtable/<int:id>/',views.addroomtable,name='addroomtable'),
    path('productedit/<int:id>/',views.productedit,name='productedit'),
    path('productupdate/',views.productupdate,name='productupdate'),
    path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),
    path('Room_view',views.Room_view,name='Room_view'),
    path('RoomDetails/<int:id>/',views.RoomDetails,name='RoomDetails'),
    path('paymentdone',views.payment_done,name='paymentdone'),
    path('showbill',views.showbill,name='showbill'),
    path('Warden_AttendenceView',views.Warden_AttendenceView,name='Warden_AttendenceView'),
    path('ajax/', views.ajax, name= 'ajax'),
    path('scan/',views.scan,name='scan'),
    path('details/', views.details, name= 'details'),
    path('reset/',views.reset,name='reset'),
    path('clear_history/',views.clear_history,name='clear_history'),
    path('LibrarianAddBook', views.LibrarianAddBook, name='LibrarianAddBook'),
    path('booktable', views.booktable, name='booktable'),
    path('addbooktable/<int:id>/',views.addbooktable,name='addbooktable'),
    path('bookedit/<int:id>/',views.bookedit,name='bookedit'),
    path('bookupdate/<int:id>/',views.bookupdate,name='bookupdate'),
    path('deletebook/<int:id>/',views.deletebook,name='deletebook'),
    path('pdf/<int:id>/', views.get,name='pdf'),
    path('WardenViewPaymentDetails/',views.WardenViewPaymentDetails,name='WardenViewPaymentDetails'),


    # path('return_book/<int:id>',views.return_issued_book,name="return_issued_book"),
    # # path('edit_issued/<int:id>',views.edit_issued,name="edit_issued"),
    # path('mainPage', views.mainPage, name="mainPage"),
    # path("acceptedOutpassNotifications", views.acceptedOutpassNotifications, name="acceptedOutpassNotifications"),
    # path("acceptedOutpassNotifications1", views.acceptedOutpassNotifications1, name="acceptedOutpassNotifications1"),

]
