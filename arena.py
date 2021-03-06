import matplotlib.pyplot as plt
from agents import Prey, Hunter
import numpy as np
from auxilary_functions import intersects


class Arena:
    def __init__(self, limits = None):
        self.agents = []
        self.hunters = {}
        self.prey = {}
        self.max_hunter_id = 0
        self.max_pray_id = 0
        self.hunter_population = 0
        self.pray_population = 0
        self.anim_limits = limits

    def add_hunter(self, max_velocity, max_acceleration, decision_function, position, catch_radious, name = None):
        self.max_hunter_id += 1
        if name is None:
            name = 'hunter' + str(self.max_hunter_id + 1)
        self.hunters[name] = Hunter(max_velocity, max_acceleration, decision_function, position, catch_radious, name)
        self.agents.append(name)
        self.hunter_population += 1

    def add_prey(self,max_velocity, max_acceleration, decision_function, position, evasion_chance, name = None):
        self.max_pray_id += 1
        if name is None:
            name = 'prey' + str(self.max_pray_id + 1)
        self.prey[name] = Prey(max_velocity, max_acceleration, decision_function, position, evasion_chance, name)
        self.agents.append(name)
        self.pray_population += 1

    def propagate(self):
        for agent in self.hunters.values():
            agent.update_situation((self.hunters, self.prey))
            agent.make_maneuver()
            plt.scatter(agent.position[0], agent.position[1], color = 'red')
        for agent in self.prey.values():
            agent.update_situation((self.hunters, self.prey))
            agent.make_maneuver()
            plt.scatter(agent.position[0], agent.position[1], color='blue')
            plt.pause(0.25)



    def check_get_got(self):
        cached = []
        for hunter in self.hunters.values():
            for prey in self.prey.values():
                if intersects([hunter.last_move, hunter.position], [prey.last_move, prey.position]) \
                        and (prey.evasion_chance < np.random.uniform(0,1)):
                    print('Hunter {0} got {1}'.format(hunter.name, prey.name))

                    cached.append(prey.name)
                    self.agents.remove(prey.name)
                    self.pray_population -= 1
        for i in cached:
            self.prey.pop(i)

    def simulate(self, turns_threshold):
        plt.figure()
        plt.xlim(self.anim_limits[0])
        plt.ylim(self.anim_limits[1])
        turn = 0
        while True:
            self.propagate()
            self.check_get_got()
            if self.pray_population == 0:
                print('Hunters won after {0} turns. Got {1} agents in the process'.format(turn, self.max_pray_id))
                plt.show()
                break
            if turn == turns_threshold:
                print('Pray won after {0} turns. Lost {1} agents in the process'.format(turn, self.max_pray_id -
                                                                                        self.pray_population))
                plt.show()
                break
            turn += 1
