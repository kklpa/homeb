from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Zakup


def zakup_list(request, pk):
    zakupy = akup.objects.filter(category__name="jedzenie").values('price', 'date', 'name')
    return render(request, 'homeb/zakup_list.html', {'zakupy': zakupy})

def zakup_detail(request, pk):
    zakup = get_object_or_404(Zakup, pk=pk)
    return render(request, 'homeb/zakup_detail.html', {'zakup': zakup})

def zakup_nowy(request):
    if request.method == "POST":
        form = ZakupForm(request.POST)
        if form.is_valid():
            zakup = form.save(commit=False)
            zakup.date = date.auto_now()
            zakup.save()
            return redirect('zakup_list')
    else:
        form = ZakupForm()
    return render(request, 'homeb/zakup_edit.html', {'form': form})


'''class ZakupListView(ListView):
    model = Zakup
    context_object_name = 'zakup'

class ZakupCreateView(CreateView):
    model = Zakup
    fields = ('category', 'name', 'price', 'date')
    success_url = reverse_lazy('zakup_list')

class ZakupUpdateView(UpdateView):
    model = Zakup
    fields = ('category', 'name', 'price', 'date')
    success_url = reverse_lazy('zakup_list')'''
