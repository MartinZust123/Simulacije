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
for a in [0.3,0.6,0.9,2,4]:

    objective_list = []
    
    for mul in range(80):

        #We first create our system model in which we are going to perform simulations.
        system = System(["M", 0.1 + mul*0.01], ["M", 1], queue=deque([]), gateway=False, num_of_entries=1)
        
        #We than create arrivals. 
        table_of_arrivals = system.create_arrivals(500000)
        
        #we also create list of servings.
        list_of_servings = system.create_servings(500000)

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
        power = [0,0] #first component says what is the power of the connection between source and server and what time it remains
        