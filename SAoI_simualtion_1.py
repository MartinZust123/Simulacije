#In this document I am going to simulate model described in article that me and Jernej Hribar 
#are going to use for IEEE INFOCOM Age of Information Workshop. 

from Model_SAoI import System, Packet
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

#We first create our system model in which we are going to perform simulations.
system = System(["M", 0.3], ["M", 1], gateway=True, num_of_entries=5)

#We than create arrivals. It is list with 5 lists. In each of those lists we have 
#values of arrival times for each entry.
table_of_arrivals = system.create_arrivals(1000)

#we also create list of servings.
list_of_servings = system.create_servings(1000)

#Now we simulate this queue.
time = 0
inter_serving_time = 0
age = 0
ar_ind_list = [0 for i in range(5)]
ser_ind = 0
before_gateway = []
after_gateway = []
age_list = []
bg = []
q = []
for i in range(10000):
    time += 0.01
    inter_serving_time += 0.01
    age += 0.01
    for i in range(5):
        if time > table_of_arrivals[i][ar_ind_list[i]]:
            pack = system.create_packet(10, time)
            before_gateway.append(pack)
            ar_ind_list[i] += 1
    removal = []
    for i in range(len(before_gateway)):
        before_gateway[i].trans -= 0.01
        if before_gateway[i].trans < 0:
            before_gateway[i].trans = 5
            after_gateway.append(before_gateway[i])
            removal.append(before_gateway[i])
    for e in removal:
        before_gateway.remove(e)
    removal = []
    for i in range(len(after_gateway)):
        after_gateway[i].trans -= 0.01
        if after_gateway[i].trans < 0:
            system.queue.append(after_gateway[i])
            removal.append(after_gateway[i])
    for e in removal:
        after_gateway.remove(e)
    if inter_serving_time > list_of_servings[ser_ind] and len(system.queue) != 0:
        age = time - system.queue[0].gen_time
        system.queue.popleft()
        ser_ind += 1
        inter_serving_time = 0
    age_list.append(age)
    bg.append(len(before_gateway))
    q.append(len(system.queue))

avg_age = sum(age_list)/len(age_list)
print(avg_age)