from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from farms.models import Farm
from sheep.models import Sheep
from .models import Breeding
from .forms import BreedingForm


def get_user_farm(user):
    return Farm.objects.filter(owner=user).first()


def get_available_rams(farm):
    nine_months_ago = date.today() - timedelta(days=274)

    return Sheep.objects.filter(
        farm=farm,
        sex="M",
        status="ACTIVE",
        birth_date__lte=nine_months_ago
    )


@login_required
def breeding_list(request):
    farm = get_user_farm(request.user)

    breedings = Breeding.objects.none()

    if farm:
        breedings = Breeding.objects.filter(
            ewe__farm=farm
        ).select_related("ewe", "ram").order_by("-breeding_date")

    return render(request, "breeding/breeding_list.html", {
        "breedings": breedings
    })


@login_required
def breeding_create(request):
    farm = get_user_farm(request.user)

    if not farm:
        return redirect("farm_list")

    ewes = Sheep.objects.filter(
        farm=farm,
        sex="Z",
        status="ACTIVE"
    )

    rams = get_available_rams(farm)

    if request.method == "POST":
        form = BreedingForm(request.POST)

        form.fields["ewe"].queryset = ewes
        form.fields["ram"].queryset = rams

        if form.is_valid():
            form.save()
            return redirect("breeding_list")

    else:
        form = BreedingForm()

        form.fields["ewe"].queryset = ewes
        form.fields["ram"].queryset = rams

    return render(request, "breeding/breeding_form.html", {
        "form": form
    })


@login_required
def breeding_delete(request, pk):
    farm = get_user_farm(request.user)

    breeding = get_object_or_404(
        Breeding,
        pk=pk,
        ewe__farm=farm
    )

    if request.method == "POST":
        breeding.delete()
        return redirect("breeding_list")

    return render(request, "breeding/breeding_confirm_delete.html", {
        "breeding": breeding
    })