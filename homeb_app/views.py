from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
import datetime
from django.db.models import Sum

from .forms import ZakupForm
from .models import Zakup, Kategoria, Miesiac

def zakup_list(request):
    '''zakupy = Zakup.objects.filter(category__name="jedzenie").values('price', 'date', 'name')'''
    zakupy = Zakup.objects.all()
    return render(request, 'homeb_app/zakup_list.html', {'zakupy': zakupy})
def zakup_detail(request, pk):
    zakup = get_object_or_404(Zakup, pk=pk)
    return render(request, 'homeb_app/zakup_detail.html', {'zakup': zakup})
def zakup_nowy(request):
    if request.method == "POST":
        form = ZakupForm(request.POST)
        if form.is_valid():
            zakup = form.save(commit=False)
            #mnozymy cena przez ilosc i zapisujemy do cena
            zakup.total = zakup.price * zakup.quantity
            zakup.year = 2
            zakup.save()
            return redirect('zakup_list')
    else:
        form = ZakupForm()
    return render(request, 'homeb_app/zakup_edit.html', {'form': form})

#def zakup_month(request):



def zakup_month(request):
    kategorie = Kategoria.objects.all()
    miesiace = Miesiac.objects.all()
    totals = []
    for miesiac in miesiace:
        m = Zakup.objects.filter(month__name=miesiac).values('total').aggregate(Sum('total'))
        totals.append(miesiac)
        for kategoria in kategorie:
            k = (Zakup.objects.filter(month__name=miesiac, category=kategoria).values('category__name', 'total').aggregate(Sum('total')))
            k = k.pop('total__sum', '0')
            totals.append(kategoria)
            totals.append(k)
    return render(request, 'homeb_app/zakup_month.html', {'totals': totals})

'''


kategorie = Kategoria.objects.all()
miesiace = Miesiac.objects.all()
mie = []
kat = []
totals = []
for miesiac in miesiace:
    m = Zakup.objects.filter(month__name=miesiac).values('total').aggregate(Sum('total'))
    totals.append(miesiac)
    for kategoria in kategorie:
        k = (Zakup.objects.filter(month__name=miesiac, category=kategoria).values('category__name', 'total').aggregate(Sum('total')))
        k = k.pop('total__sum')
        totals.append(kategoria)
        totals.append(k)

kategorie = Kategoria.objects.all()
miesiace = Miesiac.objects.all()

month_overall = [] 
month_category_overall = []

for miesiac in miesiace:
    m = Zakup.objects.filter(month__name=miesiac).values('total').aggregate(Sum('total'))
    print('\npodsumowanie miesiaca: \n', miesiac, ':', m, '\n')
    month_overall.append(m)
    for kategoria in kategorie:
        k = (Zakup.objects.filter(month__name=miesiac, category=kategoria).values('category__name', 'total').aggregate(Sum('total')))
        print(kategoria, ':', k)
        month_category_overall.append(k)

content[0]
content[1]
itd 
'''


'''
    m = Zakup.objects.filter(month__name="sierpien").values('total').aggregate(Sum('total'))


    miesiace = Zakup.objects.all().values('month', 'price')
    for month in miesiace:
        zakupy_month = Zakup.objects.filter(month__name=month).values('price').aggregate(Sum('price'))
        Zakup.objects.filter(month__name="sierpien").values('total').aggregate(Sum('total'))
Zakup.objects.all().delete()
'''
'''
def login_view(request):
    return render(request, 'registration/login.hml', {'form': login})

def logout_view(request):
    return redirect(request, '/')
'''
