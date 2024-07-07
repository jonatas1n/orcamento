from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from budget.models import Budget

@login_required
def budget(request):
    user = request.user
    budget = user.budget
    if not budget:
        budget = Budget.objects.create(owner=user)
    return render(request, "budget.html", { "budget": budget })
