import httpx
from app.domain.models import WeatherAlertResponse


async def fetch_active_alerts() -> WeatherAlertResponse:
    from app.helpers.alert_filter import filter_alerts_by_string
    api_url = "https://apiprevmet3.inmet.gov.br/avisos/ativos"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()

            raw_body = response.text.strip()
            if not raw_body:
                return WeatherAlertResponse()

            filtered = filter_alerts_by_string(response.json(), "metropolitana do rio de janeiro")
            return WeatherAlertResponse.model_validate(filtered)


            

    except httpx.HTTPStatusError as e:
        print(f"Weather API error: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"Network error: {e}")
    except ValueError as e:
        # pega JSON inválido
        print(f"Invalid JSON from API: {e}")

    return WeatherAlertResponse()
