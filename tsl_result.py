import json
from requests import request
import typer
import tsl_endpoints
import api_response
import requests

QUIT = "q"
NEXT_PAGE = "n"
PREVIOUS_PAGE = "p"
ADVANCED_SEARCH = "adv"

DELETE = "del"
EDIT = "edit"
SHOW = "v"

def search_result(tv_show_name: str, response : dict, advanced):
    # TV show list
    results = response['results']

    # Pagination information
    current_page =  int(response['page'])
    last_page =  int(response['total_pages'])

    typer.echo(f"Page {current_page}/{last_page}")

    for index, tv_show in enumerate(results, 0):
        typer.echo(f"{index+1} : {tv_show['name']}")
    
    try:
        while True:
            typer.echo(f"\nSelect title id \ntype {QUIT} to quit")

            if current_page != last_page:
                typer.echo(f"type {NEXT_PAGE} for the next page")
            if current_page > 1:
                typer.echo(f"type {PREVIOUS_PAGE} for the previous page")
            if not advanced and current_page == last_page:
                typer.echo(f"type {ADVANCED_SEARCH} for an advanced search")
            
            id = typer.prompt(">>>")
            
            if id == QUIT or id == QUIT.upper():
                raise typer.Abort()
            elif current_page != last_page and (id == NEXT_PAGE or id == NEXT_PAGE.upper()):
                response = api_response.get_response(
                    tsl_endpoints.search_tv_show(tv_show_name, current_page+1, advanced))

                series_id = search_result(tv_show_name, response, advanced)
                break
            elif current_page > 1 and (id == PREVIOUS_PAGE or id == PREVIOUS_PAGE.upper()):
                response = api_response.get_response(
                    tsl_endpoints.search_tv_show(tv_show_name, current_page-1, advanced))

                series_id = search_result(tv_show_name, response, advanced)
                break
            elif not advanced and current_page == last_page and (
                id == ADVANCED_SEARCH or id == ADVANCED_SEARCH.upper()):
                response = api_response.get_response(
                    tsl_endpoints.search_tv_show(tv_show_name, adv=True))
                series_id = search_result(tv_show_name, response, True)
                
                break
            else:
                try:
                    id = int(id)-1

                    if id >= 0 and id < len(results):
                        series_id = results[id]['id']
                        break
                    typer.echo("Invalid ID")
                except Exception:
                    typer.echo("Invalid input")
    except typer.Abort:
        typer.echo("No TV series added")
        raise typer.Exit()
        
    return series_id

def tv_show_details_result(response : dict):
    for label in response:
        typer.echo("{:<24} {:<3}".format(label+":", response[label]))

def add_tv_show_result(id: int):
    try:
        while True:
            typer.echo(f"Set priority [1 to 5]\ntype {QUIT} to quit")
            priority = typer.prompt(">>>")
            if priority == QUIT or priority == QUIT.upper():
                raise typer.Abort()
            else:
                try:
                    priority = int(priority)

                    if priority > 0 and priority <= 5:
                        break
                    typer.echo("Invalid number")
                except Exception:
                    typer.echo("Invalid input")
    except typer.Abort:
        typer.echo("No TV series added")
        raise typer.Exit()
    
    api_response.post_response(
        tsl_endpoints.add_tv_show(id, priority))

    return True

def show_list_result(response : dict):
    results = response['results']
    current_page =  int(response['page'])
    last_page =  int(response['total_pages'])

    typer.echo(f"Page {current_page}/{last_page}")

    for index, tv_show in enumerate(results, 0):
        typer.echo("{:<1} : {:<24} priority: {:<5}"
        .format(index+1, tv_show['name'][:20]+ (tv_show['name'][20:] and '..'), tv_show['priority']))
    
    try:
        while True:
            typer.echo(f"\nSelect title id \ntype {QUIT} to quit")

            if current_page != last_page:
                typer.echo(f"type {NEXT_PAGE} for the next page")
            if current_page > 1:
                typer.echo(f"type {PREVIOUS_PAGE} for the previous page")
            
            id = typer.prompt(">>>")
            
            if id == QUIT or id == QUIT.upper():
                raise typer.Abort()
            elif current_page != last_page and (id == NEXT_PAGE or id == NEXT_PAGE.upper()):
                response = api_response.get_response(
                    tsl_endpoints.show_list(current_page+1))

                series_id = show_list_result(response)
                break
            elif current_page > 1 and (id == PREVIOUS_PAGE or id == PREVIOUS_PAGE.upper()):
                response = api_response.get_response(
                    tsl_endpoints.show_list(current_page-1))

                series_id = show_list_result(response)
                break
            else:
                try:
                    id = int(id)-1

                    if id >= 0 and id < len(results):
                        series_id = results[id]['id']
                        break
                    typer.echo("Invalid ID")
                except Exception:
                    typer.echo("Invalid input")
    except typer.Abort:
        raise typer.Exit()

    return series_id

def edit_priority_result(id: int):
    try:
        while True:
            typer.echo(f"Update priority [1 to 5]\ntype {QUIT} to quit")
            priority = typer.prompt(">>>")
            if priority == QUIT or priority == QUIT.upper():
                raise typer.Abort()
            else:
                try:
                    priority = int(priority)

                    if priority > 0 and priority <= 5:
                        break
                    typer.echo("Invalid number")
                except Exception:
                    typer.echo("Invalid input")
    except typer.Abort:
        typer.echo("Priority not updated")
        raise typer.Exit()

    api_response.patch_response(
        tsl_endpoints.update_priority(id, priority))

def genres_result(response : dict):
    for genre in response['genres']:
        typer.echo(f"{genre['genre']}")

def tv_show_action(id: int):
    try:
        while True:
            typer.echo(f"\nSelect action \ntype {QUIT} to quit")
            typer.echo(f"type {SHOW} to see the details")
            typer.echo(f"type {EDIT} to edit the priority")
            typer.echo(f"type {DELETE} to remove the tv show from the list")
            
            choice = typer.prompt(">>>")
            
            if choice == QUIT or choice == QUIT.upper():
                raise typer.Abort()
            elif choice == SHOW or choice == SHOW.upper():
                details_response = api_response.get_response(tsl_endpoints.tv_show_details(id))
                tv_show_details_result(details_response)
                break
            elif choice == EDIT or choice == EDIT.upper():
                edit_priority_result(id)
                typer.echo("The priority has been updated!")
                break
            elif choice == DELETE or choice == DELETE.upper():
                api_response.delete_response(tsl_endpoints.remove_tv_show(id))
                typer.echo("Tv show removed from the list.")
                break
            else:            
                typer.echo("Invalid input")
    except typer.Abort:
        raise typer.Exit()