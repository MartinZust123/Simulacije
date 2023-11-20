# Model for SAoI

import numpy as np 
from numpy import random 
from collections import deque

#elements of next class are update packets that we are studying in our
#queueing system. It is the central class of this model. 

class Packet:
    """
    Elements of class Packet present packet updates 
    with specific size, transmition time and generation time.
    """

    num_of_packets = 0

    def __init__(self, size, trans, gen_time, position):
        """
        Arguments
        ---------
        size: int
            number of bytes it takes in the computer memory.

        trans: int
            amout of time units it takes to move a packet from source to gateway. 

        gen_time: float 
            time at which packet was created.

        position: string
            current possition of the packet.
        """ 
        self.size = size
        self.trans = trans
        self.gen_time = gen_time
        self.position = position

        Packet.num_of_packets += 1
    
    def __repr__(self):
        return "Packet(size={}, trans={}, gen_time={}, position={})".format(self.size, self.trans, self.gen_time, self.position)

    def __str__(self):
        return "Instance of class Packet with size {}, remaining transsmision time {}, time of generation {} and current possition {}.".format(self.size, self.trans, self.gen_time, self.position)
    
    def transmit(self, time):
        """
        Reduces the transmission time of a packet. 

        Arguments
        ---------
        time: float

        Effects
        ---------
        it reduces the transmisson time of a packet for 'time' units.
        """
        self.trans -= time

    def change_position(self, new_position):
        """
        Changes the position of a packet to a new_position

        Arguments
        ---------
        new_position: string
            Usualy in set {"bg" (before gateway), "ag" (after gateway), "q" (queue), "o" (out)}

        Effects
        --------
        changes the position of a packet to string new_position
        """
        self.position = new_position 

        if self.position == "o":
            Packet.num_of_packets -= 1

    #What if we would like to change number of packets for some reason?
    @classmethod 
    def change_num(cls, n):
        """
        Sets the number of packets in the system to n. 

        Arguments
        ---------
        n: int 

        Effects
        --------
        changes the number of packets in the system to n.
        """
        cls.num_of_packets = n

    @classmethod 
    def add_num(cls, n):
        """ 
        Increase the number of packets in the system for n. 

        Arguments 
        ---------
        n: int 

        Effects
        -------
        increase the number of packets in the system for n. 
        """
        cls.num_of_packets += n 

#----------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------#

