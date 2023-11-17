from Model_SAoI import Packet, System 
from numpy import random

#First task is to simulate M/M/1 queue and measure its age.
sistem = System(["M", 0.5], ["M", 1])
prihodi = sistem.create_arrivals(100)
strezbe = sistem.create_servings(100)

time = 0
ar_ind = 0
ser_ind = 0
inter_serving_time = 0
age_list = []
for i in range(2000):
    sistem.increase_age(0.05)
    time += 0.05 
    inter_serving_time += 0.05
    if prihodi[ar_ind] < time:
        sistem.add_to_queue(Packet(1,0,time,"bq"))
        ar_ind += 1
    if strezbe[ser_ind] < inter_serving_time and len(sistem.queue) != 0:
        sistem.set_age(time - sistem.queue[0].gen_time)
        sistem.delete_from_queue()
        inter_serving_time = 0
        ser_ind += 1
    age_list.append(sistem.age)

avg_age = sum(age_list)/len(age_list)
print(avg_age)
