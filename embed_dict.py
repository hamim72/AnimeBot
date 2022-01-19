import discord

COLOR = discord.Color.blue().value
AUTHOR = {
    'name':'MyAnimeList',
    'url':'https://myanimelist.net/',
    'icon_url':'https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png'
}

def anime(resp: dict):
    if resp['episodes']==None:
        resp['episodes'] = 'Unknown'

    if resp['synopsis']=='':
        resp['synopsis'] = 'No synopsis'

    if resp['studios']:
        studios = [studio['name'] for studio in resp['studios']]
        studios = ', '.join(studios)
    else:
        studios = 'None found'
        
    anime_dict = {
        'title':resp['title'],
        'url':resp['url'],
        'description':resp['synopsis'],
        'color':COLOR,
        'thumbnail':{
            'url':resp['image_url']
        },
        'author':AUTHOR,
        'fields':[
            {
                'name':'Type',
                'value':resp['type'],
                'inline':True
            },
            {
                'name':'Score',
                'value':str(resp['score']),
                'inline':True
            },
            {
                'name':'Members',
                'value':resp['members'],
                'inline':True
            },
            {
                'name':'Episodes',
                'value':str(resp['episodes']),
                'inline':True
            },
            {
                'name':'Status',
                'value':resp['status'],
                'inline':True
            },
            {
                'name':'Studios',
                'value':studios,
                'inline':True
            },
        ]
    }
    return anime_dict

def manga(resp):
    if resp['chapters']==None:
        resp['chapters'] = 'Unknown'

    if resp['synopsis']=='':
        resp['synopsis'] = 'No synopsis'

    authors = [author['name'] for author in resp['authors']]
    authors = ', '.join(authors)

    manga_dict = {
        'title':resp['title'],
        'url':resp['url'],
        'description':resp['synopsis'],
        'color':COLOR,
        'thumbnail':{
            'url':resp['image_url']
        },
        'author':AUTHOR,
        'fields':[
            {
                'name':'Type',
                'value':resp['type'],
                'inline':True
            },
            {
                'name':'Score',
                'value':str(resp['score']),
                'inline':True
            },
            {
                'name':'Members',
                'value':resp['members'],
                'inline':True
            },
            {
                'name':'Chapters',
                'value':str(resp['chapters']),
                'inline':True
            },
            {
                'name':'Status',
                'value':resp['status'],
                'inline':True
            },
            {
                'name':'Authors',
                'value':authors,
                'inline':True
            },
        ]
    }
    
    return manga_dict

def person(resp):
    person_dict = {
        'title':resp['name'],
        'url':resp['url'],
        'color':COLOR,
        'thumbnail':{
            'url':resp['image_url']
        },
        'author':AUTHOR
    }
    return person_dict

search_results = {
    'title':'Search Results',
    'color':COLOR,
    'author':AUTHOR
}
