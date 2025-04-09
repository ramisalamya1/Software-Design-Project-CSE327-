from django.shortcuts import render
from hospital_search.models import Hospital
from .models import HospitalStats


def compare_hospitals_view(request):
    """
    Display a comparison view for selected hospitals.

    :param request: Django HTTP request with optional `ids` query param (comma-separated hospital IDs).
    :return: Rendered comparison template with hospitals, their stats, and system recommendation.

    Query Parameters:
        - ids (str): Comma-separated hospital IDs to compare.

    Template Context:
        - hospitals (QuerySet): Selected hospitals to compare.
        - stats_map (dict): Mapping of hospital IDs to their HospitalStats.
        - recommended (Hospital): Best option based on recovery rate and cost efficiency.
    """
    ids = request.GET.get("ids")
    hospitals = []
    stats_map = {}
    recommended = None

    if ids:
        id_list = [int(i) for i in ids.split(",") if i.isdigit()]
        hospitals = Hospital.objects.filter(id__in=id_list)
        stats_map = {
            stat.hospital.id: stat
            for stat in HospitalStats.objects.filter(hospital__in=hospitals)
        }

        if hospitals:
            recommended = max(
                hospitals,
                key=lambda h: (
                    stats_map[h.id].recovery_rate / h.cost_estimate
                    if h.id in stats_map and h.cost_estimate > 0 else 0
                )
            )

        # Optional: sort hospitals by name
        hospitals = sorted(hospitals, key=lambda h: h.name)

    return render(request, "hospital_comparison/compare.html", {
        "hospitals": hospitals,
        "stats_map": stats_map,
        "recommended": recommended
    })
