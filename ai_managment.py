from player_class_ai import Player
import random
import pygame
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
        self.elite_individuals = []
        self.ultimate_individual = None
        self.fitness_done = False
        self.crossover_done = False
        self.mutation_done = False
        self.go_next = False
        self.was_bigger = False
        self.showout = False
        self.testing = False
        self.testing_done = False
    def get_ultimate_individual(self):
        return self.ultimate_individual
    def get_showout(self):
        return self.showout
    def get_elite(self):
        return self.elite_individuals
    def get_generation(self):
        return self.generation
    def get_mutation_done(self):
        return self.mutation_done
    def get_crossover_done(self):
        return self.crossover_done
    def get_fitness_done(self):
        return self.fitness_done
    def get_actual_gen(self):
        return self.actual_generation
    def get_go_next(self):
        self.go_next = True
        for x in self.actual_generation:
            if not x.get_go_next():
                self.go_next = False
        return self.go_next     
    def mutation_wages(self, player):
        decide_number = random.randint(1,100)
        wages = []
        if decide_number < self.mutation_rate*100:
            for x in player.get_player_wages():
                if x > 1:
                    x += random.randint(-1, 1)
                    wages.append(x)
                else:
                    x += random.randint(0, 1)
                    wages.append(x)
            player.set_player_wages(wages)
        else:
            wages.append(player.get_player_wages())
    def create_wages(self):
        wages = []
        for x in range(3):
            wage = random.randint(1, 4)
            wages.append(wage)
        wages.append(1)
        wages.append(1)
        return wages
    def create_moves(self, player):
        player_movments = [(1,0,1), (1,0,0), (1,1,0), (0,1,0), (0,0,1)]
        wages = player.get_player_wages()
        player.set_player_moves([])
        for y in range(3):
            player.player_add_new_move([random.choices(player_movments, wages)[0], random.randint(200,2000)])  
    def create_population(self, actual_map, actual_map_id, how_many=None, parents=None, how_many_seq=None):
        if self.generation > 0 and parents is not None:
            for x in range(how_many):
                parent_a, parent_b = parents
                gen_parent =  random.choice([parent_a, parent_b])
                gen_parent_moves = copy.deepcopy(gen_parent.get_parent_moves())
                new_player = Player(
                            gen_parent.get_player_current_map(),
                            gen_parent.get_player_current_map_id(),
                            gen_parent.get_player_wages())
                self.next_generation.append(new_player)
                new_player.set_parent_moves(gen_parent_moves)
                new_player.update_rect(gen_parent.get_player_xy())
                self.create_moves(new_player)
                
        elif how_many_seq is None and parents is None and how_many is None: 
            for x in range(self.size_of_generation):
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            self.create_wages())
                self.create_moves(new_player)
                if self.generation == 0:
                    self.actual_generation.append(new_player)
                else:
                    self.next_generation.append(new_player)              
    def fitness_n_selection(self):
        self.generation += 1
        best_indyviduals = sorted(self.actual_generation, 
                                  key=lambda x: 680-x.get_player_rect().bottom + (x.get_player_current_map_id()*680), 
                                  reverse=True)
        if len(best_indyviduals) > 0:
            if best_indyviduals[0].get_value() - self.actual_best_score > 0:
                for x in best_indyviduals:
                    if x.get_value() >= best_indyviduals[0].get_value():
                        self.best_individuals.append(x)
                        moves_to_add = copy.deepcopy(x.get_player_moves())
                        x.add_parent_moves(moves_to_add)
                self.actual_best_score = best_indyviduals[0].get_value()
        self.fitness_done = True   
    def crossover(self, actual_map, actual_map_id):
        def more_parents(how_many, list_of_parents):
            if how_many % 2 == 1:
                list_of_parents.remove(list_of_parents[-1])
            how_many = len(list_of_parents)
            number_of_pairs = how_many / 2
            how_many_pep = int(self.size_of_generation/number_of_pairs)
            left = int(self.size_of_generation - (number_of_pairs*how_many))
            for x in range(0, how_many, 2):
                parents = (list_of_parents[x], list_of_parents[x+1])
                self.create_population(actual_map, actual_map_id, how_many_pep, parents)
            if left>0:
                parents = (list_of_parents[0], list_of_parents[1])
                self.create_population(actual_map, actual_map_id, left, parents)
        
        number_of_individuals = len(self.best_individuals)
        if number_of_individuals > 1:
            more_parents(number_of_individuals, self.best_individuals)
        if number_of_individuals == 1:
            seccond_parent = copy.copy(self.best_individuals[0])
            parents = (self.best_individuals[0], seccond_parent)
            self.create_population(actual_map, actual_map_id, self.size_of_generation, parents)
        if self.size_of_generation > len(self.next_generation) and len(self.best_individuals) > 0:
            self.create_population(actual_map, 
                                   actual_map_id, 
                                   self.size_of_generation - len(self.next_generation), 
                                   None, 
                                   None)
        if len(self.best_individuals) == 0:
            if len(self.elite_individuals) == 1:
                seccond_parent = copy.copy(self.elite_individuals[0])
                parents = self.elite_individuals[0], seccond_parent
                self.create_population(actual_map, 
                                    actual_map_id, 
                                    self.size_of_generation, 
                                    parents, 
                                    None) 
            elif len(self.elite_individuals) > 1:
                ammount_elites = len(self.elite_individuals)
                more_parents(ammount_elites, self.elite_individuals)                       
        self.crossover_done = True        
    def mutation(self):
        for x in self.next_generation:
            self.mutation_wages(x)
        self.mutation_done = True
    def prep_for_next_gen(self):
        if len(self.best_individuals) > 0:
            self.elite_individuals = []
            for x in self.best_individuals:
                self.elite_individuals.append(x)
            for x in self.elite_individuals:
                print(self.generation)
                print(x.get_parent_moves())
        self.actual_generation = self.next_generation
        self.next_generation = []
        self.best_individuals = []
        self.fitness_done = False
        self.crossover_done = False
        self.mutation_done = False
        self.go_next = False 
        self.testing = False
        self.testing_done = False
    def alghoritm_end(self, map, final_object):
        for x in self.actual_generation:
            if pygame.Rect.colliderect(x.get_player_rect(), final_object.get_rect()) and map == x.get_player_current_map():
                if x.get_player_landed() and not x.get_player_steping():
                    self.showout = True
                    self.ultimate_individual = x 
                    ultimate_moves = copy.deepcopy(self.ultimate_individual.get_player_moves())
                    self.ultimate_individual.add_parent_moves(ultimate_moves)
                    moves_did = self.ultimate_individual.get_player_did_moves()
                    print("ile ruchow zrobil : " + str(moves_did))
                    print("przed usunieciem : "+ str(len(self.ultimate_individual.get_parent_moves())))
                    if moves_did==2:
                        to_delete = 0 
                    else:
                        to_delete = 3-moves_did
                    for y in range(to_delete):
                        self.ultimate_individual.rem_last_parent_move()
                    print("przed usunieciem : "+ str(len(self.ultimate_individual.get_parent_moves())))
                    with open('Sequence_that_solved_game.txt', 'w') as file:
                        for item in x.get_parent_moves():
                            file.write(str(item)+'\n')   
                    print("now, new guy ")      
    def ultimate_indyvidual(self, map_name, map_id):
        self.actual_generation = []
        new_player = Player(
                            map_name,
                            map_id,
                            self.ultimate_individual.get_player_wages())
        self.actual_generation.append(new_player)
        new_player.set_player_moves(self.ultimate_individual.get_parent_moves())
    def create_moves_from_file(self, filename):
        lines = []
        lines_after_ev = []
        with open(filename, 'r') as plik:
            lines = plik.readlines()
        for x in lines:
            lines_after_ev.append(eval(x))
        return lines_after_ev
    def create_from_file(self, map_name, map_id):
        self.actual_generation = []
        new_player = Player(
                            map_name,
                            map_id,
                            self.create_wages())
        self.actual_generation.append(new_player)
        new_player.set_player_moves(self.create_moves_from_file("Sequence_that_solved_game.txt"))
        self.showout = True

    def testing_if(self, map_name, map_id):
        self.next_generation = self.actual_generation
        self.actual_generation = []
        self.go_next = False
        self.testing = True
        self.testing_done = False
        which_list = []
        if len(self.best_individuals) > 0:
            which_list = self.best_individuals
        else:
            which_list = self.elite_individuals

        for x in which_list:
            moves = x.parent_moves
            new_player = Player(
                            map_name,
                            map_id,
                            self.create_wages())
            self.actual_generation.append(new_player)
            new_player.set_player_moves(moves)
        

    def testing_done_func(self):
        self.actual_generation = self.next_generation
        self.next_generation = []
        self.testing = False
        self.testing_done = True
