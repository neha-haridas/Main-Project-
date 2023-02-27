from django.urls import path, include
from .import views
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
    path('profile/', views.profile, name='profile'),
    path('profile/update',views.profile_update,name='profile_update'),
    path('Library_home/', views.Library_home, name='Library_home'),
    path('Viewbookindex/', views.Viewbookindex, name='Viewbookindex'),
    path('onebook/<int:id>/',views.onebook,name='onebook'),
    path('Catagory_Books/<int:id>/',views.Catagory_Books,name='Catagory_Books'),
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




    # path('return_book/<int:id>',views.return_issued_book,name="return_issued_book"),
    # # path('edit_issued/<int:id>',views.edit_issued,name="edit_issued"),
    # path('mainPage', views.mainPage, name="mainPage"),
    # path("acceptedOutpassNotifications", views.acceptedOutpassNotifications, name="acceptedOutpassNotifications"),
    # path("acceptedOutpassNotifications1", views.acceptedOutpassNotifications1, name="acceptedOutpassNotifications1"),




]