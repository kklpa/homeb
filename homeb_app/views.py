from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from .forms import ZakupForm
from .models import Zakup, Kategoria, Miesiac

def get_last5(user):
    last5 = Zakup.objects.filter(user__username=user).order_by('-id')[:5]
    return last5

def get_totals(user, month, year):
    kategorie = Kategoria.objects.all()
    miesiace = Miesiac.objects.all()
    totals = []
    month_counter = 0
    month_number = month
    #start month now, stop -12, step -1
    for i in range(month, -12, -1):
        #count month for exit after 12 reached
        month_counter = month_counter+1
        if month_counter > 12:
            break
        #check if year has changed
        if month_number == 0:
            month_number = 12
            year = year-1
        #get current month name
        month_name = Miesiac.objects.filter(id=month_number)
        #append month name to list
        totals.append(month_name[0])
        #iterate categories for each month and get data
        for kategoria in kategorie:
            k = (Zakup.objects.filter(user__username=user, month__id=month_number, category=kategoria, year=year).values('category__name', 'month__name', 'total').aggregate(Sum('total')))        
            #k = (Zakup.objects.filter(user__username=request.user, month__id=miesiac, category=kategoria, year=datetime.datetime.now().year).values('category__name', 'total').aggregate(Sum('total')))
            #k = (Zakup.objects.filter(user__username=request.user, month__name=miesiac, category=kategoria, year=2018).values('category__name', 'total').aggregate(Sum('total')))
            #remove total__sum from k
            k = k.pop('total__sum', '0')
            #append category name
            totals.append(kategoria)
            #append queried total for category in current month
            totals.append(k)
        #decrement month number
        month_number = month_number-1
    #print('totals: ', totals)      
    return totals

def get_day_sum(user, day):
    day_sum = Zakup.objects.filter(user__username=user, date=day).values('total').aggregate(Sum('total'))
    day_sum = day_sum.pop('total__sum', '0')
    return day_sum

def get_month_sum(user, month, year):
    month_sum = Zakup.objects.filter(user__username=user, month__id=month, year=year).values('total').aggregate(Sum('total'))
    month_sum = month_sum.pop('total__sum', '0')
    return month_sum

@login_required
def zakup_main(request):
    '''-----------------------------set variables---------------------------'''
    today = datetime.datetime.now()
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    '''-----------------------------get last 5 records----------------------'''
    last5 = get_last5(request.user)
    '''-----------------------------get summary last for 12 months----------'''
    totals = get_totals(request.user, month, year)
    '''-----------------------------get current day summary-----------------'''
    day_sum = get_day_sum(request.user, today)
    '''-----------------------------get current month summary---------------'''
    month_sum = get_month_sum(request.user, month, year)
    
    '''-----------------------------post form for dodaj zakup---------------'''
    if request.method == "POST":
        form = ZakupForm(request.POST)
        if form.is_valid():
            zakup = form.save(commit=False)
            zakup.total = zakup.price * zakup.quantity
            zakup.user = request.user
            zakup.save()
            return redirect('/')
    else:
        form = ZakupForm(initial={'year': datetime.datetime.now().year, 'month': datetime.datetime.now().month })
    
    '''----------------------------render page------------------------------'''
    return render(request, 'homeb_app/main.html', { 'last5': last5, 'totals': totals, 'form': form, 'day_sum': day_sum, 'month_sum': month_sum })

@login_required
def zakup_delete(request, pk):
    zakup = Zakup.objects.get(pk=pk).delete()
    return redirect('/')

@login_required
def zakup_detail(request, pk):
    zakup = get_object_or_404(Zakup, pk=pk)
    return render(request, 'homeb_app/zakup_detail.html', {'zakup': zakup })

@login_required
def zakup_day_detail(request):
    day_details = (Zakup.objects.filter(user__username=request.user, date=datetime.datetime.now()).values('pk', 'name', 'price', 'quantity', 'category__name', 'month__name', 'total', 'date' ))
    return render(request, 'homeb_app/zakup_day_detail.html', {'day_details': day_details })

@login_required
def zakup_month_detail(request):
    month_details = (Zakup.objects.filter(user__username=request.user, month__id=datetime.datetime.now().month, year=datetime.datetime.now().year).values('pk', 'name', 'price', 'quantity', 'category__name', 'month__name', 'total', 'date' ))
    return render(request, 'homeb_app/zakup_month_detail.html', {'month_details': month_details })

def login_view(request):
    return render(request, 'registration/login.hml', {'form': login})

def logout_view(request):
    return redirect(request, '/')
