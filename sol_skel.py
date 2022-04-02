"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = "north"
NORTH = "south"

NCARS = 100

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.coches_norte = Value('i',0)
        self.coches_sur = Value('i',0)
        self.semaforo_norte = Condition(self.mutex)
        self.semaforo_sur = Condition(self.mutex)
    
    def puede_entrar_sur(self):
        return self.coches_norte.value == 0
    
    def puede_entrar_norte(self):
        return self.coches_sur.value == 0
        
    def wants_enter(self, direction):
        self.mutex.acquire()
        if direction == SOUTH:
            self.semaforo_sur.wait_for(self.puede_entrar_sur)
            self.coches_sur.value += 1    
        else:
            self.semaforo_norte.wait_for(self.puede_entrar_norte)
            self.coches_norte.value += 1   
        self.mutex.release()

    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        if direction == SOUTH:
            self.semaforo_sur.notify_all()
            self.semaforo_norte.notify_all()
            self.coches_sur.value -= 1   
        else:
            self.semaforo_norte.notify_all()
            self.semaforo_sur.notify_all()
            self.coches_norte.value -= 1   
        self.mutex.release()

def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {direction} created")
    delay(6)
    print(f"car {cid} heading {direction} wants to enter")
    monitor.wants_enter(direction)
    print(f"car {cid} heading {direction} enters the tunnel")
    delay(3)
    print(f"car {cid} heading {direction} leaving the tunnel")
    monitor.leaves_tunnel(direction)
    print(f"car {cid} heading {direction} out of the tunnel")



def main():
    monitor = Monitor()
    cid = 0
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1)==1  else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s
        
if __name__ == '__main__':
    main()
