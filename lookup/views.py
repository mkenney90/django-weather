from datetime import date
from django.shortcuts import render

# Create your views here.


def home(request):
    import json
    import requests
    from datetime import datetime

    today = datetime.today().strftime("%Y-%m-%d")

    api_requests = requests.get(
        "https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode=29609&date="
        + today
        + "&distance=5&API_KEY=69EF95CC-A676-4E15-B053-47E847D99EC6"
    )

    try:
        api = json.loads(api_requests.content)
    except Exception as e:
        api = "error"

    if api[0]["Category"]["Name"] == "Good":
        category_color = "success"
    elif api[0]["Category"]["Name"] == "Moderate":
        category_color = "info"
    elif api[0]["Category"]["Name"] == "Unhealthy":
        category_color = "warning"
    else:
        category_color = "danger"

    return render(request, "home.html", {"api": api, "category_color": category_color})


def about(request):
    return render(request, "about.html", {})
