from urllib.parse import urlencode
from pydantic import BaseModel, field_validator
from common import make_request, BadRequestError, ForbiddenError, BadStatusCodeError


class ResponseMain(BaseModel):
    temp: float


class ResponseWeather(BaseModel):
    description: str


class Response(BaseModel):
    main: ResponseMain
    weather: list[ResponseWeather]

    @field_validator("weather")
    def validate_weather_not_empty(cls, v):
        if not v:
            raise ValueError("weather list must not be empty")
        return v

    @property
    def temp(self) -> float:
        return self.main.temp

    @property
    def description(self) -> str:
        return self.weather[0].description


if __name__ == "__main__":
    city = input("Enter city: ").strip()
    api_key = input("Enter API key: ").strip()

    if not city:
        raise ValueError("city is required")
    if not api_key:
        raise ValueError("API key is required")

    query = urlencode(
        {
            "q": city,
            "appid": api_key,
            "units": "metric",
        }
    )
    url = "https://api.openweathermap.org/data/2.5/weather?" + query
    try:
        response = make_request("GET", url)

        data = response.json()
        data_parsed = Response(**data)

        temp = data_parsed.temp
        description = data_parsed.description

        print(f"temperature: {temp}°c")
        print(f"description: {description}")
    except BadRequestError:
        print("request failed: Bad request")
    except ForbiddenError:
        print("request failed: Forbidden")
    except BadStatusCodeError as exc:
        print(f"request failed: Bad status code {exc.status_code}")
    except Exception as exc:
        print(f"request failed: {exc}")
