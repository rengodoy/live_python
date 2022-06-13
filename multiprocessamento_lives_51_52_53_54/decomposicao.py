from queue import Queue
from shutil import copyfileobj, get_unpack_formats
from threading import Thread, Event
from time import sleep
from tracemalloc import start
from requests import get
from urllib.parse import urljoin
from os import makedirs
from os.path import exists
from shutil import rmtree
from datetime import datetime
from functions import target

base_url = "https://pokeapi.co/api/v2/"
event = Event()
fila = Queue(maxsize=101)
path = '/tmp/downloads/'



def get_urls():
    pokemons = get(urljoin(base_url, 'pokemon/?limit=5 ')).json()['results']
    [fila.put(pokemon) for pokemon in pokemons]
    event.set()
    fila.put('Kill')

class Worker(Thread):
    def __init__(self, target, queue, *, name='Worker'):
        super().__init__()
        self.name = name
        self.queue = queue
        self._target = target
        self._stoped = False

    def run(self):
        # event.wait()
        import ipdb; ipdb.set_trace()
        while not self.queue.empty():
            pokemon = self.queue.get()
            print(self.name, pokemon)
            if pokemon == 'Kill':
                self.queue.put(pokemon)
                self._stoped = True
                break
            self._target(pokemon)

    def join(self):
        while not self._stoped:
            sleep(0.1)

# Inicio do programa (Cria diretorio e inicia o timer)
if not exists(path):
    makedirs(path)
else:
    rmtree(path)
    makedirs(path)

start_time = datetime.now()
get_urls()
print(fila.queue)
print('start')
th = Worker(target=target, queue=fila, name='Worker1')
th.start()
th.join()
end_time = datetime.now() - start_time