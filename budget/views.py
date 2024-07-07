from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from budget.models import Budget

@login_required
def budget(request):
    user = request.user
    budget = user.budget
    if not budget:
        budget = Budget.objects.create(owner=user)[0]
    data = {
        "revenues": budget.revenues(),
        "spents": budget.spents(),
        "total": budget.total()
    }

    return render(request, "budget/budget.html", data)
