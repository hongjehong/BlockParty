from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .models import Party, Participate
from .forms import PartyForm, ParticipateForm

# Create your views here.
@require_http_methods(['GET', 'POST'])
def index(request):
    partys = Party.objects.all()
    context = {
        'partys': partys,
    }
    return render(request, 'blocks/index.html', context)


@login_required
@require_http_methods(['POST', 'GET'])
def create(request):
    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            party = form.save(commit=False)
            party.user = request.user
            party.save()
            return redirect('blocks:index')
    else:
        form = PartyForm()
    context = {
        'form': form,
    }
    return render(request, 'blocks/create.html', context)


@login_required
@require_POST
def delete(request, party_pk):
    party = Party.objects.get(pk=party_pk)
    party.delete()
    return redirect('blocks:index')

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, party_pk):
    if request.method == "POST":
        party = Party.objects.get(pk=party_pk)
        party_form = PartyForm(request.POST, instance=party)
        if party_form.is_valid():
            party_edit = party_form.save(commit=False)
            party_edit.user = request.user
            party_edit.save()
            return redirect('blocks:detail', party.pk)

    else: 
        party = Party.objects.get(pk=party_pk)
        party_form = PartyForm(instance=party)
    context = {
        'party_form': party_form,
    }
    return render(request, 'blocks/update.html', context)


@require_http_methods(['GET', 'POST'])
def detail(request, party_pk):
    party = get_object_or_404(Party, pk=party_pk)
    # participates = Participate.objects.filter(party=party)
    participates = party.participate_set.all()
    participate_form = ParticipateForm()
    context = {
        'party': party,
        'participates': participates,
        'participate_form': participate_form,
    }
    return render(request, 'blocks/detail.html', context)


@login_required
@require_POST
def participate(request, party_pk):
    party = get_object_or_404(Party, pk=party_pk)
    form = ParticipateForm(request.POST)
    if form.is_valid():
        participate_form = form.save(commit=False)
        participate_form.party = party
        participate_form.user = request.user
        participate_form.save()
    
    return redirect('blocks:detail', party.pk)


@login_required
@require_POST
def participate_delete(request, party_pk, participate_pk):
    participate = get_object_or_404(Participate, party=party_pk, pk=participate_pk)
    participate.delete()
    return redirect('blocks:detail', party_pk)