import requests

session = requests.Session()

api_path = 'https://api.jikan.moe/v3/'
search_type_list = ['anime','manga','person']

def mal_search(search_type: str, query: str):
    query = query.split()
    if search_type in search_type_list:
        query_str = '+'.join(query)
        search_path = ''.join((api_path,'search/',search_type))
        # response = requests.get(search_path, params={
        response = session.get(search_path, params={    
            'q':query_str,
            'page':1
            })
        response_json = response.json()

        if search_type=='person':
            return [[result['mal_id'],result['name'],result['url']] for result in response_json['results']]
        else:
            return [[result['mal_id'],result['title'],result['url']] for result in response_json['results']]
    else:
        return None


def get_info(search_type, mal_id):
    if mal_id: 
        url = ''.join((api_path,search_type,'/',str(mal_id)))
        response = session.get(url)
        response_json = response.json()
    return response_json

