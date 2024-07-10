import json
import urllib.request
from django.shortcuts import render

def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city', '')
        api_key = "cdbe173e423ca6ed6a6f08b2d90ff866"
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        try:
            response = urllib.request.urlopen(url).read()
            json_data = json.loads(response)
            data = {
                "name": str(json_data["name"]),
                "country_code": str(json_data["sys"]["country"]), 
                "temperature": str(json_data["main"]["temp"]), 
                "pressure": str(json_data["main"]["pressure"]),
                "humidity": str(json_data["main"]["humidity"])
            }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                data = {"error": "City not found. Please enter a valid city name."}
            else:
                data = {"error": f"HTTP Error: {e.reason}"}
        except urllib.error.URLError as e:
            data = {"error": f"URL Error: {e.reason}"}
        except json.JSONDecodeError:
            data = {"error": "Error parsing the weather data. Please try again later."}
        except Exception as e:
            data = {"error": f"An unexpected error occurred: {str(e)}"}
    
    return render(request, 'index.html', {"data": data})
