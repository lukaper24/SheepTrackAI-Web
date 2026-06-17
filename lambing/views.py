from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from farms.models import Farm
from sheep.models import Sheep

from .forms import LambingForm, LambForm
from .models import Lambing, Lamb


def get_user_farm(user):
    return Farm.objects.filter(owner=user).first()


@login_required
def lambing_list(request):
    farm = get_user_farm(request.user)

    lambings = Lambing.objects.none()

    if farm:
        lambings = Lambing.objects.filter(
            mother__farm=farm
        ).select_related(
            "mother",
            "father_sheep"
        ).order_by("-lambing_date")

    return render(request, "lambing/lambing_list.html", {
        "farm": farm,
        "lambings": lambings,
    })


@login_required
def lambing_create(request):
    farm = get_user_farm(request.user)

    if not farm:
        return redirect("farm_list")

    LambFormSet = modelformset_factory(
        Lamb,
        form=LambForm,
        extra=5,
        can_delete=False
    )

    mothers = Sheep.objects.filter(
        farm=farm,
        sex="Z",
        status="ACTIVE"
    )

    # Otac kod janjenja mora biti dovoljno star:
    # 9 mjeseci za pripust + oko 5 mjeseci skotnosti = cca 424 dana.
    father_min_birth_date = date.today() - timedelta(days=424)

    fathers = Sheep.objects.filter(
        farm=farm,
        sex="M",
        status="ACTIVE",
        birth_date__lte=father_min_birth_date
    )

    mother_breeds = {
        str(sheep.id): sheep.breed
        for sheep in mothers
    }

    father_breeds = {
        str(sheep.id): sheep.breed
        for sheep in fathers
    }

    if request.method == "POST":
        form = LambingForm(request.POST)
        form.fields["mother"].queryset = mothers
        form.fields["father_sheep"].queryset = fathers

        formset = LambFormSet(request.POST, queryset=Lamb.objects.none())

        if form.is_valid() and formset.is_valid():
            lambing = form.save(commit=False)

            try:
                lambing.save()
            except ValidationError as error:
                form.add_error(None, error)
                return render(request, "lambing/lambing_create.html", {
                    "form": form,
                    "formset": formset,
                    "mother_breeds": mother_breeds,
                    "father_breeds": father_breeds,
                })

            saved_lambs = 0

            for lamb_form in formset:
                if lamb_form.cleaned_data and lamb_form.cleaned_data.get("initial_tag"):
                    if saved_lambs < lambing.lamb_count:
                        lamb = lamb_form.save(commit=False)
                        lamb.lambing = lambing
                        lamb.save()
                        saved_lambs += 1

            if saved_lambs != lambing.lamb_count:
                lambing.delete()
                form.add_error(
                    "lamb_count",
                    "Broj unesene janjadi mora odgovarati odabranom broju janjadi."
                )
            else:
                lambing.mother.save()

                if lambing.father_sheep:
                    lambing.father_sheep.save()

                return redirect("lambing_detail", pk=lambing.pk)
    else:
        form = LambingForm()
        form.fields["mother"].queryset = mothers
        form.fields["father_sheep"].queryset = fathers

        formset = LambFormSet(queryset=Lamb.objects.none())

    return render(request, "lambing/lambing_create.html", {
        "form": form,
        "formset": formset,
        "mother_breeds": mother_breeds,
        "father_breeds": father_breeds,
    })


@login_required
def lambing_detail(request, pk):
    farm = get_user_farm(request.user)

    lambing = get_object_or_404(
        Lambing,
        pk=pk,
        mother__farm=farm
    )

    return render(request, "lambing/lambing_detail.html", {
        "lambing": lambing,
    })


@login_required
def lambing_delete(request, pk):
    farm = get_user_farm(request.user)

    lambing = get_object_or_404(
        Lambing,
        pk=pk,
        mother__farm=farm
    )

    if request.method == "POST":
        lambing.delete()
        return redirect("lambing_list")

    return render(request, "lambing/lambing_confirm_delete.html", {
        "lambing": lambing,
    })


@login_required
def lamb_list(request):
    farm = get_user_farm(request.user)

    lambs = Lamb.objects.none()

    if farm:
        six_months_ago = date.today() - timedelta(days=183)

        lambs = Lamb.objects.filter(
            lambing__mother__farm=farm
        ).filter(
            models.Q(official_tag="") |
            models.Q(lambing__lambing_date__gt=six_months_ago)
        ).select_related(
            "lambing",
            "lambing__mother",
            "converted_sheep"
        ).order_by("-lambing__lambing_date")

        query = request.GET.get("q")
        status = request.GET.get("status")

        if query:
            lambs = lambs.filter(
                models.Q(initial_tag__icontains=query) |
                models.Q(official_tag__icontains=query)
            )

        if status == "marked":
            lambs = lambs.exclude(official_tag="")

        if status == "unmarked":
            lambs = lambs.filter(official_tag="")

    return render(request, "lambing/lamb_list.html", {
        "farm": farm,
        "lambs": lambs,
    })


@login_required
def lamb_update(request, pk):
    farm = get_user_farm(request.user)

    lamb = get_object_or_404(
        Lamb,
        pk=pk,
        lambing__mother__farm=farm
    )

    if request.method == "POST":
        form = LambForm(request.POST, instance=lamb)

        if form.is_valid():
            form.save()
            return redirect("lamb_list")
    else:
        initial = {
            "official_tag": lamb.official_tag.replace("HR ", "") if lamb.official_tag else ""
        }

        form = LambForm(instance=lamb, initial=initial)

    return render(request, "lambing/lamb_update.html", {
        "form": form,
        "lamb": lamb,
    })