#we also want to generalize concept of a system because we notice that certain patterns repeat. 
#With this reason we create class System. Its elements are queueing systems. 
class System:
    """ 
    Elements of class System present queueing system with 
    specific arrival, serving and other policies. 
    """

    def __init__(self, arrivals, servings, gateway=False, num_of_queues=1, num_of_servers=1, queue=deque([]), queue_capacity=None, FIFO=True, age=0):
        """
        Arguments
        ---------
        arrivals: (str, float) tuple
            determines the distribution and the frequency of arrivals. 

        servings: (str, float) tuple
            determines the distribution and the frequency of servings.

        gateway: bool
            Determines whether or not gateway is included in the system. 
            Default value is False. 

        num_of_queues: int 
            determines the number of queues that the system will have. 
            Default value is 1.

        num_of_servers: int 
            determines the number of servers that the system will have.
            Default values is 1 

        queue: deque
            presents the queue in the system. 

        queue_capacity: int optional
            determines the maximum number of elements in each queue. 
            Default value is None which represents infinity.

        FIFO: bool
            determines what is the serving policy of the packets. 
        """ 
        self.arrivals = arrivals 
        self.servings = servings 
        self.gateway = gateway 
        self.num_of_queues = num_of_queues
        self.num_of_servers = num_of_servers
        self.queue = queue
        self.queue_capacity = queue_capacity
        self.FIFO = FIFO
        self.age = 0

    #Example of an element is simple M/M/1 queue with exponential interarrival time, 
    #exponential serving time, one server and one queue, without gateway and infinite
    #queue capacity. We create such queue with System(("M",lambda),("M", mi)). 

    def __repr__(self):
        return f"System(arrivals={self.arrivals}, servings={self.servings}, gateway={self.gateway}, FIFO={self.FIFO})"

    def __str__(self):
        return f"Queuing system with arrival rate {self.arrivals} and serving rate {self.servings}."

    def __len__(self):
        if self.queue_capacity == None:
            return 0
        else:
            return self.queue_capacity
    
    def create_arrivals(self, total_time):
        """ 
        Creates list of arrivals for specific system such that
        timestamp of last arrival is bigger than total_time. 

        Arguments
        ---------
        total_time: int 
            total time of the symulation of the queueing system. 

        Returns
        --------
        float list
            list of arrival times of specific system.  
        """
        [letter, arrival_rate] = self.arrivals
        if letter == "M":
            #we deal with exponential interarrival times
            t = 0
            list_of_arrivals = []
            while t <= total_time: #when we exceed total_time we stop
                dt = random.exponential(scale=(1/arrival_rate)) #interarrival time
                t += dt
                list_of_arrivals.append(t)
            return list_of_arrivals
        elif letter == "D":
            #we deal with deterministic iterarrival times
            t = 0
            dt = (1/arrival_rate) #interarrival time
            list_of_arrivals = []
            while t <= total_time: 
                t += dt 
                list_of_arrivals.append(t)
            return list_of_arrivals
        elif letter == "U":
            #we deal with continuos uniform interarrival time
            t = 0
            list_of_arrivals = []
            while t <= total_time:
                dt = random.uniform(0,2/arrival_rate) #interarrival time
                t += dt 
                list_of_arrivals.append(t)
            return list_of_arrivals
        else:
            raise ValueError("Wrong input!")
        #note that arrival times are not interarrival but timestamps at which 
        #the system recieves the new update. If we want to derive interarrival
        #times we need to subtract consequative elements of this list. 

    def create_servings(self, total_time):
        """ 
        Creates list of serving times for specific system such that
        sum of all values is bigger than total_time. 

        Arguments
        ---------
        total_time: int 
            total time of the symulation of the queueing system. 

        Returns
        --------
        float list
            list of serving times of specific system.  
        """
        [letter, serving_rate] = self.servings
        if letter == "M":
            #we deal with exponential random variable
            t = 0
            list_of_servings = []
            while t <= total_time: 
                dt = random.exponential(scale=(1/serving_rate))
                list_of_servings.append(dt)
                t += dt
            return list_of_servings
        elif letter == "D":
            #we deal with deterministic serving times
            t = 0
            dt = (1/serving_rate)
            n = int(total_time/dt) + 1
            list_of_servings = [dt] * n
            return list_of_servings
        elif letter == "U":
            #we deal with uniform continuous random variable 
            t = 0
            list_of_servings = []
            while t <= total_time:
                dt = random.uniform(0,2/serving_rate)
                list_of_servings.append(dt)
                t += dt 
            return list_of_servings
        else:
            raise ValueError("Wrong input!")
        #note that serving times are not timestamps at which 
        #specific serving is terminated but rather time that it
        #takes for specific serving. If we want to derive absolute 
        #timestamps at which specific serving is completed than we
        #need to sum all of the values till that serving itself included. 

    def create_packet(self, size, time):
        if self.gateway == True:
            trans = 5 
        else:
            trans = 0
        return Packet(size, trans, time, "bg")

    #we interpret packet that is in the last position of deque as the packet that is in the last position of queue.
    #That is why we alway add elements to the end of deque, that is we append them. 
    def add_to_queue(self, packet):
        """Method that adds packet from class Packet to queue."""
        self.queue.append(packet)

    #for the method delete_packet we need to be careful whether we have FIFO policy or LIFO policy. 
    def delete_from_queue(self):
        """Method that deletes packet of type Packet from queue."""
        if self.FIFO == True:
            self.queue.popleft()
        else:
            self.queue.pop()

    def shuffle(self):
        """Method that shuffles the queue."""
        def to_list(dq):
            l = []
            for e in dq:
                l.append(e)
            return l
        l = to_list(self.queue)
        self.queue = deque(random.permutation(l))

    def increase_age(self, time_delta):
        """Increase age for time_delta"""
        self.age += time_delta

    def set_age(self, age):
        """Sets age of the system to age"""
        self.age = age

class OneQueueServer(System):
    
    def __init__(self, arrivals, servings, gateway=False, num_of_queues=1, queue_capacity=None, FIFO=True):
        super().__init__(arrivals, servings, gateway, num_of_queues, queue_capacity, FIFO)
        self.utilisation_ratio = arrivals/servings
        