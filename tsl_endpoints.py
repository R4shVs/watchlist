tsl_api = 'http://127.0.0.1:8000/api/v1'


def search_tv_show(tv_show_name: str, page = 1, adv = False):
    return f"{tsl_api}/search?query={tv_show_name}&page={page}&advanced={adv}"

def tv_show_details(id: int):
    return f"{tsl_api}/tv_show/{id}"

def add_tv_show(id: int, priority: int):
    return f"{tsl_api}/list/{id}/add_tv_show?priority={priority}"

def show_list(page = 1):
    return f"{tsl_api}/list?page={page}"

def update_priority(id: int, priority: int):
    return f"{tsl_api}/list/{id}/edit_tv_show?priority={priority}"

def remove_tv_show(id: int):
    return f"{tsl_api}/list/{id}/remove_tv_show"

def filter_by_title(tv_show_name: str, page = 1):
    return f"{tsl_api}/list?page={page}&title={tv_show_name}"

def filter_by_genre(genre: str, page = 1):
    return f"{tsl_api}/list?page={page}&genre={genre}"

def filter_by_rating(rating : int, page = 1):
    return f"{tsl_api}/list?page={page}&rating={rating}"

def filter_by_priority(priority : int, page = 1):
    return f"{tsl_api}/list?page={page}&priority={priority}"

def genres():
    return f"{tsl_api}/genre"