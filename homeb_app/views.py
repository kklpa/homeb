from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from .forms import ZakupForm
from .models import Zakup, Kategoria, Miesiac

@login_required
def zakup_main(request):
    '''
    zakupy = Zakup.objects.all()
    '''
    zakupy = Zakup.objects.filter(user__username=request.user).values('pk', 'date', 'name', 'category', 'price', 'quantity', 'total', 'month__name', 'year')
    last = Zakup.objects.filter(user__username=request.user).order_by('-id')[:5]
    
    kategorie = Kategoria.objects.all()
    miesiace = Miesiac.objects.all()
    month_now = datetime.datetime.now().month
    year = datetime.datetime.now().year
    month_ids = Miesiac.objects.all().values('id')    
    
    totals = []
    month_table = []
    month_counter = 0
    month_number = 0
    month_number = month_now
    for month_id in month_ids:
        m = month_id.pop('id')
        month_table.append(m)
    for i in range(month_now, -12, -1):
        month_counter = month_counter+1
        if month_counter > 12:
            print('mamy 12 miesiecy')
            break
        if month_number == 0:
            month_number = 12
            year = year-1
        n = Miesiac.objects.filter(id=month_number)
        totals.append(n[0])
        for kategoria in kategorie:
            k = (Zakup.objects.filter(user__username=request.user, month__id=month_number, category=kategoria, year=year).values('category__name', 'month__name', 'total').aggregate(Sum('total')))        
            #k = (Zakup.objects.filter(user__username=request.user, month__id=miesiac, category=kategoria, year=datetime.datetime.now().year).values('category__name', 'total').aggregate(Sum('total')))
            #k = (Zakup.objects.filter(user__username=request.user, month__name=miesiac, category=kategoria, year=2018).values('category__name', 'total').aggregate(Sum('total')))
            k = k.pop('total__sum', '0')
            totals.append(kategoria)
            totals.append(k)
        month_number = month_number-1
    #print('totals: ', totals)      
    day_sum = Zakup.objects.filter(date=datetime.datetime.now()).values('total').aggregate(Sum('total'))
    day_sum = day_sum.pop('total__sum', '0')
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
    return render(request, 'homeb_app/main.html', {'zakupy': zakupy, 'last': last, 'totals': totals, 'form': form, 'day_sum': day_sum })

'''@login_required
def zakup_nowy(request):
    return render(request, 'homeb_app/main.html', {'form': form})
'''
@login_required
def zakup_month(request):
    return render(request, 'homeb_app/zakup_month.html', ({ 'miesiace': miesiace, 'kategorie': kategorie, 'totals': totals }) )

@login_required
def zakup_delete(request, pk):
    zakup = Zakup.objects.get(pk=pk).delete()
    return redirect('/')

@login_required
def zakup_detail(request, pk):
    zakup = get_object_or_404(Zakup, pk=pk)
    return render(request, 'homeb_app/zakup_detail.html', {'zakup': zakup })

def login_view(request):
    return render(request, 'registration/login.hml', {'form': login})

def logout_view(request):
    return redirect(request, '/')

'''
@login_required
def zakup_last(request):
    return render(request, 'homeb_app/base.html', {'last': last})
'''

