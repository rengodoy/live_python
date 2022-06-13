from shutil import copyfileobj
from requests import get
from urllib.parse import urljoin

base_url = "https://pokeapi.co/api/v2/"
path = '/tmp/downloads/'

def get_sprite_url(url, sprite='front_default'):
    """Faz o download da url do sprite"""
    return url['name'],get(url).json()['sprites'][sprite]

def get_bin_file(args):
    """
    Faz o download da imagem do pokeapi
    """
    filename, url = args
    return filename,get(url, stream=True).raw

def save_file(*args, path=path, type='png'):
    """
    Salva binario da imagem do pokeapi como arquivo
    """
    filename, binary = args
    with open(path + filename + '.' + type, 'wb') as out_file:
        copyfileobj(binary, out_file)
    return filename + '.' + type

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