from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

AEROBOTICS_API_URL = "https://api.aerobotics.com/farming/surveys/"
HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer 5d03db72854d43a8ce0c63e0d4fb4a261bc29b95ea46b541f537dbf0891b45d6"
}

def get_tree_surveys():
    #orchard_ID = input('Enter Orchard ID: ')
    orchard_ID = 216269
    survey_ID = requests.get(AEROBOTICS_API_URL + "?orchard_id=" + str(orchard_ID), headers=HEADERS).json().get("results")[0].get("id")
    response = requests.get(AEROBOTICS_API_URL + str(survey_ID) + "/tree_surveys/", headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Aerobotics API")

    results = response.json().get("results", [])
    filtered_results = [x for x in results if x.get("ndre", 0) < 0.45]
    return filtered_results

@app.get("/orchards/216269/missing-trees/")
def missing_trees():
    missing_trees_response = get_tree_surveys()
    latLng = []
    for tree in missing_trees_response:
        lat = tree.get("lat")
        lng = tree.get("lng")
        latLng.append({"lat": lat, "lng": lng})
    return {"Missing Trees": latLng}

print(missing_trees())
