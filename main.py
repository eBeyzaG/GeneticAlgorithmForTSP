import math
import random

class City:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    
    def print_info(self):
        print("City:", self.id, "Coordinates:", str(self.x) + ",", self.y)

class Solution:
    def __init__(self, city_list=None):
        if city_list is None:
            self.city_list = []
        else:
            self.city_list = city_list

        self.calculate_fitness()

    def calculate_distance(self, city_1, city_2):
        return math.sqrt((city_1.x - city_2.x)**2 + (city_1.y - city_2.y)**2)

    def calculate_fitness(self):
        total_distance = 0
        if self.city_list:
            for count, city in enumerate(self.city_list):
                if count == len(self.city_list)  - 1:
                    break
                total_distance += self.calculate_distance(self.city_list[count], self.city_list[count+1])
            total_distance += self.calculate_distance(self.city_list[-1], self.city_list[0])
        self.fitness = total_distance
        return total_distance

    def print_solution(self):
        for city in self.city_list:
            print(str(city.id) + " ", end='')
        print("Fitness:", self.fitness)


PARENT_COUNT = 10
CITY_COUNT = 0
MUTATION_PROB = 0.3
ITERATION_COUNT = 5000
K_TOURNAMENT_PM = 10
POPULATION_SIZE = 150


#store all cities    
cities = []

#list of lists to store solutions
population = []

glob_best_solution = None


def print_population():
    i = 1
    for solution in population:
        print("Solution", i)
        for city in solution.city_list:
            print(str(city.id) + " ",  end='')
        print("  Fitness :" + str(solution.fitness))
        i+=1

def read_file():
    
    global cities
    global CITY_COUNT
    #start reading the file from fourth line
    tsp_file = open("Cities Coordinates.txt", "r")

    for line in tsp_file.readlines()[3:-1]:
        words = line.split()
        new_city = City(int(words[0]), int(words[1]), int(words[2]))
        #new_city.print_info()
        cities.append(new_city)
    CITY_COUNT = len(cities)

    tsp_file.close()

def initialize_population(pop_size=100):
    for i in range(pop_size):
        #create a random solution and add it to population
        copy = cities[:]
        random.shuffle(copy)
        new_sol = Solution(copy)
        population.append(new_sol)

def k_tournament_parent_selection(k=10):
    #choose k solutions randomly then choose the best one among them 
    # as a parent
    random_chosens = random.choices(population, k=k)
    optimum_sol_fitness = 57384975643876345
    optimum_sol = None
    
    for sol in random_chosens:
        if sol.fitness < optimum_sol_fitness:
            optimum_sol_fitness = sol.fitness
            optimum_sol = sol
    
    return optimum_sol

def order_one_cross_over(parent_1, parent_2):

    swath = []
    child = Solution()

    random_index = random.randint(0, CITY_COUNT - 1)
    random_swath_width = random.randint(1, CITY_COUNT - 1)

    #make sure the chosen width does not exceed list
    while random_index + random_swath_width >= CITY_COUNT :
        random_swath_width -= 1
    
    #create swath with elements chosen at random index from parent 1 
    swath.extend(parent_1.city_list[random_index : random_index + random_swath_width])

    #copy from second parent to child if not in the swath
    for i in range(CITY_COUNT):
        if parent_2.city_list[i] not in swath:
            child.city_list.append(parent_2.city_list[i])
    
    #add swath to the child
    child.city_list[random_index:random_index] = swath[:]
    
    child.calculate_fitness()
    child.print_solution()
    return child

def inversion_mutation(child):
    #choose random indices
    random_index = random.randint(1, CITY_COUNT - 1)
    random_second_index = random.randint(1, CITY_COUNT - 1)
    
    #make sure the first index is smaller than the second
    if random_second_index < random_index:
        temp = random_index
        random_index = random_second_index
        random_second_index = temp

    #inverse the elements from first index to second index
    child.city_list = child.city_list[0:random_index] + child.city_list[random_second_index:random_index-1:-1] + child.city_list[random_second_index + 1:]
    child.calculate_fitness()

def find_worst_solution():
    worst_sol_index = 0
    worst_sol_fitness = -1
    for idx,solution in enumerate(population):
        if solution.fitness > worst_sol_fitness:
            worst_sol_index = idx
            worst_sol_fitness = solution.fitness
    return worst_sol_index

def find_best_solution():
    global glob_best_solution
    best_sol = None
    best_sol_fitness = 99999999999999999999999
    for idx,solution in enumerate(population):
        if solution.fitness < best_sol_fitness:
            best_sol = solution
            best_sol_fitness = solution.fitness
    glob_best_solution = best_sol
    return best_sol

def __main__():

    #read cities from file
    read_file()
    
    #initialize the population randomly & calculate fitness
    initialize_population(POPULATION_SIZE)

    for i in range(ITERATION_COUNT):

        #choose parents
        parents = []
        for j in range(PARENT_COUNT):
            parents.append(k_tournament_parent_selection(K_TOURNAMENT_PM))
        
        #apply cross over
        children = []
        for k in range(0, len(parents) - 1, 2):
            children.append(order_one_cross_over(parents[k], parents[k+1]))
            children.append(order_one_cross_over(parents[k+1], parents[k]))
    
        #apply mutation
        for child in children:
            if random.random() <= MUTATION_PROB:
                inversion_mutation(child)
                #child.print_solution()
                
        #replace worst in population with children
        for child in children:
            worst_idx = find_worst_solution()
            population[worst_idx] = child
            #child.print_solution()
            #population.pop(worst_idx)
            #population.append(child)
        
        #assign global best solution
        find_best_solution()

    print("Best Solution:")
    glob_best_solution.print_solution()
    

__main__()
