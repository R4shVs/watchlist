import typer
import tsl_result
import tsl_endpoints
import api_response
import filter

app = typer.Typer()
app.add_typer(filter.app, name='filter')

def add_token(token: str):
    f = open("token.txt", "w")
    f.write(token)
    f.close()

def remove_token():
    f = open("token.txt", "w")
    f.write("")
    f.close()

@app.command()
def token(token: str):
    add_token(token)

@app.command()
def delete_token():
    remove_token()

@app.command()
def add(tv_show_name: str):
    search_tv_show_response = api_response.get_response(tsl_endpoints.search_tv_show(tv_show_name))

    if search_tv_show_response['total_results'] == 0:
        search_tv_show_response = api_response.get_response(tsl_endpoints.search_tv_show(tv_show_name, adv=True))
        if search_tv_show_response['total_results'] == 0:
            typer.echo("Tv show not found")
            raise typer.Exit()
        adv = True
    else: adv = False

    tv_show_id = tsl_result.search_result(tv_show_name, search_tv_show_response, adv)

    details_response = api_response.get_response(tsl_endpoints.tv_show_details(tv_show_id))
    tsl_result.tv_show_details_result(details_response)
    
    add = typer.confirm("Add tv show to your list?")

    if not add:
        typer.echo("No tv show added!")
        raise typer.Abort()
    
    if tsl_result.add_tv_show_result(tv_show_id):
        typer.echo("Tv show added to your watchlist!")

@app.command()
def list():
    list_response = api_response.get_response(tsl_endpoints.show_list())

    if (list_response['total_results'] == 0):
        typer.echo("Your watchlist is empty!")
        raise typer.Exit()
    tv_show_id =  tsl_result.show_list_result(list_response)
    
    tsl_result.tv_show_action(tv_show_id)
    

@app.command()
def genres():
    genres_response = api_response.get_response(tsl_endpoints.genres())
    tsl_result.genres_result(genres_response)


if __name__ == "__main__":
    app()