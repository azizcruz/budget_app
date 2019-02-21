from django import forms
from .models import Expense, Project


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('title', 'amount', 'category')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "budget")