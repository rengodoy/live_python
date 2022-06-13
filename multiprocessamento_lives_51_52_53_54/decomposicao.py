from multiprocessing import Event
from queue import Queue
from threading import Thread
from requests import get
from urllib.parse import urljoin

base_url = "https://pokeapi.co/api/v2/"
event = Event()
fila = Queue(maxsize=101)

def get_urls():
    pokemons = get(urljoin(base_url, 'pokemon/?limit=500')).json()['results']
    [fila.put(pokemon) for pokemon in pokemons]
    event.set()
    fila.put('Kill')

Parei em 30 minutos