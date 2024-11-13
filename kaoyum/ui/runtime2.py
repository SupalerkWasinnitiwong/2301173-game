import pygame
from pygame import Rect, Surface
from pygame.event import Event
from typing import Self
from itertools import zip_longest
from kaoyum.utils import add
from .core import UINode, Constraints
from .widget.core import Widget, StatefulWidget
from .state import State
from .widget.input import GestureHandler
from ..assets_manager import AssetsManager

# it mean we will have to diff these trees 3 times
# Definitions Tree -> Reattach State (rebuild if needed) -> Layout (handling event????) -> Composite 
# TODO: Event handling: set a listener to some rect area and call the callback if the event is in the rect area
# Definitions:
#   - from build() method
# State reattaching:
#   - Should call create state() method of StatefulWidget
#   - extract state from StatefulWidget and store it in StateNode
#   - reattach the state to the StatefulWidget with the same key if any or else same position 
# Layouting:
#   - how to layout the nodes
#   - children report their constraints to the parent (measure() will not take any argument)
#   - parent decides the children's size and position
#   - fill_max_size handling: constraints.min_size = inf
#   - PARENT UI NODE MUST REPORT THE CHILDREN PLACEMENT after it's got it's size determined : layout(w, h)
#     - must take fill_max_size into account (via min_size inf)

# Node list:
#   - UINode
#   - UIText
#   - SizedNode
#   - Box
#   - Stack
    #   - VStack
    #   - HStack
#   - StatefulWidget
#   - GestureHandler
class RenderTextureRegistry:
    # TODO: texture recycling
    pass

class ImmediateNode:
    def __init__(self, node: UINode):
        self.node = node
        self.state = node.state if isinstance(node, StatefulWidget) else None
        self.surface = None

    def resize(self, size: tuple[int, int]):
        # TODO: check if we can reuse the surface 
        if self.surface is None:
            self.surface = Surface(size, pygame.SRCALPHA, 32)
        else:
            # TextureRegistry.recycle(self.surface)
            self.surface = Surface(size, pygame.SRCALPHA, 32)

        # check node type before reattaching the state

class UIRuntime2:
    def __init__(self, root: Widget, size: tuple[int, int], draw_bound: bool = False):
        self.root_node = root
        self.root_immediate_node = None
        self.draw_bound = draw_bound
        self.size = size
        self.compositor.render()

    def diff(self, node: UINode):
        if self.root_immediate_node is None:
            self.root_immediate_node = ImmediateNode(self.root_node)

    def reattach_state(self, node: UINode):
        if isinstance(node, StatefulWidget):
            node.create_state()
            node.state = node.state

    def layout(self, node: UINode):
        if isinstance(node, Widget):
            node.layout()

    def composite(self, node: UINode):
        pass
