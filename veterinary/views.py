from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from farms.models import Farm
from sheep.models import Sheep
from .models import VeterinaryRecord
from .forms import VeterinaryRecordForm


def get_user_farm(user):
    return Farm.objects.filter(owner=user).first()


@login_required
def veterinary_list(request):
    farm = get_user_farm(request.user)

    records = VeterinaryRecord.objects.none()

    if farm:
        records = VeterinaryRecord.objects.filter(
            animal__farm=farm
        ).select_related("animal").order_by("-date")

        record_type = request.GET.get("type")
        query = request.GET.get("q")

        if record_type:
            records = records.filter(record_type=record_type)

        if query:
            records = records.filter(animal__eid_number__icontains=query)

    return render(request, "veterinary/veterinary_list.html", {
        "records": records,
        "types": VeterinaryRecord.RECORD_TYPES,
    })


@login_required
def veterinary_create(request):
    farm = get_user_farm(request.user)

    if not farm:
        return redirect("farm_list")

    if request.method == "POST":
        form = VeterinaryRecordForm(request.POST)
        form.fields["animal"].queryset = Sheep.objects.filter(farm=farm)

        if form.is_valid():
            form.save()
            return redirect("veterinary_list")
    else:
        form = VeterinaryRecordForm()
        form.fields["animal"].queryset = Sheep.objects.filter(farm=farm)

    return render(request, "veterinary/veterinary_form.html", {"form": form})


@login_required
def veterinary_delete(request, pk):
    farm = get_user_farm(request.user)

    record = get_object_or_404(
        VeterinaryRecord,
        pk=pk,
        animal__farm=farm
    )

    if request.method == "POST":
        record.delete()
        return redirect("veterinary_list")

    return render(request, "veterinary/veterinary_confirm_delete.html", {
        "record": record
    })