from django.shortcuts import render
from .forms import SoupForm


def home(request):
    return render(request, 'soup/home.html')


def order(request):
    if request.method == 'POST':
        filled_form = SoupForm(request.POST)
        if filled_form.is_valid():
            note = 'Thanks for ordering! Your %s soup with %s and %s is on its way.' \
                   % (filled_form.cleaned_data['size'], filled_form.cleaned_data['topping1'],
                      filled_form.cleaned_data['topping2'],)
            new_form = SoupForm
            return render(request, 'soup/order.html', {'soupform': new_form, 'note':note})
    else:
        form = SoupForm
        return render(request, 'soup/order.html', {'soupform': form})
