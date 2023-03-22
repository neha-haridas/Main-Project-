# from pyexpat import model
from pyexpat import model
from django.contrib import admin

# Register your models here.
from .models import Account, Book, Category_Book,librarian
from django.contrib.auth.admin import UserAdmin

from mycardapp import models

# admin.site.unregister(Group)


class AccountAdmin(admin.ModelAdmin):
    list_display=['first_name','email','contact','regno','dpmnt']
admin.site.register(Account,AccountAdmin)

class librarianAdmin(admin.ModelAdmin):
    list_display=['First_name','Last_name','email','Phone_number','is_libr','is_active']
admin.site.register(librarian,librarianAdmin)


# warden_site.register(Account)


class WardenAdminArea(admin.AdminSite):
    site_header ='Warden Admin Area'
warden_site=WardenAdminArea(name='WardenAdmin')


# class OutpassAdmin(admin.ModelAdmin):
#     list_display = ['name','dept','mobno','sem','ldate','idate','purpose','dest','status']
# admin.site.register(tbl_outpass,OutpassAdmin)    
# warden_site.register(tbl_outpass,OutpassAdmin)



class LibraryAdminArea(admin.AdminSite):
    site_header ='Library Admin Area'
library_site=LibraryAdminArea(name='LibraryAdmin') 
class BookAdmin(admin.ModelAdmin):
    list_display = ['book_name','book_category','book_quantity','book_price','book_author','book_language','book_publisher','book_status']
library_site.register(Book,BookAdmin)    

class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id','category_name']
library_site.register(Category_Book,BookCategoryAdmin)    

