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
                return redirect('account:total')
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
        return total(request)
    else:
        return redirect('account:login')

def total(request):
    if request.is_ajax():
        form_value = request.POST.get('month')
        form_value = form_value.split('-')
        month = form_value[1]
        year = form_value[0]
        e_table = Expense.objects.filter(user=request.user, date__month=month, date__year=year)
        i_table = Incomes.objects.filter(user=request.user, date__month=month, date__year=year)
        e_total = float(0)  # total for the users expenses for the month
        for item in e_table:
            e_total += float(item.price)
        e_total = round(e_total, 2)
        i_total = float(0)  # total for the users incomes for the month
        for item in i_table:
            i_total += float(item.price)
        i_total = round(i_total, 2)
        ie_total = i_total - e_total
        data = {
            'total': ie_total
        }
        category_expense_totals = {}
        for item in e_table:
            if str(item.category) not in category_expense_totals:
                category_expense_totals[str(item.category)] = float(item.price)
            else:
                category_expense_totals[str(item.category)] += float(item.price)

        sent_json = json.dumps({'total':ie_total,'category_expense_table':category_expense_totals})
        return HttpResponse(sent_json, content_type='application/JSON')

    else:
        today = datetime.today()
        month = today.month
        year = today.year
        e_table = Expense.objects.filter(user = request.user ,date__month= month , date__year=year)
        i_table = Incomes.objects.filter(user = request.user, date__month= month, date__year=year)
        e_total = float(0) #total for the users expenses for the month
        for item in e_table:
            e_total += float(item.price)
        e_total = round(e_total, 2)
        i_total = float(0) #total for the users incomes for the month
        for item in i_table:
            i_total += float(item.price)
        i_total = round(i_total, 2)
        ie_total = i_total - e_total
        ie_total = round(ie_total,2)
        if (month % 10) == 0: #look over this code one more time
            month_year = str(year)+"-"+str(month)
        else:
            month_year = str(year) + "-0" + str(month) # to set the value the month needs to be in YYYY-MM format

        category_expense_totals = {}
        for item in e_table:
            if str(item.category) not in category_expense_totals:
                category_expense_totals[str(item.category)] = float(item.price)
            else:
                category_expense_totals[str(item.category)] += float(item.price)
        category_expense_totals = json.dumps(category_expense_totals)
        print(category_expense_totals)
        return render(request, 'accounts/total.html', {'total':ie_total , 'month_year':month_year , 'cat_expense_total':category_expense_totals})




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










