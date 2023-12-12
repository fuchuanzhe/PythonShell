# uvicorn app:app --reload
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import docker
import datetime

app = FastAPI()

class Session:
    def __init__(self, ip: str):
        self.ip = ip
        self.previous_commands = []
        self.previous_results = []

    def get_prev_connected(self):
        if len(self.previous_commands) == 0:
            return ""
        elif len(self.previous_commands) == 1:
            return self.previous_commands[0]
        return '; '.join(self.previous_commands).strip()
    
    def get_history(self):
        str_builder = ""
        for i in range(len(self.previous_commands)):
            str_builder += ">>> " + self.previous_commands[i] + "\n"
            str_builder += self.previous_results[i] + "\n"
        return str_builder
    
    def execute(self, command: str):
        docker_client = docker.from_env()
        docker_command = f"/comp0010/sh -w '{self.get_prev_connected()}' '{command}'"
        container = docker_client.containers.run("shell", 
                                                 docker_command).decode('utf-8')
        print(container)
        result = container
        self.previous_commands.append(command)
        self.previous_results.append(result)
        return result

class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def get_session(self, ip: str):
        if ip not in self.sessions:
            self.sessions[ip] = Session(ip)
        return self.sessions[ip]
    
    def create_session(self, ip: str):
        self.sessions[ip] = Session(ip)
    
    def delete_session(self, ip: str):
        del self.sessions[ip]
    

session_manager = SessionManager()


@app.get("/")
def read_root():
    # return index.html
    with open('index.html', 'r') as f:
        return HTMLResponse(f.read())

@app.get("/get-ip")
def get_ip(request: Request):
    return {"ip": request.client.host}

@app.get("/get-history")
def get_history(request: Request):
    ip = request.client.host
    session = session_manager.get_session(ip)
    return {"history": session.get_history()}

class Command(BaseModel):
    command: str

@app.post("/execute")
def execute(request: Request, command: Command):
    print(command.command)
    ip = request.client.host
    session = session_manager.get_session(ip)
    return {"result": session.execute(command.command.strip())}

@app.get("/reset")
def reset(request: Request):
    ip = request.client.host
    session_manager.delete_session(ip)
    return {"status": "success"}