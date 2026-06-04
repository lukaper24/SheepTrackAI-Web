from django.contrib.auth.decorators import login_required
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

    if request.method == "POST":
        form = LambingForm(request.POST)
        form.fields["mother"].queryset = Sheep.objects.filter(
            farm=farm,
            sex="Z"
        )

        formset = LambFormSet(request.POST, queryset=Lamb.objects.none())

        if form.is_valid() and formset.is_valid():
            lambing = form.save(commit=False)
            lambing.save()

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
                lambing.mother.category = "OVCA"
                lambing.mother.save()
                return redirect("lambing_detail", pk=lambing.pk)

    else:
        form = LambingForm()
        form.fields["mother"].queryset = Sheep.objects.filter(
            farm=farm,
            sex="Z"
        )

        formset = LambFormSet(queryset=Lamb.objects.none())

    return render(request, "lambing/lambing_create.html", {
        "form": form,
        "formset": formset,
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