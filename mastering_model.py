from Model_SAoI import Packet, System 
from numpy import random

#Packet(size, trans, gen_time, position)
#System(arrivals, servings, gateway=False, num_of_queues=1, num_of_servers=1, queue=deque([]), queue_capacity=None, FIFO=True, age=0)
#First task is to simulate M/M/1 queue and measure its age.
#sistem = System(["M", 0.5], ["M", 1]) #ustvarimo sistem, v katerem se nahajamo
#prihodi = sistem.create_arrivals(100) #ustvarimo sto prihodov
#strezbe = sistem.create_servings(100) #ustvarimo sto strežb
#
#time = 0 
#ar_ind = 0
#ser_ind = 0
#inter_serving_time = 0
#age_list = []
#for i in range(2000):
#    sistem.increase_age(0.05)
#    time += 0.05 
#    inter_serving_time += 0.05
#    if prihodi[ar_ind] < time:
#        sistem.add_to_queue(Packet(1,0,time,"bq"))
#        ar_ind += 1
#    if strezbe[ser_ind] < inter_serving_time and len(sistem.queue) != 0:
#        sistem.set_age(time - sistem.queue[0].gen_time)
#        sistem.delete_from_queue()
#        inter_serving_time = 0
#        ser_ind += 1
#    age_list.append(sistem.age)

#Poskusimo sedaj simulirati še vrsto M/D/1
sistem1 = System(["D", 0.5], ["M", 1])
prihodi1 = sistem1.create_arrivals(1000)
strezbe1 = sistem1.create_servings(1000)

time = 0
ar_ind = 0
ser_ind = 0
inter_serving_time = 0
age_list = []
for i in range(20000):
    sistem1.increase_age(0.05)
    time += 0.05
    inter_serving_time += 0.05
    if prihodi1[ar_ind] < time:
        sistem1.add_to_queue(Packet(1,0,time,"bq"))
        ar_ind += 1 
    if strezbe1[ser_ind] < inter_serving_time and len(sistem1.queue) != 0:
        sistem1.set_age(time - sistem1.queue[0].gen_time)
        sistem1.delete_from_queue()
        inter_serving_time = 0
        ser_ind += 1
    age_list.append(sistem1.age)

print(sum(age_list)/len(age_list))