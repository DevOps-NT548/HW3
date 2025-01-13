from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Expression(BaseModel):
    expression: str

class Result(BaseModel):
    result: str

@app.post("/evaluate", response_model=Result)
def evaluate_expression(expression: Expression):
    try:
        expr = expression.expression.replace('＊', '*').replace('−', '-').replace('＋', '+').replace('÷', '/')
        while '^2' in expr:
            pos = expr.rfind('^2')
            start_pos = pos - 1
            while start_pos > 0 and expr[start_pos].isdigit() or expr[start_pos] in '.':
                start_pos -= 1
            start_pos += 1
            before_power = expr[start_pos:pos]
            expr = expr[:start_pos] + f"({before_power})**2" + expr[pos + 2:]
        result = str(eval(expr))
        return Result(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid expression")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Calculator"}