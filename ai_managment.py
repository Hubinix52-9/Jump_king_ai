from player_class_ai import Player
import random

class Evolutionary_alghoritm():
    def __init__(self, number) -> None:
        self.size_of_generation = number
        self.mutation_rate = 0.2
        self.generation = 1
        self.actual_best_score = 0
        self.actual_generation = []
        self.best_individuals = []

    def mutation_wages(self, player):
        decide_number = random.randint(1,100)
        wages = []
        if decide_number > self.mutation_rate*100:
            for x in player.player_get_wages():
                x += random.randint(0,1)
                wages.append(x)
            player.player_update_wages(wages)
        else:
            wages.append(player.player_get_wages())

    def create_moves_seq(self, player):
        player_movments = [(1,0,1), (1,0,0), (1,1,0), (0,0,1), (0,1,0)]
        wages = player.player_get_wages()
        sek = []
        for y in range(5):
            sek.append([random.choices(player_movments, wages)[0], random.randint(200,2000)])
        return sek
    
    def create_population(self, actual_map, actual_map_id, how_many, parents=None):
        list_of_players = []
        if self.generation > 1 and len(self.best_individuals) > 1 and parents is not None:
            parent_a, parent_b = parents
            for x in range(how_many):
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            random.choice([parent_a.player_get_wages(), parent_b.player_get_wages()]),
                            random.choice([parent_a.get_player_moves(), parent_b.get_player_moves()]))
                new_player.player_add_new_seq(self.create_moves_seq())
                list_of_players.append(new_player)
            self.actual_generation.append(list_of_players)
        elif self.generation == 1 and parents is None: 
            for x in range(self.size_of_generation):
                new_player = Player(
                            actual_map,
                            actual_map_id,
                            [1,1,1,1,1],
                            self.create_moves_seq())
                list_of_players.append(new_player)
            self.actual_generation.append(list_of_players)
        return list_of_players
    
    def fitness_n_selection(self):
        best_indyviduals = sorted(self.actual_generation, key=lambda x: x.get_player_rect().bottom, reverse=True)
        for x in best_indyviduals:
            if x.get_player_rect().bottom > self.actual_best_score:
                self.best_individuals.append(x)
    
    def crossover(self, actual_map, actual_map_id):
        number_of_individuals = len(self.best_individuals)
        if number_of_individuals > 1:
            if self.best_individuals % 2 == 1:
                self.best_individuals.remove(number_of_individuals-1)
            number_of_pairs = int(number_of_individuals / 2)
            for x in range(0, number_of_individuals, 2):
                parents = (self.best_individuals[x], self.best_individuals[x+1])
                self.create_population(actual_map, actual_map_id, (0.6*self.size_of_generation)/number_of_pairs, )
        if number_of_individuals == 1:
            parents = (self.best_individuals[0], self.best_individuals[0])
            self.create_population(actual_map, actual_map_id, (0.6*self.size_of_generation)/number_of_pairs, )


            