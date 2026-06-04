from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from farms.models import Farm
from sheep.models import Sheep
from .models import Breeding
from .forms import BreedingForm


def get_user_farm(user):
    return Farm.objects.filter(owner=user).first()


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

    if request.method == "POST":
        form = BreedingForm(request.POST)

        form.fields["ewe"].queryset = Sheep.objects.filter(
            farm=farm,
            sex="Z"
        )

        form.fields["ram"].queryset = Sheep.objects.filter(
            farm=farm,
            sex="M"
        )

        if form.is_valid():
            form.save()
            return redirect("breeding_list")

    else:
        form = BreedingForm()

        form.fields["ewe"].queryset = Sheep.objects.filter(
            farm=farm,
            sex="Z"
        )

        form.fields["ram"].queryset = Sheep.objects.filter(
            farm=farm,
            sex="M"
        )

    return render(request, "breeding/breeding_form.html", {"form": form})


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