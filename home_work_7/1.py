import requests


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        posts = response.json()
    except Exception as exc:
        print(f"Request failed: {exc}")
    else:
        for post in posts[:5]:
            title = post.get("title", "")
            body = post.get("body", "")
            print(f"title: {title}\nbody: {body}\n")
