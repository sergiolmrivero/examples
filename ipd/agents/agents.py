# -*- coding: utf-8 -*-
""" Agents for the iterated prisioners dilemma model """
from EcoSimpy import DiscreteEventAgent
from .ipd_action_set import *


class Player(DiscreteEventAgent):
    """ A basic player in the Iterated Prisioners Dilemma """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.my_payoff = 0
        self.my_play = "C"
        self.other_name = ""
        self.other_play = "C"
        self.other_payoff = 0
        self.strategy = Strategy()
        self.game = Game(self.name, "C", 3, "", "C", 3)
        self.strategy.update_game(self.game)
        self.mean_payoff = 0

    def step(self):
        """ The agent selects a play from a strategy """
#        self.select_game()
        self.update_mean_payoff()

    def play(self):
        """ The agent plays a strategy """
        return self.my_play

    def game_payoff(self, other_name, other_play, other_payoff, my_payoff):
        """ Get the game payoff """
        self.my_payoff = my_payoff
        self.other_name = other_name
        self.other_play = other_play
        self.other_payoff = other_payoff
        self.game.my_payoff = my_payoff
        self.game.other_name = other_name
        self.game.other_play = other_play
        self.game.other_payoff = other_payoff
        self.strategy.update_game(self.game)
    
    def select_game(self, other_player):
        """ The player selects it's game"""
        self.my_play = self.strategy.select_game(other_player)

    def update_mean_payoff(self):
        """ The player calculates it's average payoff """
        self.mean_payoff = (self.mean_payoff + self.my_payoff)/2

    
class GoodPlayer(Player):
    """ A player that always cooperate """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = AlwaysCooperate()


class BadPlayer(Player):
    """ A player that always defect """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = AlwaysDefect()



class RandomPlayer(Player):
    """ A player that randomly plays """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = RandomPlay()


class TitForTatPlayer(Player):
    """ Tit for tat player """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = SimpleTitForTat()


class TitForTatWithRecallPlayer(Player):
    """ Tit for tat player """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = TitForTat()

class RancorousPlayer(Player):
    """ Rancorous player """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = SimpleRancorous()


class RancorousWithRecallPlayer(Player):
    """ Rancorous player - Impl: Lucas 2023-10-25 """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = Rancorous()

class GenericStrategyPlayer(Player):
    """Implemnts a player with memory and generic strategies"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = Generic()
        self.memory = Memory()

#Nathan
class PeriodicPlayer(Player):
    """ Periodic player C, D """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = PerCD()

class HardTitForTatPlayer(Player):
    """ Hard Tit for tat player """
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = HardTitForTat()

class SlowTitForTatPlayer(Player):
    """Slow Tit for Tat Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = SlowTitForTat()

class TitFor2TatPlayer(Player):
    """Tit For 2 Tat Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = TitFor2Tat()

class GradualPlayer(Player):
    """Gradual Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = Gradual()
#FIM

class PavlovPlayer(Player):
    """Pavlov Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = Pavlov()

class ProberPlayer(Player):
    """Prober Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = Prober()

#Novas

class MistrustPlayer(Player):
    """Mistrust Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = Mistrust()

class SoftMajorityPlayer(Player):
    """ SoftMajority Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = SoftMajority()


class HardMajorityPlayer(Player):
    """ HardMajority Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = HardMajority()

class MemPlayer(Player):
    """ Mem Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = Mem()

class ZDEqualizerPlayer(Player):
    """ZD Equalizer Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = ZDEqualizer()


class ZDExtortionPlayer(Player):
    """ZD Extortion Player"""
    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
        self.strategy = ZDExtortion()