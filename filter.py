import typer
import api_response
import tsl_endpoints
import tsl_result

app = typer.Typer()

EMPTY =  "No tv show found"

def filter_list(list_response):
    if (list_response['total_results'] == 0):
        typer.echo(EMPTY)
        raise typer.Exit()

    tv_show_id =  tsl_result.show_list_result(list_response)
    tsl_result.tv_show_action(tv_show_id)

@app.command()
def name(tv_show_name:str):
    filter_list(api_response.get_response(tsl_endpoints.filter_by_title(tv_show_name)))

@app.command()
def genre(genre:str):
    filter_list(api_response.get_response(tsl_endpoints.filter_by_genre(genre)))
    
@app.command()
def rating(rating:float):
    filter_list(api_response.get_response(tsl_endpoints.filter_by_rating(rating)))
    
@app.command()
def priority(priority:int):
    filter_list(api_response.get_response(tsl_endpoints.filter_by_priority(priority)))
