from django.urls import path
from . import views

app_name = "budget"

urlpatterns = [
    path('', views.AddProjectView.as_view(), name="add"),
    path('<slug:project_slug>/', views.project_details, name="project_details"),
    path('confirm/<int:pk>/<slug:project_slug>', views.confirm_page, name="confirm_page")
]