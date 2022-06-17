import requests
import typer

def header():
    f = open("token.txt", "r")
    bearer_token = f.read()
    return {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        "Authorization": f"Bearer {bearer_token}"
    }
    
def check_response(response):
    if(not response.ok):
        if(response.status_code == 403):
            typer.echo(f"You nedd a token to use the application!\nUse the command 'token' to add one.")
        elif(response.status_code == 409):
            typer.echo(f"The tv show is already in the list.")
        else: typer.echo(f"Error: {response.status_code}")
        
        raise typer.Exit()

def get_response(url:str):
    response = requests.get(url, headers=header())
    check_response(response)
    return response.json()

def post_response(url:str):
    response = requests.post(url,  headers=header())
    if(not response.ok):
        check_response(response)
    return response.json()

def patch_response(url:str):
    response = requests.patch(url, headers=header())
    if(not response.ok):
        check_response(response)
    return response.json()

def delete_response(url:str):
    response = requests.delete(url,  headers=header())
    if(not response.ok):
        check_response(response)
    return response.json()