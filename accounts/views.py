from django.shortcuts import render , redirect , render_to_response
import json
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from .forms import loginForm , SignInForm , Expense_form, Income_form
from django.contrib.auth import authenticate , login , logout
from .models import User , Expense , Incomes
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')

def register(request):
    form = SignInForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            print("user is saved")
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('first_name')
            return redirect("account:home")
    else:
        return render(request, 'accounts/login_page.html', {'form': form})

def login_view(request):
    form =  loginForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usera = authenticate(request, username = username , password = password)
            if usera is not None:
                login(request, usera)
                return render(request, 'accounts/Content.html')
            else:
                return HttpResponse("the user did not exist")
        else:
            return HttpResponse("the form is not valid ")
    else:
        return render(request,'accounts/login_page.html', {'form': form})


def logout_view(request):
    user = request.session
    try:
        logout(request)
    except:
        return HttpResponse("user doesnt exist to logout")
    return render(request , "accounts/home.html")

def welcome(request):
    if request.user.is_authenticated:
        return render(request , 'accounts/Content.html')
    else:
        return redirect('account:login')



def expense_form(request):
    form = Expense_form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            expense_temp_form = form.save(commit=False)
            expense_temp_form.user = request.user
            form.save()
            return redirect('account:expense_table')
        else:
            return HttpResponse("form was not valid")
    else:
        return render(request,'accounts/login_page.html',{'form':form})

def income_form(request):
    form = Income_form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            income_temp_form = form.save(commit=False)
            income_temp_form.user = request.user
            form.save()
            return redirect('account:income_table')
        else:
            return HttpResponse("form was not valid")
    else:
        return render(request , 'accounts/login_page.html',{'form':form})


def expense_table(request):
        if request.method == 'GET':
            today = datetime.now()
            month = today.month
            year = today.year
            tables = Expense.objects.filter(user = request.user ,date__month= month , date__year=year)
            total = float(0)
            for item in tables:
                total += float(item.price)
                total = round(total, 2)
            page = 'expense'
            return render(request , 'accounts/tab_content.html' , {'tables':tables , 'page':page , 'total':total})
        else:
            if request.is_ajax():
                form_value = request.POST.get('month')
                form_value = form_value.split('-')
                month = form_value[1]
                year = form_value[0]
                tables = Expense.objects.filter(user=request.user, date__month=month, date__year=year)
                serialized_data = serializers.serialize('json',tables,indent=2,use_natural_foreign_keys=True, use_natural_primary_keys=True)
                return HttpResponse(serialized_data,content_type='application/json')

def income_table(request):
    if request.method == 'GET':
        today = datetime.now()
        month = today.month
        year = today.year
        tables = Incomes.objects.filter(user = request.user , date__month = month , date__year=year)
        total = float(0)
        for item in tables:
            total += float(item.price)
            total = round(total , 2)
            print('the item does exist')
        page = 'income'
        return render(request,'accounts/tab_content.html', {'tables':tables , 'page':page , 'total':total})
    else:
        if request.is_ajax():
            form_value = request.POST.get('month')
            form_value = form_value.split('-')
            month = form_value[1]
            year = form_value[0]
            tables = Incomes.objects.filter(user=request.user, date__month=month, date__year=year)
            serialized_data = serializers.serialize('json', tables, indent=2, use_natural_foreign_keys=True,
                                                    use_natural_primary_keys=True)
            return HttpResponse(serialized_data, content_type='application/json')










