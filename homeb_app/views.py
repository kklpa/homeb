from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Zakup

@login_required
def zakup_list(request):
    zakupy = Zakup.objects.filter(category__name="jedzenie").values('price', 'date', 'name')
    return render(request, 'homeb_app/zakup_list.html', {'zakupy': zakupy})
@login_required
def zakup_detail(request, pk):
    zakup = get_object_or_404(Zakup, pk=pk)
    return render(request, 'homeb_app/zakup_detail.html', {'zakup': zakup})
@login_required
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
    return render(request, 'homeb_app/zakup_edit.html', {'form': form})

def login_view(request):
    return render(request, 'registration/login.hml', {'form': login})

def logout_view(request):
    return redirect(request, '/')

