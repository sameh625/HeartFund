from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils.dateparse import parse_date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project
from .serializers import ProjectSerializer

# ---------- Pages ----------
@login_required
def add_project_page(request):
    return render(request, "projects/add_project.html")

@login_required
def my_projects(request):
    return render(request, "projects/my_projects.html")


# ---------- APIs ----------
@api_view(["GET", "POST"])
def project_list_create_api(request):
    if request.method == "GET":
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def project_detail_api(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(ProjectSerializer(project).data)

    if project.owner != request.user:
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PUT":
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    project.delete()
    return Response({"message": "Project deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def user_projects_api(request):
    projects = Project.objects.filter(owner=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def search_projects_api(request):
    start_date = parse_date(request.GET.get("start"))
    end_date = parse_date(request.GET.get("end"))

    if not start_date or not end_date:
        return Response({"error": "Invalid dates"}, status=status.HTTP_400_BAD_REQUEST)

    projects = Project.objects.filter(
        start_date__gte=start_date,
        end_date__lte=end_date
    )

    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
