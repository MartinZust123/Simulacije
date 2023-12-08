#In this document I am going to simulate model described in article that me and Jernej Hribar 
#are going to use for IEEE INFOCOM Age of Information Workshop. 

from Model_SAoI import System, Packet
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

#We first create our system model in which we are going to perform simulations.
system = System(["M", 0.1], ["M", 1], gateway=True, num_of_entries=5)

#We than create arrivals. It is list with 5 lists. In each of those lists we have 
#values of arrival times for each entry.
table_of_arrivals = system.create_arrivals(1000)

#we also create list of servings.
list_of_servings = system.create_servings(1000)

