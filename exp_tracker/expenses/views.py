from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Transaction
from expenses.filters import TransactionFilter


def index(request):
    return render(request, 'expenses/index.html')


@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET, 
        queryset=Transaction.objects.filter(user=request.user).select_related('category'))
    context= {'filter': transaction_filter}
    if request.htmx:
        return render(request, 'expenses/partial/transactions-container.html', context)
    return render(request, 'expenses/transactions-list.html', context)

