from datetime import date
from django.shortcuts import render
from requests import request

# Create your views here.


def home(request):
    zipcode = 29609

    if request.method == "POST":
        zipcode = request.POST["zipcode"]

    response = lookup(zipcode)

    if response == "error":
        return render(request, "home.html", {"response": "error"})
    elif response == "notfound":
        return render(request, "home.html", {"response": "notfound"})
    else:
        if response["aqi"][0]["Category"]["Name"] == "Good":
            category_color = "success"
        elif response["aqi"][0]["Category"]["Name"] == "Moderate":
            category_color = "info"
        elif response["aqi"][0]["Category"]["Name"] == "Unhealthy":
            category_color = "warning"
        else:
            category_color = "danger"

        return render(
            request,
            "home.html",
            {"response": response, "category_color": category_color},
        )


def about(request):
    return render(request, "about.html", {})


def lookup(zipcode):
    import json
    import requests
    from datetime import datetime

    today = datetime.today().strftime("%Y-%m-%d")
    api_requests = requests.get(
        "https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode="
        + str(zipcode)
        + "&date="
        + today
        + "&distance=5&API_KEY=69EF95CC-A676-4E15-B053-47E847D99EC6",
    )
    geo_requests = requests.get(
        "https://geocode.xyz/" + str(zipcode) + "?region=US&json=1"
    )
    try:
        api = json.loads(api_requests.content)
        geo = json.loads(geo_requests.content)
    except Exception as e:
        return "error"

    if len(api) == 0 or "error" in geo:
        return "notfound"

    if api != "error" and api != "notfound":
        latt = geo["latt"]
        long = geo["longt"]

        if float(latt) + float(long) == 0.0:
            return "notfound"

        zone_requests = requests.get(
            "https://api.weather.gov/points/" + latt + "," + long
        )
        print(zone_requests.status_code)

        try:
            zone = json.loads(zone_requests.content)
        except Exception as e:
            zone = "error"
            print("weather zone error")

        forecast_url = zone["properties"]["forecast"]

        weather_requests = requests.get(forecast_url)

        try:
            weather = json.loads(weather_requests.content)
        except Exception as e:
            weather = "error"

        response = {"aqi": api}

        if weather != "error":
            response["weather"] = weather

    return response
