"""
Etapas
- fazer download das imagens do pokeapi

Sync demorou - 2 minutos e 47 segundos na primeira vez
                na segunda 1 minutos e 46 segundos
                na terceira 2 minutos e 59 segundos
                na quarta 1 minutos e 44 segundos
threads
asyncio
concurrence.features
multprocess
"""
from datetime import datetime
from urllib.parse import urljoin
from requests import get
from os import makedirs
from os.path import exists
from threading import Thread
from shutil import rmtree
from queue import Queue

# Define variáveis
base_url = "https://pokeapi.co/api/v2/"
path = '/tmp/downloads/'

def download_image(filename, url, *, path=path, type='png'):
    """
    Downloada imagem do pokeapi
    """
    response = get(url, stream=True)
    with open(path + filename + '.' + type, 'wb') as out_file:
        out_file.write(response.content)
    return filename + '.' + type

def get_image_url(url, sprite='front_default'):
    """
    Retorna url da imagem do pokeapi
    """
    return get(url).json()['sprites'][sprite]


# Inicio do programa (Cria diretorio e inicia o timer)
if not exists(path):
    makedirs(path)
else:
    rmtree(path)
    makedirs(path)

start_time = datetime.now()
pokemons = get(urljoin(base_url, 'pokemon/?limit=500')).json()['results']
images_url = {j['name']: get_image_url(j['url']) for j in pokemons}
files = [download_image(name,url) for name, url in images_url.items()]
end_time = datetime.now() - start_time

print(f'Tempo total (hh:mm:ss.ms) {end_time}')
