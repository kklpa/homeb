from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
import datetime

from .forms import ZakupForm
from .models import Zakup

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
            zakup.save()
            return redirect('zakup_list')
    else:
        form = ZakupForm()
    return render(request, 'homeb_app/zakup_edit.html', {'form': form})

'''
kategorie = Kategoria.objects.all()
for kategoria in kategorie:
    m = Zakup.objects.filter(month__name="sierpien", category=kategoria).values('category__name', 'total').aggregate(Sum('total'))
    print(kategoria, ':', m)


'''


#def zakup_month(request):
    #m = Zakup.objects.filter(month__name="sierpien").values('total').aggregate(Sum('total'))





    #miesiace = Zakup.objects.all().values('month', 'price')
    #for month in miesiace:
        #zakupy_month = Zakup.objects.filter(month__name=month).values('price').aggregate(Sum('price'))
      #ZZakup.objects.filter(month__name="sierpien").values('total').aggregate(Sum('total'))
#Zakup.objects.all().delete()
'''def login_view(request):
    return render(request, 'registration/login.hml', {'form': login})

def logout_view(request):
    return redirect(request, '/')
'''

'''
months = Zakup.objects.all().values('month', 'price')
for month in miesiace:
    asd = sum(month.values())
    print(month.values())
    print(asd)

'''
