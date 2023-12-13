from django import forms
from django.shortcuts import render
from django.urls import path
from commercial.models import FicheTarification, TransferedFicheTarification
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.utils import timezone
import datetime
from jet.dashboard import dashboard
from commercial.adminsite import commercial_admin


class PeriodForm(forms.Form):
    period_choices = [
        ('day', _('Jour en cours')),
        ('week', _('Semaine en cours')),
        ('month', _('Mois en cours')),
        ('year', _('Année en cours depuis janvier')),
    ]

    period = forms.ChoiceField(choices=period_choices, required=True, label=_(''))

    # start_date = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     required=False,
    #     label=_('Début')
    # )

    # end_date = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     required=False,
    #     label=_('Fin')
    # )


def daily_transactions_view(request):
    if request.GET and not 'period' in request.GET:
        request.GET = request.GET.copy()
        request.GET['period'] = 'day'
        
    form = PeriodForm(request.GET)
    context = {'form': form}

    period = form.fields['period']
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        total_purchase_grams, total_purchase_currency, total_sale_grams, total_sale_currency = get_purchases_and_sales(
            period, start_date, end_date)

        context['total_purchase_grams'] = total_purchase_grams
        context['total_purchase_currency'] = total_purchase_currency
        context['total_sale_grams'] = total_sale_grams
        context['total_sale_currency'] = total_sale_currency

    return render(request, 'commercial/admin/daily_transactions.html', context)

def get_purchases_and_sales(period, start_date, end_date):
    today = timezone.now().date()

    if period == 'day':
        end_date = today
    elif period == 'week':
        end_date = today
        start_date = end_date - datetime.timedelta(days=today.weekday())
    elif period == 'month':
        end_date = today
        start_date = datetime.date(today.year, today.month, 1)
    elif period == 'year':
        end_date = today
        start_date = datetime.date(today.year, 1, 1)

    queryset = FicheTarification.objects.filter(date__range=(start_date, end_date), transferer=True)
    total_purchase_grams = queryset.aggregate(Sum('poids_kilograms'))['poids_kilograms__sum'] or 0
    total_purchase_currency = queryset.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Add your logic here for sales
    total_sale_grams = 0
    total_sale_currency = 0

    return total_purchase_grams, total_purchase_currency, total_sale_grams, total_sale_currency

from django.template.loader import render_to_string
def charts_view(request):
    context = {}
    context['tarification'] = TransferedFicheTarification.objects.all()
    return render(request, "commercial/admin/chart_module.html", context)

# This method registers view's path
dashboard.urls.register_urls([
    path(
        'daily-transactions/',
        commercial_admin.admin_view(daily_transactions_view),
        name='daily-transactions'
    ),
    path(
        'chart/',
        commercial_admin.admin_view(charts_view),
        name='charts'
    )
])