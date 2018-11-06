from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from .forms import ZakupForm
from .models import Zakup, Kategoria, Miesiac

@login_required
def zakup_main(request):
    #zakupy = Zakup.objects.all()
    #zakupy = Zakup.objects.filter(user__username=request.user).values('pk', 'date', 'name', 'category', 'price', 'quantity', 'total', 'month__name', 'year')
    '''-----------------------------get last 5 records----------------------'''
    last = Zakup.objects.filter(user__username=request.user).order_by('-id')[:5]
    '''-----------------------------get summary last for 12 months----------'''
    kategorie = Kategoria.objects.all()
    miesiace = Miesiac.objects.all()
    month_now = datetime.datetime.now().month
    year_now = datetime.datetime.now().year
    totals = []
    month_counter = 0
    month_number = month_now
    year = year_now
    #start month now, stop -12, step -1
    for i in range(month_now, -12, -1):
        #count month for exit after 12 reached
        month_counter = month_counter+1
        if month_counter > 12:
            #print('mamy 12 miesiecy')
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
            k = (Zakup.objects.filter(user__username=request.user, month__id=month_number, category=kategoria, year=year).values('category__name', 'month__name', 'total').aggregate(Sum('total')))        
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
    '''------------------------get current day summary---------------------'''
    day_sum = Zakup.objects.filter(date=datetime.datetime.now()).values('total').aggregate(Sum('total'))
    day_sum = day_sum.pop('total__sum', '0')
    '''------------------------get current month summary-------------------'''
    month_sum = Zakup.objects.filter(month__id=month_now, year=year_now).values('total').aggregate(Sum('total'))
    month_sum = month_sum.pop('total__sum', '0')
    '''------------------------post form for dodaj zakup-------------------'''
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
    '''------------------------render page---------------------------------'''
    return render(request, 'homeb_app/main.html', { 'last': last, 'totals': totals, 'form': form, 'day_sum': day_sum, 'month_sum': month_sum })

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
    print('####: ', day_details)
    return render(request, 'homeb_app/zakup_day_detail.html', {'day_details': day_details })

@login_required
def zakup_month_detail(request):
    month_details = (Zakup.objects.filter(user__username=request.user, month__id=datetime.datetime.now().month, year=datetime.datetime.now().year).values('pk', 'name', 'price', 'quantity', 'category__name', 'month__name', 'total', 'date' ))
    print(month_details)
    return render(request, 'homeb_app/zakup_month_detail.html', {'month_details': month_details })

def login_view(request):
    return render(request, 'registration/login.hml', {'form': login})

def logout_view(request):
    return redirect(request, '/')

'''@login_required
def zakup_nowy(request):
    return render(request, 'homeb_app/main.html', {'form': form})
'''
'''
@login_required
def zakup_month(request):
    return render(request, 'homeb_app/zakup_month.html', ({ 'miesiace': miesiace, 'kategorie': kategorie, 'totals': totals }) )
'''
'''
@login_required
def zakup_last(request):
    return render(request, 'homeb_app/base.html', {'last': last})
'''

