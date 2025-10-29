# yourapp/forms.py
from allauth.account.forms import SignupForm
from django import forms
from expenses.models import Transaction, Category

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect()
    )
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    class Meta:
        model = Transaction
        fields = (
            'type',
            'amount',
            'date',
            'category',       
        )
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

        