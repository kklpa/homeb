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
    totals = []
    for miesiac in miesiace:
        m = Zakup.objects.filter(month__name=miesiac).values('total').aggregate(Sum('total'))
        totals.append(miesiac)
        for kategoria in kategorie:
            k = (Zakup.objects.filter(user__username=request.user, month__name=miesiac, category=kategoria, year=datetime.datetime.now().year).values('category__name', 'total').aggregate(Sum('total')))
            k = k.pop('total__sum', '0')
            totals.append(kategoria)
            totals.append(k)
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
'''
'''
'''
'''

'''
z = Zakup.objects.filter(month__name='wrzesien').values('user__username')
user = auth.authenticate(username="name", password="pass")
15 elementor na 12 miesiecy

    sumy = []
    kategorie = Kategoria.objects.all()
    miesiace = Miesiac.objects.all()
    for miesiac in miesiace:
        for kategoria in kategorie:
            k = (Zakup.objects.filter(month__name=miesiac, category=kategoria).values('category__name', 'total').aggregate(Sum('total')))
            print(k)
            sumy.append(k)

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


