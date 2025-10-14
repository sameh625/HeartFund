from decimal import Decimal, InvalidOperation
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils.dateparse import parse_date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, Contribution
from .serializers import ProjectSerializer, ContributionSerializer

ORDERING_MAP = {
    "latest": "-id",
    "target_asc": "target",
    "target_desc": "-target",
    "raised_desc": "-raised",
    "raised_asc": "raised",
    "end_asc": "end_date",
    "end_desc": "-end_date",
}
def annotate_with_raised(queryset):
    return queryset.annotate(
        raised=Coalesce(
            Sum("contributions__amount", output_field=DecimalField(max_digits=12, decimal_places=2)),
            Value(0),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
    )

@login_required
def add_project_page(request):
    return render(request, "projects/add_project.html")

@login_required
def my_projects(request):
    return render(request, "projects/my_projects.html")


@api_view(["GET", "POST"])
def project_list_create_api(request):
    if request.method == "GET":
        order = request.GET.get("order", "latest")
        queryset = annotate_with_raised(Project.objects.all()).order_by(ORDERING_MAP.get(order, "-id"))
        serializer = ProjectSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def project_detail_api(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(ProjectSerializer(project, context={"request": request}).data)

    if project.owner != request.user:
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

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
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=status.HTTP_403_FORBIDDEN)
    projects = annotate_with_raised(Project.objects.filter(owner=request.user)).order_by("-id")
    serializer = ProjectSerializer(projects, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def search_projects_api(request):
    start_date = parse_date(request.GET.get("start"))
    end_date = parse_date(request.GET.get("end"))
    order = request.GET.get("order", "latest")

    if not start_date or not end_date:
        return Response({"error": "Invalid dates"}, status=status.HTTP_400_BAD_REQUEST)

    queryset = Project.objects.filter(
        start_date__gte=start_date,
        end_date__lte=end_date
    )
    queryset = annotate_with_raised(queryset)

    queryset = queryset.order_by(ORDERING_MAP.get(order, "-id"))

    serializer = ProjectSerializer(queryset, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET", "POST"])
def project_contributions_api(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        contributions = project.contributions.all()
        return Response(ContributionSerializer(contributions, many=True).data)

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=status.HTTP_403_FORBIDDEN)

    if project.owner_id == request.user.id:
        return Response({"detail": "You cannot contribute to your own project."}, status=status.HTTP_403_FORBIDDEN)

    
    raised = project.contributions.aggregate(total=Sum("amount", output_field=DecimalField(max_digits=12, decimal_places=2))).get("total") or Decimal("0")
    target = Decimal(str(project.target))
    if raised >= target:
        return Response({"detail": "This project is fully funded."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount_value = request.data.get("amount")
        amount = Decimal(str(amount_value))
        if amount <= 0:
            raise InvalidOperation
    except Exception:
        return Response({"amount": ["Enter a positive amount."]}, status=status.HTTP_400_BAD_REQUEST)

    if raised + amount > target:
        remaining = target - raised
        return Response({"amount": [f"Contribution exceeds project target. You can contribute up to {remaining}."]}, status=status.HTTP_400_BAD_REQUEST)

    contribution = Contribution.objects.create(project=project, donor=request.user, amount=amount)
    return Response(ContributionSerializer(contribution).data, status=status.HTTP_201_CREATED)
