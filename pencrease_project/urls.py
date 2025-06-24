"""diabetesproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from userapp import views as user_views
from adminapp import views as admin_views
from mainapp import views as main_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Main
    path('admin/', admin.site.urls),
    path('', main_views.home, name = 'home'),
    path('login/', user_views.login, name = 'login' ),
    path('register', user_views.register, name = 'register' ),
    path('admin', main_views.admin, name = 'admin' ),
    path('contact', main_views.contact, name = 'contact' ),
    path('about', main_views.about, name = 'about' ),
    # User
    path('predict', user_views.predict, name = 'predict' ),
    path('user-dashboard', user_views.userdashboard, name = 'userdashboard' ),
    path('profile', user_views.profile, name = 'profile' ),
    path('result', user_views.result, name = 'result'),
    path('userlogout', user_views.userlogout, name = 'userlogout'),
    path('otpverify', user_views.otpverify, name = 'otpverify'),
    
    # Admin 
    path('admin-dashboard', admin_views.admindashboard, name = 'admindashboard'),
    path('pending-users', admin_views.pendingusers, name = 'pendingusers'),
    path('all-users', admin_views.allusers, name = 'allusers'),
    path('upload-dataset', admin_views.uploaddataset, name = 'uploaddataset'),
    path('view-dataset', admin_views.viewdataset, name = 'viewdataset'),
   
    path('knn-algm', admin_views.knnalgm, name = 'knnalgm'),
    path('annalgm', admin_views.annalgm, name = 'annalgm'),
    path('logistc', admin_views.logistc, name = 'logistc'),
  
    path('sxn-alg', admin_views.sxmalgm, name = 'sxmalgm'),
    path('dt-algm', admin_views.dtalgm, name = 'dtalgm'),
    path('c-graph', admin_views.cgraph, name = 'cgraph'),
    path('accept-user/<int:id>', admin_views.accept_user, name = 'accept_user'),
    path('reject-user/<int:id>', admin_views.reject_user, name = 'reject'),
    path('delete-user/<int:id>', admin_views.delete_user, name = 'delete_user'),
    path('delete-dataset/<int:id>',admin_views.delete_dataset, name = 'delete_dataset'),
    path('admin-logout', admin_views.adminlogout, name='adminlogout'),
 
    path('KNN_btn', admin_views.KNN_btn, name='KNN_btn'),
    path('ANN_btn', admin_views.ANN_btn, name='ANN_btn'),
    path('logistic_btn', admin_views.logistic_btn, name='logistic_btn'),

    path('SXM_btn', admin_views.SXM_btn, name='SXM_btn'),
    path('Decisiontree_btn', admin_views.Decisiontree_btn, name='Decisiontree_btn'),
    path('view_view', admin_views.view_view, name='view_view'),
    # path('sendSMS', user_views.sendSMS, name = 'sendSMS'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

