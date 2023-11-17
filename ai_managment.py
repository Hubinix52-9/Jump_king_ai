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
    
    def create_population(self, screen_width, screen_height, actual_map, actual_map_id, wages):
        list_of_players = []
        for x in range(self.size_of_generation):
            sek = self.create_moves_seq()
            new_player = Player(
                        600,
                        screen_height-105,
                        'assets/standing2.png',
                        screen_width,
                        screen_height,
                        actual_map,
                        actual_map_id,
                        wages)
            new_player.set_player_new_seq(sek)
            list_of_players.append(new_player)
        self.actual_generation.append(list_of_players)
        return list_of_players
    
    def fitness_n_selection(self):
        best_indyviduals = sorted(self.actual_generation, key=lambda x: x.get_player_rect().bottom, reverse=True)
        for x in best_indyviduals:
            if x.get_player_rect().bottom > self.actual_best_score:
                self.best_individuals.append(x)
    
    def crossover(self):
        number_of_individuals = len(self.best_individuals)
        if number_of_individuals > 1:
            if self.best_individuals % 2 == 1:
                self.best_individuals.remove(number_of_individuals-1)
                number_of_pairs = number_of_individuals / 2
            