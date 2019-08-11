from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import loginForm , SignInForm , Expense_form
from django.contrib.auth import authenticate , login , logout
from .models import User , Expense , Incomes
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
            return redirect('account:welcome')
        else:
            return HttpResponse("form was not valid")
    else:
        return render(request,'accounts/expenses_test_form.html',{'form':form})

def total_expense(request):
    expense_set = Expense.objects.filter(user=request.user)
    total_expense_amount = 0
    for expenses in expense_set:
        total_expense_amount += expenses.price
    return HttpResponse("the total expense amount is: " + str(total_expense_amount))

