class Score:
    def __init__(self, set_scores=None):
        # set_scores should be a dictionary like {"set1": {"player_a": 6, "player_b": 3}, ...}
        self.set_scores = set_scores if set_scores is not None else {}

    def __add_set_score(self, set_name, player_a_score, player_b_score):
        self.set_scores[set_name] = {"player_a": player_a_score, "player_b": player_b_score}
    
    def add_first_set_score(self,player_a_score, player_b_score):
        self.__add_set_score("set1", player_a_score, player_b_score)
    
    def add_second_set_score(self,player_a_score, player_b_score):
        self.__add_set_score("set2", player_a_score, player_b_score)
    
    def add_third_set_score(self,player_a_score, player_b_score):
        self.__add_set_score("set3", player_a_score, player_b_score)
    
    def add_fourth_set_score(self,player_a_score, player_b_score):
        self.__add_set_score("set4", player_a_score, player_b_score)

    def add_fifth_set_score(self,player_a_score, player_b_score):
        self.__add_set_score("set5", player_a_score, player_b_score)

    def to_dict(self):
        return self.set_scores

    def __str__(self):
        return str(self.set_scores)
