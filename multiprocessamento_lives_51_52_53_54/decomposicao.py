from queue import Queue
from threading import Thread, Event
from time import sleep
from requests import get
from urllib.parse import urljoin
from functions import target, timeit

base_url = "https://pokeapi.co/api/v2/"
event = Event()
fila = Queue(maxsize=101)
path = '/tmp/downloads/'



def get_urls(size=100,offset=0):
    pokemons = get(urljoin(base_url, f'pokemon/?limit={size}&offset={offset}')).json()['results']
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
        print(self.name, 'started')

    def run(self):
        event.wait()
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


def get_pool(n_th:int):
    """ Cria n threads """
    return [Worker(target=target, queue=fila, name=f'Worker {i}') for i in range(n_th)]


with timeit():
    print(fila.queue)
    thrs = get_pool(10)
    print('start')
    get_urls(size=50, offset=0)
    [th.start() for th in thrs]
    get_urls(size=50,offset=50)
    get_urls(size=50,offset=100)
    get_urls(size=50,offset=150)
    get_urls(size=50,offset=200)
    get_urls(size=50,offset=250)
    get_urls(size=50,offset=300)
    print('joins')
    [th.join() for th in thrs]