from django.shortcuts import render
from .models import Hospital

def hospital_search_view(request):
    """
    View to handle hospital search and filtering.

    Accepts the following GET parameters:
        - treatment (str): Filter hospitals by treatment type (case-insensitive).
        - city (str): Filter by city.
        - country (str): Filter by country.
        - accreditation (str): Filter by accreditation.
        - min_cost (float): Minimum estimated cost.
        - max_cost (float): Maximum estimated cost.
        - sort_by (str): 'cost_asc' or 'cost_desc' to sort hospitals by cost.

    Returns:
        Rendered HTML page with a filtered list of hospitals and treatment types.
    """
    hospitals = Hospital.objects.all()

    treatment = request.GET.get("treatment")
    city = request.GET.get("city")
    country = request.GET.get("country")
    accreditation = request.GET.get("accreditation")
    min_cost = request.GET.get("min_cost")
    max_cost = request.GET.get("max_cost")
    sort_by = request.GET.get("sort_by")

    if treatment:
        hospitals = hospitals.filter(treatment_type__icontains=treatment)
    if city:
        hospitals = hospitals.filter(city__icontains=city)
    if country:
        hospitals = hospitals.filter(country__icontains=country)
    if accreditation:
        hospitals = hospitals.filter(accreditation__icontains=accreditation)
    if min_cost:
        hospitals = hospitals.filter(cost_estimate__gte=min_cost)
    if max_cost:
        hospitals = hospitals.filter(cost_estimate__lte=max_cost)
    if sort_by == "cost_asc":
        hospitals = hospitals.order_by("cost_estimate")
    elif sort_by == "cost_desc":
        hospitals = hospitals.order_by("-cost_estimate")

    treatment_types = Hospital.objects.values_list("treatment_type", flat=True).distinct()

    return render(request, "search.html", {
        "hospitals": hospitals,
        "treatment_types": treatment_types,
    })
