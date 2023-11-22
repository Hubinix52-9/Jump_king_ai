from player_class_ai import Player
import random
import pygame
import time
import copy

class Evolutionary_alghoritm():
    def __init__(self, number) -> None:
        self.size_of_generation = number
        self.mutation_rate = 0.2
        self.generation = 0
        self.actual_best_score = 100
        self.actual_generation = []
        self.next_generation = []
        self.best_individuals = []
        self.elite_individual = None
        self.all_moves = True
        self.fitness_done = False
        self.crossover_done = False
        self.mutation_done = False
        self.all_landed = False
        self.was_bigger = False

    def get_mutation_done(self):
        return self.mutation_done

    def get_crossover_done(self):
        return self.crossover_done

    def get_fitness_done(self):
        return self.fitness_done

    def get_actual_gen(self):
        return self.actual_generation

    def mutation_wages(self, player):
        decide_number = random.randint(1,100)
        wages = []
        if decide_number < self.mutation_rate*100:
            for x in player.player_get_wages():
                x += random.randint(0, 2)
                wages.append(x)
            player.player_update_wages(wages)
        else:
            wages.append(player.player_get_wages())

    def create_moves(self, player):
        player_movments = [(1,0,1), (1,0,0), (1,1,0), (0,0,1), (0,1,0)]
        wages = player.player_get_wages()
        for y in range(5):
            player.player_add_new_move([random.choices(player_movments, wages)[0], random.randint(200,2000)])
    
    def create_population(self, actual_map, actual_map_id, how_many=None, parents=None, how_many_seq=None):
        if self.generation > 0 and parents is not None:
            for x in range(how_many):
                parent_a, parent_b = parents
                parent_a_wages = copy.deepcopy(parent_a.player_get_wages())
                parent_b_wages = copy.deepcopy(parent_b.player_get_wages())
                parent_a_moves = copy.deepcopy(parent_a.get_player_moves())
                parent_b_moves = copy.deepcopy(parent_b.get_player_moves())
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            random.choice([parent_a_wages, parent_b_wages]))
                self.next_generation.append(new_player)
                new_player.player_update_moves(random.choice([parent_a_moves, parent_b_moves]))
                if self.was_bigger:
                    self.create_moves(new_player)
        elif how_many_seq is None and parents is None and how_many is None: 
            for x in range(self.size_of_generation):
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            [1,1,1,1,1])
                self.create_moves(new_player)
                if self.generation == 0:
                    self.actual_generation.append(new_player)
                else:
                    self.next_generation.append(new_player)
        elif self.generation > 0 and parents is None:
            for x in range(how_many):
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            [1,1,1,1,1])
                self.create_moves(new_player)
                for y in range(how_many_seq):
                    self.create_moves(new_player)
                self.next_generation.append(new_player)

    def fitness_n_selection(self):
        self.generation += 1
        print(self.actual_best_score)
        best_indyviduals = sorted(self.actual_generation, 
                                  key=lambda x: 680-x.get_player_rect().bottom + (x.get_player_current_map_id()*680), 
                                  reverse=True)
        for x in best_indyviduals:
            if 680-x.get_player_rect().bottom + (x.get_player_current_map_id()*680) > self.actual_best_score:
                self.best_individuals.append(x)
                self.was_bigger = True
                self.actual_best_score = 680-x.get_player_rect().bottom + (x.get_player_current_map_id()*680)
                print("added best score")
        print(self.actual_best_score)
        self.fitness_done = True
    
    def crossover(self, actual_map, actual_map_id):
        number_of_individuals = len(self.best_individuals)
        if number_of_individuals > 1:
            print("two or more guys")
            if number_of_individuals % 2 == 1:
                self.best_individuals.remove(self.best_individuals[number_of_individuals-1])
            number_of_individuals = len(self.best_individuals)
            number_of_pairs = number_of_individuals / 2
            for x in range(0, number_of_individuals, 2):
                parents = (self.best_individuals[x], self.best_individuals[x+1])
                how_many = self.size_of_generation/number_of_pairs
                self.create_population(actual_map, actual_map_id, how_many, parents)
        if number_of_individuals == 1:
            print("one best guy")
            parents = (self.best_individuals[0], self.best_individuals[0])
            self.create_population(actual_map, actual_map_id, self.size_of_generation, parents)
        if self.size_of_generation > len(self.next_generation) and len(self.best_individuals) > 0:
            self.create_population(actual_map, 
                                   actual_map_id, 
                                   self.size_of_generation - len(self.next_generation), 
                                   None, 
                                   len(self.actual_generation[0].get_player_moves())//5)
        if  len(self.best_individuals) == 0 and self.elite_individual is None:
            self.create_population(actual_map, 
                                   actual_map_id, 
                                   None, 
                                   None, 
                                   None) 
        elif len(self.best_individuals) == 0 and self.elite_individual is not None:
            parents = self.elite_individual, self.elite_individual
            self.create_population(actual_map, 
                                   actual_map_id, 
                                   self.size_of_generation, 
                                   parents, 
                                   None) 
        self.crossover_done = True
        
    def mutation(self):
        for x in self.next_generation:
            self.mutation_wages(x)
        self.mutation_done = True

    def prep_for_next_gen(self):
        if len(self.best_individuals) > 0:
            self.elite_individual = self.best_individuals[0]
            print("tutaj jest wartosc elity")
            print(len(self.elite_individual.get_player_moves()))
            print("tutaj jest wartosc elity")
        self.actual_generation = self.next_generation
        self.next_generation = []
        self.best_individuals = []
        self.all_moves = True
        self.fitness_done = False
        self.crossover_done = False
        self.mutation_done = False
        self.all_landed = False
       

    def alg_end(self, final_object):
        for x in self.actual_generation:
            if pygame.Rect.colliderect(x.get_player_rect(), final_object.get_rect()):
                print(x.get_player_moves())

    def all_made_moves(self):
        self.all_moves = True
        for x in self.actual_generation:
            if len(x.get_player_moves())-1 > x.get_player_did_moves():
                self.all_moves = False
        return self.all_moves
    
    def all_landed_func(self):
        self.all_landed = True 
        for x in self.actual_generation:
            self.all_landed = x.get_player_landed()
        return self.all_landed





            