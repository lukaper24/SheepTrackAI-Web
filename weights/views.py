from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from farms.models import Farm
from sheep.models import Sheep
from lambing.models import Lamb

from .models import WeightRecord
from .forms import WeightRecordForm


def get_user_farm(user):
    return Farm.objects.filter(owner=user).first()


@login_required
def weight_list(request):
    farm = get_user_farm(request.user)

    records = WeightRecord.objects.none()

    if farm:
        records = WeightRecord.objects.filter(
            sheep__farm=farm
        ) | WeightRecord.objects.filter(
            lamb__lambing__mother__farm=farm
        )

        records = records.order_by("-date")

    return render(request, "weights/weight_list.html", {
        "records": records
    })


@login_required
def weight_create(request):
    farm = get_user_farm(request.user)

    if not farm:
        return redirect("farm_list")

    if request.method == "POST":
        form = WeightRecordForm(request.POST)

        form.fields["sheep"].queryset = Sheep.objects.filter(
            farm=farm,
            status="ACTIVE"
        )

        form.fields["lamb"].queryset = Lamb.objects.filter(
            lambing__mother__farm=farm
        )

        if form.is_valid():
            form.save()
            return redirect("weight_list")

    else:
        form = WeightRecordForm()

        form.fields["sheep"].queryset = Sheep.objects.filter(
            farm=farm,
            status="ACTIVE"
        )

        form.fields["lamb"].queryset = Lamb.objects.filter(
            lambing__mother__farm=farm
        )

    return render(request, "weights/weight_form.html", {
        "form": form
    })


@login_required
def weight_delete(request, pk):
    farm = get_user_farm(request.user)

    record = get_object_or_404(
        WeightRecord,
        pk=pk
    )

    if record.sheep and record.sheep.farm != farm:
        return redirect("weight_list")

    if record.lamb and record.lamb.lambing.mother.farm != farm:
        return redirect("weight_list")

    if request.method == "POST":
        record.delete()
        return redirect("weight_list")

    return render(request, "weights/weight_confirm_delete.html", {
        "record": record
    })