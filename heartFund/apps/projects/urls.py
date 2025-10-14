from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # API endpoints
    path("api/", views.project_list_create_api, name="project_list_create_api"),
    path("api/<int:pk>/", views.project_detail_api, name="project_detail_api"),
    path("api/<int:pk>/contributions/", views.project_contributions_api, name="project_contributions_api"),
    path("api/mine/", views.user_projects_api, name="user_projects_api"),
    path("api/search/", views.search_projects_api, name="search_projects_api"),

    # Frontend pages
    path("add/", views.add_project_page, name="add_project"),
    path("mine/", views.my_projects, name="my_projects"),
]


# GET /projects/api/ → all projects # type: ignore
# POST /projects/api/ → create project (must be logged in)
# GET /projects/api/<id>/ → view single project
# PUT /projects/api/<id>/ → update project (only if owner)
# DELETE /projects/api/<id>/ → delete project (only if owner)
# GET /projects/api/mine/ → list projects owned by logged-in user
# GET /projects/api/search/?start=2025-09-01&end=2025-09-30 → search projects by date range