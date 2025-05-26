from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import random
import os

app = FastAPI()

# CORS pour les requêtes API (utile si tu testes encore depuis localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route API
@app.get("/api/math")
def get_math_exercises(
    operations: list[str] = Query(["add"]),
    count: int = 10,
    digits: str = "1-10"
):
    # Fonction utilitaire
    def parse_digits_param(digits: str):
        try:
            if '-' in digits:
                start, end = map(int, digits.split('-'))
                return list(range(start, end + 1))
            elif ',' in digits:
                return list(map(int, digits.split(',')))
            else:
                return [int(digits)]
        except:
            return list(range(1, 10))

    pool = parse_digits_param(digits)
    fallback = list(range(1, 11))
    exercises = []

    for _ in range(count):
        op = random.choice(operations)
        fixed = random.choice(pool)
        other = random.choice(fallback)

        if random.choice([True, False]):
            a, b = fixed, other
        else:
            a, b = other, fixed

        if op == "add":
            question = f"{a} + {b}"
            answer = a + b
        elif op == "sub":
            question = f"{a} - {b}"
            answer = a - b
        elif op == "mul":
            question = f"{a} × {b}"
            answer = a * b
        elif op == "div":
            b = random.choice(pool)
            result = random.choice(pool)
            a = b * result
            question = f"{a} ÷ {b}"
            answer = result
        else:
            continue

        exercises.append({"question": question, "answer": answer})
    return {"exercises": exercises}

# Servir le frontend buildé (Vite)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

