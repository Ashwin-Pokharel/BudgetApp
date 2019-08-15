from django.conf.urls import url
from . import views

app_name = 'account'
urlpatterns = [
    url(r'^home', views.home, name='home'),
    url(r'^register', views.register , name = 'register'),
    url(r'^login',views.login_view , name= 'login'),
    url(r'^welcome', views.welcome , name='welcome'),
    url(r'^logout', views.logout_view , name = 'logout'),
    url(r'^expense_form',views.expense_form , name='expense_form'),
    url(r'^expenses' , views.expense_table , name='expense_table'),
    url(r'^incomes', views.income_table , name= 'income_table'),
    url(r'^income_form', views.income_form, name='income_form'),
]