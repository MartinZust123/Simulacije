#In this document I am going to simulate model described in article that me and Jernej Hribar 
#are going to use for IEEE INFOCOM Age of Information Workshop. 

from Model_SAoI import System, Packet
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import os 

# Get current working folder
current_directory = os.getcwd()

# Build absolute path to the file
file_path = os.path.join(current_directory, "Obravnava CI za Veliko Britanijo", "Carbon_Intensity_Data_jan.csv")

# Read CSV file
df_jan = pd.read_csv(file_path)

# Create list of values of CI
CI_list = df_jan["Actual Carbon Intensity (gCO2/kWh)"].tolist()

#We need to change CI_list, such that it will have constant values of CI for half an hour.
CI_list1 = []
for i in range(500):
    for j in range(30*60*100):
        CI_list1.append(CI_list[i])

def objective_function(aoi, cf, a):
    return aoi*(cf**a)

objective_table = []
for a in [0.3,0.6,0.9,1.2,1.4]:

    objective_list = []
    
    for mul in range(80):

        #We first create our system model in which we are going to perform simulations.
        system = System(["M", 0.1 + mul*0.01], ["M", 1], queue=deque([]), gateway=False, num_of_entries=1)
        
        #We than create arrivals. 
        table_of_arrivals = system.create_arrivals(2000)
        
        #we also create list of servings.
        list_of_servings = system.create_servings(2000)

        #Now we simulate this queue.
        time = 0
        inter_serving_time = 0
        age = 0
        ar_ind = 0
        ser_ind = 0
        age_list = []
        q = []
        CF = 0
        CF_list = []
        busy = 0
        power_list = []
        powerv = [0,0] #first component says what is the power of the connection between source and server and what time it remains

        for i in range(100000):
            #We increase all of the parameters that are dependant on time
            time += 0.01
            inter_serving_time += 0.01
            age += 0.01
            #We welcome new arrivals from all of the sources if there are any
            if time > table_of_arrivals[0][ar_ind]:
                pack = Packet(size=10, gen_time=time, trans=0, position="q")
                ar_ind += 1
                powerv = [5,0.05]
            #We refresh the time remaining value in power
            powerv[1] -= 0.01
            if powerv[1] < 0:
                powerv = [0,0]
            removal = [] #list with elements to remove from before_gateway
            #We check whether we must take a new element to the server
            if inter_serving_time > list_of_servings[ser_ind] and len(system.queue) == 0:
                busy = 0
            elif inter_serving_time > list_of_servings[ser_ind] and len(system.queue) != 0:
                age = time - system.queue[0].gen_time
                system.queue.popleft()
                ser_ind += 1
                inter_serving_time = 0
                busy = 1
            age_list.append(age)
            q.append(len(system.queue))
            power = 10 + 10*busy + powerv[0]
            CF += (power*CI_list1[i])*0.01
        
        CF_avg = CF/100000
        age_avg = sum(age_list)/len(age_list)
        objective_list.append(objective_function(age_avg, CF_avg, a))
    
    objective_table.append(objective_list)

x_values = []
x = 0.1
for i in range(80):
    x_values.append(x)
    x += 0.01

#plt.plot(x_values, CF_avg_list)
plt.plot(x_values, objective_table[0], label="a=0.3")
plt.plot(x_values, objective_table[1], label="a=0.6")
plt.plot(x_values, objective_table[2], label="a=0.9")
plt.plot(x_values, objective_table[3], label="a=1.2")
plt.plot(x_values, objective_table[4], label="a=1.4")
plt.legend()
plt.show()