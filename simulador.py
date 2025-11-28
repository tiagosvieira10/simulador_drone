from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import math
import itertools
import random

PriorityOrder = {"alta": 0, "media": 1, "baixa": 2}

@dataclass
class Order:
    id: int
    x: float
    y: float
    weight: float
    priority: str

    def coord(self) -> Tuple[float,float]:
        return (self.x, self.y)

@dataclass
class Trip:
    orders: List[Order] = field(default_factory=list)
    total_weight: float = 0.0

    def coords(self):
        return [o.coord() for o in self.orders]

    def add_order(self, order: Order):
        self.orders.append(order)
        self.total_weight += order.weight

    def remove_order(self, order: Order):
        self.orders.remove(order)
        self.total_weight -= order.weight

