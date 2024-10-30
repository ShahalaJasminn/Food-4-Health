import requests
from django.conf import settings
def fetch_food_suggestions(dietary_preference, sugar_level=None, cholesterol_level=None):
    # Prepare the base search query based on dietary preference
    search_query = f"{dietary_preference} food"
    
    # Customize query based on sugar and cholesterol levels
    if sugar_level and sugar_level > 100:
        search_query += " low sugar"
    if cholesterol_level and cholesterol_level > 200:
        search_query += " low cholesterol"

    headers = {
        'x-app-id': settings.NUTRITIONIX_APP_ID,
        'x-app-key': settings.NUTRITIONIX_APP_KEY,
    }

    try:
        # Search for foods matching the customized query
        response = requests.get(
            f'https://trackapi.nutritionix.com/v2/search/instant?query={search_query}',
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            foods = data.get('branded', [])  # Get branded food items
            if foods:
                return [food['food_name'] for food in foods[:5]]  # Return top 5 suggestions
            else:
                return []
        else:
            return []

    except Exception as e:
        return []


def fetch_diet_plan(weight, height, dietary_preference, sugar_level, cholesterol_level):
    headers = {
        'x-app-id': settings.NUTRITIONIX_APP_ID,
        'x-app-key': settings.NUTRITIONIX_APP_KEY,
    }

    # Fetch food suggestions based on dietary preference
    query_foods = fetch_food_suggestions(dietary_preference, sugar_level, cholesterol_level)

    if not query_foods:
        query_foods = ['apple', 'milk']  # Fallback if no suggestions found

    # Create the query string
    query = ', '.join(query_foods) + f', {weight}kg, {height}cm'
    
    payload = {'query': query}

    try:
        response = requests.post(
            'https://trackapi.nutritionix.com/v2/natural/nutrients',
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('foods', [])
        else:
            return []

    except Exception as e:
        return []
