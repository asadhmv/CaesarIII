from typing import TYPE_CHECKING

from buildable.final.structures.granary import Granary
from buildable.house import House
from buildable.final.houses import *
from class_types.buildind_types import BuildingTypes
from class_types.walker_types import WalkerTypes
from game.game_controller import GameController
from walkers.walker import Walker
from enum import Enum

if TYPE_CHECKING:
    from buildable.final.structures.castle import Castle

class Actions(Enum):
    NOTHING = 0
    IN_THE_WAY_TO_CASTLE = 1
    IN_THE_WAY_TO_ATTACK = 2


class Attacker(Walker):
    def __init__(self, associated_building: 'Castle'):
        super().__init__(WalkerTypes.ATTACKER, associated_building, roads_only=True)
        self.associated_building: 'Castle' = associated_building
        self.game_controller = GameController.get_instance()
        self.current_action = Actions.NOTHING
        self.destination = None



    def destination_reached(self):

        if Actions.IN_THE_WAY_TO_ATTACK == self.current_action:
            self.current_tile.get_building().to_ruin()
            self.current_action = Actions.IN_THE_WAY_TO_CASTLE
            tile = self.associated_building.get_all_building_tiles()
            super().navigate_to(tile)

        elif Actions.IN_THE_WAY_TO_CASTLE == self.current_action:
            self.delete()
            self.current_action = Actions.NOTHING
        
        # print(self.current_tile.get_building(), self.current_tile.get_show_tile())
        # building = self.current_tile.get_building()
        

        # if building and building.get_build_type() == BuildingTypes.GRANARY:
        #     self.move_wheat_in_hand_to_granary(building)
        #     self.navigate_to(self.associated_building.get_all_building_tiles())  # back to the castle
        #     self.current_action = Actions.IN_THE_WAY_TO_CASTLE

        # elif building and building.get_build_type() == BuildingTypes.WHEAT_FARM:
        #     self.delete()

    def attackMode(self, dest):
        self.current_action = Actions.IN_THE_WAY_TO_ATTACK
        self.destination = dest
        super().navigate_to(dest)