from player_class_ai import Player
import random
import pygame

class Evolutionary_alghoritm():
    def __init__(self, number) -> None:
        self.size_of_generation = number
        self.mutation_rate = 0.2
        self.generation = 1
        self.actual_best_score = 0
        self.actual_generation = []
        self.next_generation: []
        self.best_individuals = []
        self.all_moves = True
        self.fitness_done = False
        self.crossover_done = False
        self.mutation_done = False

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
                x += random.randint(0,2)
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
        list_of_players = []
        if self.generation > 1 and len(self.best_individuals) > 1 and parents is not None:
            parent_a, parent_b = parents
            for x in range(how_many):
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            random.choice([parent_a.player_get_wages(), parent_b.player_get_wages()]))
                new_player.player_update_moves(random.choice([parent_a.get_player_moves(), parent_b.get_player_moves()]))
                self.create_moves(new_player)
                list_of_players.append(new_player)
            self.next_generation = list_of_players
        elif self.generation == 1 and parents is None: 
            for x in range(self.size_of_generation):
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            [1,1,1,1,1])
                self.create_moves(new_player)
                list_of_players.append(new_player)
            self.actual_generation = list_of_players
        elif self.generation > 1 and parents is None:
            for x in range(how_many):
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            [1,1,1,1,1])
                self.create_moves(new_player)
                for y in range(how_many_seq):
                    new_player.player_add_new_seq(self.create_moves())
                list_of_players.append(new_player)
            self.next_generation = list_of_players

    def fitness_n_selection(self):
        best_indyviduals = sorted(self.actual_generation, 
                                  key=lambda x: 680-x.get_player_rect().bottom + (x.get_player_current_map_id()*680), 
                                  reverse=True)
        for x in best_indyviduals:
            if x.get_player_rect().bottom > self.actual_best_score:
                self.best_individuals.append(x)
        self.fitness_done = True
    
    def crossover(self, actual_map, actual_map_id):
        number_of_individuals = len(self.best_individuals)
        if number_of_individuals > 1:
            if self.best_individuals % 2 == 1:
                self.best_individuals.remove(number_of_individuals-1)
            number_of_pairs = number_of_individuals / 2
            for x in range(0, number_of_individuals, 2):
                parents = (self.best_individuals[x], self.best_individuals[x+1])
                self.create_population(actual_map, actual_map_id, (int(0.9*self.size_of_generation)/number_of_pairs), parents)
        if number_of_individuals == 1:
            parents = (self.best_individuals[0], self.best_individuals[0])
            self.create_population(actual_map, actual_map_id, (int(0.9*self.size_of_generation)), parents)
        if self.size_of_generation > len(self.next_generation):
            self.create_population(actual_map, 
                                   actual_map_id, 
                                   self.size_of_generation - len(self.next_generation), 
                                   None, 
                                   len(self.next_generation[0].get_player_moves())/5)
        self.crossover = True
        
    def mutation(self):
        for x in self.next_generation:
            self.mutation_wages(x)
        self.mutation_done = True

    def prep_for_next_gen(self,):
        self.actual_generation = self.next_generation
        self.next_generation = []
        self.best_individuals = []
        self.all_moves = True
        self.fitness_done = False
        self.crossover_done = False
        self.mutation_done = False
        self.generation += 1

    def alg_end(self, final_object):
        for x in self.actual_generation:
            if pygame.Rect.colliderect(x.get_player_rect(), final_object.get_rect()):
                print(x.get_player_moves())

    def all_made_moves(self):
        self.all_moves = True
        for x in self.actual_generation:
            if len(x.get_player_moves()) != x.get_player_did_moves():
                self.all_moves = False
        return self.all_moves





            