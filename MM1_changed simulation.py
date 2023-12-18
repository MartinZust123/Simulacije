# In this document we are going to simulate M/M/1 queue. That is the most simple queue that we can simulate in queueing theory.
# We will get optimized approach that we didn't use for now. 

from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from numpy import random

# We first create some arrivals
#arrivals = []
#arrivals.append(random.exponential(scale=2,size=1))
#for i in range(200):
#    arrivals.append(arrivals[-1] + random.exponential(scale=2, size=1))
arrivals = random.exponential(scale=2,size=200)

# We than create some serving times 
servings = random.exponential(scale=1, size=200)

#Now we only go over times that actually change situation in the queue. 
ar_ind = 0
ser_ind = 0
queue = []
time = arrivals[0]
queue = []



