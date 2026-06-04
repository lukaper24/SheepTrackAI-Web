from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import FarmForm
from .models import Farm


@login_required
def farm_list(request):

    farm = Farm.objects.filter(
        owner=request.user
    ).first()

    return render(
        request,
        'farms/farm_list.html',
        {
            'farm': farm
        }
    )

@login_required
def farm_create(request):

    if Farm.objects.filter(owner=request.user).exists():
        return redirect('farm_list')

    if request.method == 'POST':
        form = FarmForm(request.POST)

        if form.is_valid():
            farm = form.save(commit=False)
            farm.owner = request.user
            farm.save()

            return redirect('farm_list')

    else:
        form = FarmForm()

    return render(
        request,
        'farms/farm_create.html',
        {'form': form}
    )