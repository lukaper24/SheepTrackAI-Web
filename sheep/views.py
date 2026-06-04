from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from farms.models import Farm
from .forms import SheepForm
from .models import Sheep


@login_required
def sheep_list(request):
    farm = Farm.objects.filter(owner=request.user).first()

    sheep = Sheep.objects.none()

    if farm:
        sheep = Sheep.objects.filter(farm=farm).order_by('eid_number')

    return render(
        request,
        'sheep/sheep_list.html',
        {
            'farm': farm,
            'sheep': sheep
        }
    )


@login_required
def sheep_create(request):
    farm = Farm.objects.filter(owner=request.user).first()

    if not farm:
        return redirect('farm_list')

    if request.method == 'POST':
        form = SheepForm(request.POST)

        if form.is_valid():
            sheep = form.save(commit=False)
            sheep.farm = farm
            sheep.save()

            return redirect('sheep_list')
    else:
        form = SheepForm()

    return render(
        request,
        'sheep/sheep_create.html',
        {
            'form': form
        }
    )