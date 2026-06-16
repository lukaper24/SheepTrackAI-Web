from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import re
from datetime import datetime

import pdfplumber
from farms.models import Farm
from .forms import SheepForm, SheepExitForm, SheepImportForm
from .models import Sheep


def get_user_farm(user):
    return Farm.objects.filter(owner=user).first()


@login_required
def sheep_list(request):
    farm = get_user_farm(request.user)

    sheep = Sheep.objects.none()

    if farm:
        sheep = Sheep.objects.filter(
            farm=farm,
            status='ACTIVE'
        ).order_by('eid_number')

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
@login_required
def sheep_archive(request):
    farm = get_user_farm(request.user)

    sheep = Sheep.objects.none()

    if farm:
        sheep = Sheep.objects.filter(
            farm=farm
        ).exclude(
            status='ACTIVE'
        ).order_by('-exit_date')

    return render(
        request,
        'sheep/sheep_archive.html',
        {
            'sheep': sheep
        }
    )
@login_required
def sheep_mark_exit(request, pk, status):
    farm = get_user_farm(request.user)

    animal = get_object_or_404(
        Sheep,
        pk=pk,
        farm=farm
    )

    allowed_statuses = ["SOLD", "DEAD", "SLAUGHTERED"]

    if status not in allowed_statuses:
        return redirect("sheep_detail", pk=animal.pk)

    if request.method == "POST":
        form = SheepExitForm(request.POST, instance=animal)

        if form.is_valid():
            animal = form.save(commit=False)
            animal.status = status
            animal.save()
            return redirect("sheep_archive")
    else:
        form = SheepExitForm(instance=animal)

    return render(request, "sheep/sheep_mark_exit.html", {
        "form": form,
        "animal": animal,
        "status": status,
    })

@login_required
def sheep_restore(request, pk):
    farm = get_user_farm(request.user)

    animal = get_object_or_404(
        Sheep,
        pk=pk,
        farm=farm
    )

    if request.method == "POST":
        animal.status = "ACTIVE"
        animal.exit_date = None
        animal.exit_reason = ""
        animal.save()

        return redirect("sheep_detail", pk=animal.pk)

    return render(request, "sheep/sheep_restore.html", {
        "animal": animal
    })

def map_breed(name):
    normalized = name.lower().strip()

    breed_map = {
        "cigaja": "CIGAJA",
        "creska": "CRESKA",
        "creska ovca": "CRESKA",
        "dalmatinska pramenka": "DALMATINSKA_PRAMENKA",
        "dubrovačka ovca": "DUBROVACKA_RUDA",
        "dubrovačka ovca – ruda": "DUBROVACKA_RUDA",
        "istarska ovca": "ISTARSKA",
        "krčka ovca": "KRCKA",
        "lička pramenka": "LICKA_PRAMENKA",
        "paška ovca": "PASKA",
        "rapska ovca": "RAPSKA",
        "istočnofrizijska ovca": "ISTOCNOFRIZIJSKA",
        "merinolandschaf": "MERINOLANDSCHAF",
        "merinolnadschaf": "MERINOLANDSCHAF",
        "romanovska ovca": "ROMANOVSKA",
        "solčavsko-jezerska": "SOLCAVSKO_JEZERSKA",
        "solcavsko-jezerska": "SOLCAVSKO_JEZERSKA",
        "solčavsko jezerska": "SOLCAVSKO_JEZERSKA",
        "suffolk": "SUFFOLK",
        "safolk": "SUFFOLK",
        "travnička pramenka": "TRAVNICKA_PRAMENKA",
        "vlašićka pramenka": "TRAVNICKA_PRAMENKA",
        "dubska pramenka": "TRAVNICKA_PRAMENKA",
        "dorper": "DORPER",
        "texel": "TEXEL",
        "teksel": "TEXEL",
        "kerry hill": "KERRY_HILL",
        "clun forest": "CLUN_FOREST",
        "kamerunska ovca": "KAMERUNSKA",
        "berrichon du cher": "BERRICHON_DU_CHER",
        "lacaune": "LACAUNE",
        "lakon": "LACAUNE",
    }

    return breed_map.get(normalized, "OSTALO")


@login_required
def sheep_import_eposjednik(request):
    farm = get_user_farm(request.user)

    if not farm:
        return redirect("farm_list")

    created_count = 0
    skipped_count = 0

    if request.method == "POST":
        form = SheepImportForm(request.POST, request.FILES)

        if form.is_valid():
            pdf_file = form.cleaned_data["pdf_file"]

            text = ""

            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            pattern = re.compile(
                r"\d+\s+"
                r"(HR\s+\d{9})\s+"
                r"(DA|NE)\s+"
                r"(?:(?:Bolus|El\.\s*markica)\s+)?"
                r"(\d{2}\.\d{2}\.\d{4}\.)\s+"
                r"([ZM])\s+"
                r"([A-Za-zČĆŽŠĐčćžšđ\- ]+)"
            )

            for line in text.splitlines():
                line = line.strip()

                match = pattern.search(line)

                if not match:
                    continue

                eid_number = match.group(1)
                birth_date_text = match.group(3)
                sex = match.group(4)
                breed_name = match.group(5).strip()

                birth_date = datetime.strptime(
                    birth_date_text,
                    "%d.%m.%Y."
                ).date()

                breed = map_breed(breed_name)

                animal, created = Sheep.objects.get_or_create(
                    eid_number=eid_number,
                    defaults={
                        "farm": farm,
                        "breed": breed,
                        "sex": sex,
                        "birth_date": birth_date,
                        "notes": "Uvezeno iz e-Posjednik PDF popisa.",
                    }
                )

                if created:
                    created_count += 1
                else:
                    skipped_count += 1

            return render(request, "sheep/sheep_import.html", {
                "form": form,
                "created_count": created_count,
                "skipped_count": skipped_count,
                "import_done": True,
            })

    else:
        form = SheepImportForm()

    return render(request, "sheep/sheep_import.html", {
        "form": form,
        "import_done": False,
    })