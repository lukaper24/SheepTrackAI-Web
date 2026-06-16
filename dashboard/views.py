from datetime import date, timedelta
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from farms.models import Farm
from sheep.models import Sheep
from lambing.models import Lambing, Lamb

from django.http import JsonResponse


@login_required
def home(request):
    farm = Farm.objects.filter(owner=request.user).first()

    stats = {
        "total_sheep": 0,
        "ewes": 0,
        "rams": 0,
        "lambs": 0,
        "lambings": 0,
        "unmarked_lambs": 0,
    }

    alerts = []
    chart_labels = []
    chart_data = []

    if farm:
        sheep = Sheep.objects.filter(farm=farm)
        lambings = Lambing.objects.filter(mother__farm=farm)
        lambs = Lamb.objects.filter(lambing__mother__farm=farm)

        stats["total_sheep"] = sheep.count()
        stats["ewes"] = sheep.filter(category="OVCA").count()
        stats["rams"] = sheep.filter(category="OVAN").count()
        stats["lambs"] = lambs.count()
        stats["lambings"] = lambings.count()
        stats["unmarked_lambs"] = lambs.filter(official_tag="").count()

        if stats["unmarked_lambs"] > 0:
            alerts.append(f"{stats['unmarked_lambs']} janjadi još nema službenu markicu.")

        old_date = date.today() - timedelta(days=365)
        inactive_ewes = sheep.filter(category="OVCA").exclude(
            lambings__lambing_date__gte=old_date
        ).distinct()

        if inactive_ewes.exists():
            alerts.append(f"{inactive_ewes.count()} ovaca nije imalo janjenje u zadnjih 12 mjeseci.")

        young_mothers = sheep.filter(
            sex="Z",
            birth_date__gt=date.today() - timedelta(days=304)
        )

        if young_mothers.exists():
            alerts.append(f"{young_mothers.count()} ženskih grla još nije dovoljno staro za janjenje.")

        for month in range(1, 13):
            count = lambings.filter(
                lambing_date__year=date.today().year,
                lambing_date__month=month
            ).count()

            chart_labels.append(str(month))
            chart_data.append(count)

    return render(request, "home.html", {
        "farm": farm,
        "stats": stats,
        "alerts": alerts,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
    })

def about(request):
    return render(request, "about.html")


def api_dashboard_stats(request):
    farm = Farm.objects.filter(owner=request.user).first()

    data = {
        "total_sheep": 0,
        "active_sheep": 0,
        "lambings": 0,
        "lambs": 0,
        "veterinary_records": 0,
        "weights": 0,
    }

    if request.user.is_authenticated and farm:
        from lambing.models import Lambing, Lamb
        from veterinary.models import VeterinaryRecord
        from weights.models import WeightRecord
        from sheep.models import Sheep

        data = {
            "total_sheep": Sheep.objects.filter(farm=farm).count(),
            "active_sheep": Sheep.objects.filter(farm=farm, status="ACTIVE").count(),
            "lambings": Lambing.objects.filter(mother__farm=farm).count(),
            "lambs": Lamb.objects.filter(lambing__mother__farm=farm).count(),
            "veterinary_records": VeterinaryRecord.objects.filter(animal__farm=farm).count(),
            "weights": (
                WeightRecord.objects.filter(sheep__farm=farm).count()
                + WeightRecord.objects.filter(lamb__lambing__mother__farm=farm).count()
            ),
        }

    return JsonResponse(data)