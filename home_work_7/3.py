from pydantic import BaseModel
from common import make_request, BadRequestError, ForbiddenError, BadStatusCodeError


class RequestBody(BaseModel):
    title: str
    body: str
    user_id: int


class ResponseBody(BaseModel):
    id: int
    title: str
    body: str
    user_id: int


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts"
    request_body = RequestBody(title="Test Post", body="This is a test post", user_id=1)

    try:
        response = make_request("POST", url, request_body.model_dump())

        response_json = response.json()
        response_parsed = ResponseBody(**response_json)

        print("created post:")
        print(f"id: {response_parsed.id}")
        print(f"title: {response_parsed.title}")
        print(f"body: {response_parsed.body}")
        print(f"user_id: {response_parsed.user_id}")
    except BadRequestError:
        print("request failed: Bad request")
    except ForbiddenError:
        print("request failed: Forbidden")
    except BadStatusCodeError as exc:
        print(f"request failed: Bad status code {exc.status_code}")
    except Exception as exc:
        print(f"request failed: {exc}")
