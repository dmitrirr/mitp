from pydantic import BaseModel
from common import make_request, BadRequestError, ForbiddenError, BadStatusCodeError


class Post(BaseModel):
    title: str
    body: str


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        response = make_request("GET", url)
        response_json = response.json()

        num_posts_to_parse = 5

        posts = [Post(**post) for post in response_json[:num_posts_to_parse]]
        for i, post in enumerate(posts):
            print(f"post {i + 1}:")
            print(f"title: {post.title}")
            print(f"body: {post.body}")
            print()
    except BadRequestError:
        print("Request failed: Bad request")
    except ForbiddenError:
        print("Request failed: Forbidden")
    except BadStatusCodeError as exc:
        print(f"Request failed: Bad status code {exc.status_code}")
    except Exception as exc:
        print(f"Request failed: {exc}")
