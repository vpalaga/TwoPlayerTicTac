from Server import host, join
from Game import Playground, Pos
from Vis import Graphic
# Player.py
import select


class Player:
    def __init__(self, is_host:bool=False, ip:str="localhost"):
        self.my_player_num:int = 0 if is_host else 1
        self.other_player_num:int = 1 if is_host else 0

        self.is_my_turn:bool = True if is_host else False

        if is_host:
            self.conn = host()
        else:
            self.conn = join(ip) # replace with ip

        self.game = Playground((20,20),(800,800))
        self.pygame = Graphic(self.game, self.my_player_num)

    def send_move(self, move:Pos):
        self.conn.send({"type": "move", "value": move.xy})

    def receive_move(self)->Pos:
        msg = self.conn.recv()
        print(msg)
        print(msg["value"])
        xy = msg["value"]
        return Pos(xy[0], xy[1])

    def play_move(self, mv:Pos)->None:
        self.game.add_move(mv, self.my_player_num)
        self.send_move(mv)
        self.is_my_turn = False

    def poll_opponent(self):
        r, _, _ = select.select([self.conn.sock], [], [], 0)
        if r:
            self.receive_move_and_apply()

    def receive_move_and_apply(self)->None:
        other_move:Pos = self.receive_move()
        self.game.add_move(other_move, self.other_player_num)
        self.is_my_turn = True
