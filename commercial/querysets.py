from commercial.models import Lingot

from django.db.models import Q

def stock_queryset(queryset=None):
        if not queryset:
            qs = Lingot.objects.all()
        else:
              qs = queryset
        # Apply your custom filters to the queryset
        qs = qs.exclude(control_bumigeb__etat='out')
        qs = qs.exclude(fonte__etat='out')
        qs = qs.exclude(vente__conclu=True)

        qs.exclude(mouvementlingotlingot__isnull=False)
        # exclude moved ones
        # lingot_ids = MouvementLingot.objects.all().values_list('lingots__id', flat=True)
        # print(len(lingot_ids) > 0)
        # if len(lingot_ids) > 0:
        #     qs = qs.exclude(id__in=lingot_ids)

        return qs

def vente_queryset(queryset=None):
    if not queryset:
        qs = Lingot.objects.all()
    else:
        qs = queryset
    
    
    stock_a_avendre = stock_queryset().filter(avendre=True, vente__isnull=True)

    qs = qs.filter(
        Q(vente__isnull=True, control_bumigeb__isnull=False, control_bumigeb__etat='in') |\
        Q(id__in=stock_a_avendre.values_list('id', flat=True))
    )

    
    # Exclure les lingots dejà designer comme ne faisant pas parti du stock dnas LingotAdmin
    qs = qs.exclude(control_bumigeb__etat='out') \
                .exclude(fonte__etat='out')\
                .exclude(vente__conclu=True)
    qs = qs
    return qs