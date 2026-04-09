import httpx
from app.domain.models import NearbyStationWeatherResponse
from app.core.config import settings


async def fetch_nearby_station_weather() -> NearbyStationWeatherResponse:
    api_url = settings.PREVMET_API_URL

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()

            raw_body = response.text.strip()
            print(f"Raw response body: {raw_body}...")  # Log the first 200 characters for debugging
            if not raw_body:
                raise ValueError("Nearby station API returned an empty response body")

        return NearbyStationWeatherResponse.model_validate(response.json())


            

    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Nearby station API error: {e.response.status_code}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Nearby station network error: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"Nearby station invalid data: {e}") from e





