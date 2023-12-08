from Model_SAoI import Packet, System 
from numpy import random
from collections import deque

sistem = System(["M", 0.1],["M",1],gateway=True, num_of_entries=5, num_of_queues=1, num_of_servers=1)

prihodi = sistem.create_arrivals(100)
spremenjeni_prihodi = []
for lista in prihodi:
    sez = []
    for e in lista:
        sez.append(int(e))
    spremenjeni_prihodi.append(sez)
print(spremenjeni_prihodi)