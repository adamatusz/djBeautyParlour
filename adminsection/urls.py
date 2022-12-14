from django.urls import path
from adminsection import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signin/', views.signin, name='signin'),
    path('service/', views.addservice, name='addservices'),
    path('manageservices/', views.manageservices, name='manageservices'),
    path('updateservice/<int:id>/', views.updateservice, name='updateservice'),
    path('addcustomer/', views.addcustomer, name='addcustomer'),
    path('customerlist/', views.customerlist, name='customerlist'),
    path('editcustomer/<int:id>/', views.editcustomer, name='editcustomer'),
    path('assignservices/<int:id>/', views.assignservices, name='assignservices'),
    path('newappointment/', views.newappointment, name='newappointment'),
    path('allappointment/', views.allappointment, name='allappointment'),
    path('viewappointment/<int:id>/', views.viewappointment, name='viewappointment'),
    path('viewinvoice/<int:id>', views.viewinvoice, name='viewinvoice'),
    path('acceptedappointment/', views.acceptedappointment, name='acceptedappointment'),
    path('rejectedappointment/', views.rejectedappointment, name='rejectedappointment'),
    path('invoices/', views.invoices, name='invoices'),
    path('searchappointment/', views.searchappointment, name='searchappointment'),
    path('searchinvoices/', views.searchinvoices, name='searchinvoices'),
    path('bwdatesreportsds/', views.bwdatesreportsds, name='bwdatesreportsds'),
    path('adminprofile/', views.adminprofile, name='adminprofile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('contactus/', views.contactus, name='contactus')
]
