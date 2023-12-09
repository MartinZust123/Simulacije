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

strezbe = sistem.create_servings(100)

#Sedaj simulirajmo to vrsto.
time = 0
inter_serving_time = 0
age = 0
ar_ind_list = [0 for i in range(5)]
ser_ind = 0
before_gateway = []
age_list = []
bg = []
q = []
for i in range(10000):
    time += 0.01
    inter_serving_time += 0.01
    age += 0.01
    for i in range(5):
        if time > prihodi[i][ar_ind_list[i]]:
            pack = sistem.create_packet(10, time)
            before_gateway.append(pack)
            ar_ind_list[i] += 1
    removal = []
    for i in range(len(before_gateway)):
        before_gateway[i].trans -= 0.01
        if before_gateway[i].trans < 0:
            sistem.queue.append(before_gateway[i])
            removal.append(before_gateway[i])
    for e in removal:
        before_gateway.remove(e)
    if inter_serving_time > strezbe[ser_ind] and len(sistem.queue) != 0:
        age = time - sistem.queue[0].gen_time
        sistem.queue.popleft()
        ser_ind += 1
        inter_serving_time = 0
    age_list.append(age)
    bg.append(len(before_gateway))
    q.append(len(sistem.queue))

print(q)