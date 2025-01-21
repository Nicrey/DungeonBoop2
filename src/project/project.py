from typing import List

from project.layer import Layer


class Project:
    name: str = "DungeonBoopMaps"
    layers: List[Layer] = []
    current_layer: int =  0
    save_path: str = ""

    def __init__(self, name = "DungeonBoopMaps", save_path = ""):
        self.name = name
        self.save_path = save_path

    def switch_layer(self, next=True):
        """
        Switches the layer of the current project to the next layer of previous layer.
        If there is none, does nothing
        Returns the pixels of the now active layer
        """
        if self.current_layer == 0 and not next:
            return self.get_current_layer() 
        if self.current_layer == len(self.layers)-1 and next:
            return self.get_current_layer() 
        self.current_layer+= 1 if next else -1
        return self.get_current_layer() 
    
    def switch_layer_to_specific(self, index):
        self.current_layer = index
        return self.get_current_layer()
    
    def get_current_layer(self):
        """Returns the pixels of the current layer"""
        return self.layers[self.current_layer]

    def new_layer(self, controller):
        new_layer = Layer("Layer" + str(len(self.layers)), controller)
        self.layers.append(new_layer)
