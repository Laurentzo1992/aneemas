from audioop import reverse
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard, DefaultIndexDashboard

from jet.dashboard.modules import DashboardModule

from jet.dashboard import modules

from django.utils.translation import gettext as _

from django.urls import reverse

from commercial.dashboard.views import charts_view

from .models import FicheTarification, Lingot, TransferedFicheTarification, Vente
from django import forms
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.html import format_html



class PeriodForm(forms.Form):
    period_choices = [
        ('day', _('Jour en cours')),
        ('week', _('Semaine en cours')),
        ('month', _('Mois en cours')),
        ('year', _('Année en cours depuis janvier')),
    ]

    period = forms.ChoiceField(choices=period_choices, required=False, label=_(''))

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
from django.template.loader import render_to_string
class Charts(DashboardModule):
    def render(self):
        context = {}
        context['tarification'] = TransferedFicheTarification.objects.all()
        return render_to_string('commercial/admin/chart_module.html', context)

class DailyTransactionModule(DashboardModule):
    title = _('Daily Transactions')
    template = 'commercial/admin/daily_transactions.html'
    form = PeriodForm

    # def render(self):
    #     return render(self.context.request, 'commercial/admin/daily_transactions.html')
    #     return HttpResponseRedirect(reverse('jet-dashboard:daily-transactions'))

    def get_purchases_and_sales(self, period):
        # Add logic to retrieve and calculate total purchases and sales for the selected period
        # The example assumes 'FicheTarification' model, adjust as needed
        # queryset = FicheTarification.objects.filter(date_tarification__range=(start_date, end_date), transferer=True)
        ftrfs = FicheTarification.objects.filter(transferer=True)

        lgts = Lingot.objects.filter(or_fin__isnull=False, fichecontrol_id__in=ftrfs.values_list('fichecontrol__id', flat=True))
        total_purchase_currency = round(sum(Decimal(ftrf.total_price) for ftrf in ftrfs),0)
        total_purchase_currency = intcomma(total_purchase_currency).replace(',', ' ')
        total_purchase_grams = round(sum(Decimal(lgt.or_fin) for lgt in lgts) / 1000, 4)
        total_purchase_grams = intcomma(total_purchase_grams)

        total_sale_grams = 0  # Add your logic here for sales
        total_sale_currency = 0  # Add your logic here for sales

        return total_purchase_grams, total_purchase_currency, total_sale_grams, total_sale_currency

    def get_context_data(self):
        form = PeriodForm(self.context.request.GET)
        context = {}
        context['form'] = form

        if form.is_valid():
            period = form.cleaned_data['period']
            # start_date = form.cleaned_data['start_date']
            # end_date = form.cleaned_data['end_date']

            total_purchase_grams, total_purchase_currency, total_sale_grams, total_sale_currency = self.get_purchases_and_sales(
                period) # """ , start_date, end_date) """

            context['total_purchase_grams'] = total_purchase_grams
            context['total_purchase_currency'] = total_purchase_currency
            context['total_sale_grams'] = total_sale_grams
            context['total_sale_currency'] = total_sale_currency

        return context

class OrFrDashboardModule(DashboardModule):
    columns = 3
    template = 'commercial/admin/or.fr.html'  # Path to your HTML template
    title = "Or.fr"  # Title displayed on the dashboard

    def init_with_context(self, context):
        pass 

class KitcoDashboardModule(DashboardModule):
    columns = 3
    template = 'commercial/admin/kitco.com.html'  # Path to your HTML template
    title = "Kitco.com"  # Title displayed on the dashboard

    def init_with_context(self, context):
        pass 

class BullionRatesDashboardModule(DashboardModule):
    columns = 3
    template = 'commercial/admin/bullionrates.com.html'  # Path to your HTML template
    title = "Bullionrates.com"  # Title displayed on the dashboard

    def init_with_context(self, context):
        pass 

class ConvertisseurDashboardModule(DashboardModule):
    columns = 3
    template = 'commercial/admin/convertisseur.html'  # Path to your HTML template
    title = "Convertisseur"  # Title displayed on the dashboard

    def init_with_context(self, context):
        pass 

class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        # self.available_children.append(CoursDashboardModule)
        self.available_children.append(OrFrDashboardModule)
        self.available_children.append(KitcoDashboardModule)
        self.available_children.append(BullionRatesDashboardModule)
        self.available_children.append(ConvertisseurDashboardModule)
        # self.children.append(CoursDashboardModule(column=0, order=0))
        self.children.append(OrFrDashboardModule(column=0, order=1))
        self.children.append(KitcoDashboardModule(column=1, order=1))
        self.children.append(BullionRatesDashboardModule(column=2, order=1))
        self.children.append(ConvertisseurDashboardModule(column=1, order=0))
        self.children.append(DailyTransactionModule(column=2, order=0))
        self.children.append(Charts(column=0, order=2))
        self.children.append(modules.LinkList(
            _('Liens rapides'),
            layout='inline',
            draggable=True,
            deletable=False,
            collapsible=False,
            children=[
                [_('Accueil'), '/gesco'],
                [_('Changer mot de passe'),
                [_('Deconnexion'), reverse('gesco:logout')],
                 reverse('gesco:password_change')],
                 [_('Ventes'), reverse('gesco:lingots_disponibles_pour_vente_changelist')],
                 [_('Achat'), reverse('gesco:commercial_fichecontrol_changelist')],
                 [_('Mouvements lingots'), reverse('gesco:commercial_lingot_changelist')]
            ],
            column=0,
            order=0
        ))

        # self.children.append(FullWidthModule(column=0, order=0))


        # Add a row with three modules
        # self.children.append(ThreeModulesRow(column=0, order=1))
        pass


