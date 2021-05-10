from django.urls import path,include
from . import views
urlpatterns = [
    
    path('/addpatient',views.addpatient),
    path('/generatereport',views.home),
    path('/detect',views.detect),
    path('/userdetail',views.userdetail),
    path('/feedback', views.feedback),
    path('/logout', views.logout),

]