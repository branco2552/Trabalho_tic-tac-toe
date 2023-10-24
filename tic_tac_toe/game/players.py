import abc #Classes base abstratas
import time

from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.minimax import find_best_move
from tic_tac_toe.logic.models import GameState, Mark, Move


class Player(metaclass=abc.ABCMeta): #Metaclasse: permite outra classe ser instanciada como objeto"""
    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    def make_move(self, game_state: GameState) -> GameState:
        if self.mark is game_state.current_mark:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("Nao existem mais movimentos possiveis")
        else:
            raise InvalidMove("E o turno do outro jogador")

    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Retornar o movimento do computador no estado atual."""


class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark, delay_seconds: float = 0.25) -> None:
        super().__init__(mark)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Retornar o movimento do computador no estado atual."""


class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return game_state.make_random_move()


class MinimaxComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        if game_state.game_not_started:
            return game_state.make_random_move()
        else:
            return find_best_move(game_state)
