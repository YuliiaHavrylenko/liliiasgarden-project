from django.shortcuts import render
from .forms import SoupForm, MultipleSoupForm
from django.forms import formset_factory
from .models import Soup


def home(request):
    return render(request, 'soup/home.html')


def order(request):
    multiple_form = MultipleSoupForm
    if request.method == 'POST':
        filled_form = SoupForm(request.POST)
        if filled_form.is_valid():
            created_soup = filled_form.save()
            created_soup_pk = created_soup.id
            note = 'Thanks for ordering! Your %s soup with %s and %s is on its way.' \
                   % (filled_form.cleaned_data['size'], filled_form.cleaned_data['topping1'],
                      filled_form.cleaned_data['topping2'],)
            filled_form = SoupForm()
        else:
            created_soup_pk = None
            note = 'Order was not created, please try again'
        return render(request, 'soup/order.html',
                          {"created_soup_pk": created_soup_pk, 'soupform': filled_form, 'note': note,
                           'multiple_form': multiple_form})
    else:
        form = SoupForm
        return render(request, 'soup/order.html', {'soupform': form, 'multiple_form': multiple_form})


def soups(request):
    number_of_soups = 2
    filled_multiple_soup_form = MultipleSoupForm(request.GET)
    if filled_multiple_soup_form.is_valid():
        number_of_soups = filled_multiple_soup_form.cleaned_data['number']
    SoupFormSet = formset_factory(SoupForm, extra=number_of_soups)
    formset = SoupFormSet()
    if request.method == 'POST':
        filled_formset = SoupFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = 'Soups have been ordered!'
            return render(request, 'soup/soups.html', {'note': note, 'formset': formset})
    else:
        return render(request, 'soup/soups.html', {'formset': formset})


def edit_order(request, pk):
    soup = Soup.objects.get(pk=pk)
    form = SoupForm(instance=soup)
    if request.method == "POST":
        filled_form = SoupForm(request.POST, instance=soup)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = 'Order has been updated.'
        else:
            note = "Soup order has failed. Try again"
        return render(request, 'soup/edit_order.html', {'note': note, 'soupform': form, 'soup': soup})
    return render(request, 'soup/edit_order.html', {'soupform': form, 'soup': soup})
