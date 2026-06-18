from fastapi import FastAPI

app = FastAPI()

users = [
    {
        "id": 1,
        "name": "Jainam"
    }
]

@app.get("/health")
def health():
    return {
        "status": "UP"
    }

@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):

    for user in users:
        if user["id"] == user_id:
            return user

    return {
        "error": "User Not Found"
    }