import requests
from django.conf import settings


def fetch_nutrition_details_from_nutritionix(meal_name):
    api_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'x-app-id': settings.NUTRITIONIX_APP_ID,
        'x-app-key': settings.NUTRITIONIX_APP_KEY,
        'Content-Type': 'application/json',
    }
    payload = {"query": meal_name}

    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json().get('foods', [{}])[0]
        return {
            'calories': data.get('nf_calories'),
            'fat': data.get('nf_total_fat'),
            'cholesterol': data.get('nf_cholesterol'),
            'protein': data.get('nf_protein'),
            'carbohydrates': data.get('nf_total_carbohydrate'),
        }
    return None
