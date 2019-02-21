from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Expense, Project, Category
from django.views.generic import CreateView, ListView
from django.contrib import messages
from .forms import ExpenseForm, ProjectForm
from django.db import IntegrityError

# Create your views here.

def project_details(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    categories = Category.objects.all()

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            Expense.objects.create(
                project=project,
                title=title,
                amount=amount,
                category= get_object_or_404(Category, category=category_name)
            ).save

            return redirect(project.get_absolute_url())




    form = ExpenseForm()
    context = {
        'project': project,
        'expenses': project.expenses.all(),
        'form': form,
    }
    return render(request, 'budget/detail_project.html', context)

def confirm_page(request, pk, project_slug):
    expense = get_object_or_404(Expense, pk=pk)
    project = get_object_or_404(Project, slug=project_slug)

    if request.method == "POST":
        delete = int(request.POST.get("delete"))
        if delete:
            expense.delete()
            messages.success(request, "Expense was deleted.")
            return redirect(project.get_absolute_url())
        else:
            return redirect(project.get_absolute_url())

        
    
    context = {
        'expense':expense
    }
    return render(request, 'budget/are_you_sure.html', context)

class ListProjects(ListView):
    model = Project
    template_name = "budget/list_projects.html"
    context_object_name = 'projects'
    extra_context = {
        "form": ProjectForm
    }

class AddProjectView(CreateView):
    model = Project
    template_name = 'budget/list_projects.html'
    fields = ('name', 'budget')
    success_url = '/'

    def form_valid(self, form):
        try:
            if(super().form_valid(form)):
                messages.success(self.request, "A project was added")
                return super().form_valid(form)
        except IntegrityError as e:
            messages.warning(self.request, "Project name exists. Try another.")
            return redirect("/")