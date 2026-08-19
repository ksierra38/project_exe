import requests
from fastapi import FastAPI, HTTPException, Path, status

# app = FastAPI()

# @app.get("/")
# async def index():
#    return {"message": "Hello World"}

# import requests
# @app.post("/convert/{state}/{city}")
# def convert(state, city):
#    print(f"Converting {city}, {state} to lat/long")
#    lat, long  = None, None
#    api_key = "6a7f57138e04b429290986wxia11d90"
#    payload = {"api_key": api_key, "state": state, "city": city}
#    try:
#     response = requests.get("https://geocode.maps.co/search", params=payload)
#     response.raise_for_status()
#    except Execution as e:
#      raise exeptionpip.HTTPExeption


app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.post("/convert/{state}/{city}")
def convert(
    state: str = Path(..., min_length=2, max_length=50, description="State abbreviation or name"),
    city: str = Path(..., min_length=1, max_length=100, description="City name")
):
    # Validate non-empty/non-whitespace inputs
    clean_state = state.strip()
    clean_city = city.strip()
    
    if not clean_state or not clean_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="State and City parameters cannot be empty or whitespace."
        )

    print(f"Converting {clean_city}, {clean_state} to lat/long")
    
    api_key = "6a7f57138e04b429290986wxia11d90"
    payload = {
        "api_key": api_key, 
        "state": clean_state, 
        "city": clean_city
    }
    
    try:
        # Include a timeout parameter so the call doesn't hang indefinitely
        response = requests.get("https://geocode.maps.co/search", params=payload, timeout=5.0)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The external geocoding service timed out."
        )
    except requests.exceptions.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"External API error: {e.response.status_code}"
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to reach the geocoding service."
        )

    data = response.json()

    if not data or not isinstance(data, list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No latitude/longitude found for '{clean_city}, {clean_state}'."
        )

    # Extract coordinates from the first matching result
    lat = data[0].get("lat")
    long = data[0].get("lon")

    return {
        "city": clean_city,
        "state": clean_state,
        "latitude": lat,
        "longitude": long
    }