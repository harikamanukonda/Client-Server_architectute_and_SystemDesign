from fastapi import FastAPI
app = FastAPI()
users = {
    1:{"name":"Sam","role":"AI Engineer"},
    2:{"name":"Jyo","role":"Architect"}
}

@app.get("/")
def home():
    return{"message":"Client-Server architecture practice"}

@app.get("/users/{user_id}")
def get_user(user_id:int):
    if user_id in users:
        return users[user_id]
    return{"message":"user not found"}

@app.post("/users")
def create_users(name:str,role:str):
    new_user = len(users)+1
    users[new_user] = {"name":name,"role":role}
    return{"message":"new user created","user_id":new_user}