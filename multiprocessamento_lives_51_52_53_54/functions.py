from shutil import copyfileobj
from requests import get
from os import makedirs
from os.path import exists
from shutil import rmtree
from contextlib import contextmanager
from datetime import datetime

base_url = "https://pokeapi.co/api/v2/"
path = '/tmp/downloads/'
# Inicio do programa (Cria diretorio e inicia o timer)
if not exists(path):
    makedirs(path)
else:
    rmtree(path)
    makedirs(path)

def get_sprite_url(url, sprite='front_default'):
    """Faz o download da url do sprite"""
    return url['name'], get(url['url']).json()['sprites'][sprite]

def get_bin_file(args):
    """
    Faz o download da imagem do pokeapi
    """
    filename, url = args
    return filename,get(url, stream=True).raw

def save_file(args, path=path, type_='png'):
    """
    Salva binario da imagem do pokeapi como arquivo
    """
    filename, binary = args
    fname = f'{path}/{filename}.{type_}'
    with open(fname, 'wb') as out_file:
        copyfileobj(binary, out_file)
    return fname

def pipeline(*funcs):
    """
    Executa funções em sequencia
    """
    def inner(arg):
        state = arg
        for func in funcs:
            state = func(state)
    return inner

target = pipeline(get_sprite_url, get_bin_file, save_file)

@contextmanager
def timeit(*args):
    start_time = datetime.now()
    yield
    time_elapsed = datetime.now() - start_time
    print(f'Tempo total (hh:mm:ss.ms) {time_elapsed}')