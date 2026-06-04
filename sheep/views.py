from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from farms.models import Farm
from .forms import SheepForm
from .models import Sheep


def get_user_farm(user):
    return Farm.objects.filter(owner=user).first()


@login_required
def sheep_list(request):
    farm = get_user_farm(request.user)

    sheep = Sheep.objects.none()

    if farm:
        sheep = Sheep.objects.filter(farm=farm).order_by("eid_number")

        query = request.GET.get("q")
        category = request.GET.get("category")

        if query:
            sheep = sheep.filter(eid_number__icontains=query)

        if category:
            sheep = sheep.filter(category=category)

    return render(request, "sheep/sheep_list.html", {
        "farm": farm,
        "sheep": sheep,
        "categories": Sheep.CATEGORY_CHOICES,
    })


@login_required
def sheep_create(request):
    farm = get_user_farm(request.user)

    if not farm:
        return redirect("farm_list")

    if request.method == "POST":
        form = SheepForm(request.POST)

        if form.is_valid():
            animal = form.save(commit=False)
            animal.farm = farm
            animal.save()
            return redirect("sheep_list")
    else:
        form = SheepForm()

    return render(request, "sheep/sheep_create.html", {"form": form})


@login_required
def sheep_detail(request, pk):
    farm = get_user_farm(request.user)

    animal = get_object_or_404(
        Sheep,
        pk=pk,
        farm=farm
    )

    return render(request, "sheep/sheep_detail.html", {
        "animal": animal
    })


@login_required
def sheep_update(request, pk):
    farm = get_user_farm(request.user)

    animal = get_object_or_404(
        Sheep,
        pk=pk,
        farm=farm
    )

    if request.method == "POST":
        form = SheepForm(request.POST, instance=animal)

        if form.is_valid():
            form.save()
            return redirect("sheep_detail", pk=animal.pk)
    else:
        initial = {
            "eid_number": animal.eid_number.replace("HR ", "")
        }

        form = SheepForm(instance=animal, initial=initial)

    return render(request, "sheep/sheep_create.html", {
        "form": form,
        "animal": animal,
        "edit_mode": True,
    })


@login_required
def sheep_delete(request, pk):
    farm = get_user_farm(request.user)

    animal = get_object_or_404(
        Sheep,
        pk=pk,
        farm=farm
    )

    if request.method == "POST":
        animal.delete()
        return redirect("sheep_list")

    return render(request, "sheep/sheep_confirm_delete.html", {
        "animal": animal
    })