from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.urls import reverse
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    budget = models.IntegerField(validators=[MinValueValidator(1)])
    date_created = models.DateTimeField(auto_now_add=True)
    
    # Slugify The Name Of The Project When Saving The Project.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('budget:project_details', kwargs={'project_slug': self.slug})

    def budget_left(self):
        project_expenses = Expense.objects.filter(project=self)
        expense_val = 0
        for expense in project_expenses:
            expense_val += expense.amount
        
        budget_left = self.budget - expense_val

        return budget_left


    def total_transactions(self):
        expenses_count = Expense.objects.filter(project=self).count()
        return expenses_count


class Category(models.Model):
    category = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title