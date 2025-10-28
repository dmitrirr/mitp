from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import ast
import operator
from typing import Any, Dict, Union


app = FastAPI(title="Calculator API", version="1.0.0")


class BinaryOpRequest(BaseModel):
    a: float
    b: float


class CreateExprRequest(BaseModel):
    a: Union[int, float, str]
    op: str = Field(pattern=r"^[+\-*/]$")
    b: Union[int, float, str]
    wrap: bool = False


class AppendExprRequest(BaseModel):
    combine_op: str = Field(pattern=r"^[+\-*/]$")
    a: Union[int, float, str]
    op: str = Field(pattern=r"^[+\-*/]$")
    b: Union[int, float, str]
    wrap: bool = False


class ExprStringRequest(BaseModel):
    expression: str


class EvaluateResponse(BaseModel):
    expression: str
    result: float


class ExpressionStore:
    def __init__(self) -> None:
        self._expression: str = ""

    @property
    def expression(self) -> str:
        return self._expression

    def set_expression(self, expr: str) -> str:
        self._expression = expr
        return self._expression

    def clear(self) -> None:
        self._expression = ""

    def create_binary(self, a: Union[int, float, str], op: str, b: Union[int, float, str], wrap: bool) -> str:
        part = f"{a} {op} {b}"
        if wrap:
            part = f"({part})"
        self._expression = part
        return self._expression

    def append_binary(self, combine_op: str, a: Union[int, float, str], op: str, b: Union[int, float, str], wrap: bool) -> str:
        if not self._expression:
            self._expression = self.create_binary(a, op, b, wrap)
            return self._expression
        part = f"{a} {op} {b}"
        if wrap:
            part = f"({part})"
        self._expression = f"{self._expression} {combine_op} {part}"
        return self._expression


store = ExpressionStore()


class DivisionByZeroError(Exception):
    pass


class InvalidExpressionError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


def _safe_eval(expr: str) -> float:
    allowed_binops: Dict[type, Any] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def eval_node(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.BinOp):
            if type(node.op) not in allowed_binops:
                raise UnsupportedOperatorError()
            left = eval_node(node.left)
            right = eval_node(node.right)
            op_fn = allowed_binops[type(node.op)]
            return op_fn(left, right)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            val = eval_node(node.operand)
            return +val if isinstance(node.op, ast.UAdd) else -val
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        raise InvalidExpressionError()

    try:
        parsed = ast.parse(expr, mode="eval")
        return float(eval_node(parsed))
    except ZeroDivisionError:
        raise DivisionByZeroError()
    except Exception:
        raise InvalidExpressionError()


@app.post("/add")
def add(req: BinaryOpRequest) -> Dict[str, float]:
    return {"result": req.a + req.b}


@app.post("/subtract")
def subtract(req: BinaryOpRequest) -> Dict[str, float]:
    return {"result": req.a - req.b}


@app.post("/multiply")
def multiply(req: BinaryOpRequest) -> Dict[str, float]:
    return {"result": req.a * req.b}


@app.post("/divide")
def divide(req: BinaryOpRequest) -> Dict[str, float]:
    if req.b == 0:
        raise HTTPException(status_code=400, detail="division by zero")
    return {"result": req.a / req.b}


@app.post("/expr/create")
def expr_create(req: CreateExprRequest) -> Dict[str, str]:
    expr = store.create_binary(req.a, req.op, req.b, req.wrap)
    return {"expression": expr}


@app.post("/expr/append")
def expr_append(req: AppendExprRequest) -> Dict[str, str]:
    expr = store.append_binary(req.combine_op, req.a, req.op, req.b, req.wrap)
    return {"expression": expr}


@app.post("/expr/from_string")
def expr_from_string(req: ExprStringRequest) -> Dict[str, str]:
    store.set_expression(req.expression)
    return {"expression": store.expression}


@app.get("/expr")
def expr_get() -> Dict[str, str]:
    return {"expression": store.expression}


@app.post("/expr/eval", response_model=EvaluateResponse)
def expr_eval() -> EvaluateResponse:
    if not store.expression:
        raise HTTPException(status_code=400, detail="empty expression")
    try:
        result = _safe_eval(store.expression)
    except DivisionByZeroError:
        raise HTTPException(status_code=400, detail="division by zero")
    except UnsupportedOperatorError:
        raise HTTPException(status_code=400, detail="unsupported operator")
    except InvalidExpressionError:
        raise HTTPException(status_code=400, detail="invalid expression")
    return EvaluateResponse(expression=store.expression, result=result)


@app.post("/expr/clear")
def expr_clear() -> Dict[str, str]:
    store.clear()
    return {"expression": store.expression}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("home_work_6.app:app", host="0.0.0.0", port=8000, reload=False)


