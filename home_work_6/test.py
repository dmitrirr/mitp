from fastapi.testclient import TestClient

from home_work_6.app import app


client = TestClient(app)


def test_basic_operations():
    r = client.post("/add", json={"a": 2, "b": 3})
    assert r.status_code == 200
    assert r.json()["result"] == 5

    r = client.post("/subtract", json={"a": 10, "b": 4})
    assert r.status_code == 200
    assert r.json()["result"] == 6

    r = client.post("/multiply", json={"a": 7, "b": 6})
    assert r.status_code == 200
    assert r.json()["result"] == 42

    r = client.post("/divide", json={"a": 20, "b": 5})
    assert r.status_code == 200
    assert r.json()["result"] == 4


def test_divide_by_zero_error():
    r = client.post("/divide", json={"a": 1, "b": 0})
    assert r.status_code == 400
    assert r.json()["detail"] == "division by zero"


def test_expression_build_and_eval():
    client.post("/expr/clear")

    r = client.post("/expr/create", json={"a": 1, "op": "+", "b": 2, "wrap": True})
    assert r.status_code == 200
    assert r.json()["expression"] == "(1 + 2)"

    r = client.post(
        "/expr/append",
        json={"combine_op": "*", "a": 3, "op": "*", "b": 4, "wrap": False},
    )
    assert r.status_code == 200
    assert r.json()["expression"] == "(1 + 2) * 3 * 4"

    r = client.post("/expr/eval")
    assert r.status_code == 200
    body = r.json()
    assert body["expression"] == "(1 + 2) * 3 * 4"
    assert body["result"] == 36.0


def test_expression_from_string_and_eval():
    expr = "-(1+2)*3 + (7 - 4)/(10 - 8)"
    r = client.post("/expr/from_string", json={"expression": expr})
    assert r.status_code == 200
    assert r.json()["expression"] == expr

    r = client.post("/expr/eval")
    assert r.status_code == 200
    body = r.json()
    assert body["expression"] == expr
    assert body["result"] == -7.5


def test_invalid_expression():
    expr = "(1+) * 2"
    r = client.post("/expr/from_string", json={"expression": expr})
    assert r.status_code == 200
    assert r.json()["expression"] == expr

    r = client.post("/expr/eval")
    assert r.status_code == 400
    assert r.json()["detail"] == "invalid expression"
