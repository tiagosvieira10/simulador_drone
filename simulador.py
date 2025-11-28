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

# Distância
def dist(a: Tuple[float,float], b: Tuple[float,float]) -> float:
    return math.hypot(a[0]-b[0], a[1]-b[1])

# Calcula distância total de rota dado uma sequência de pontos
def route_distance_from_sequence(depot: Tuple[float,float], sequence: List[Tuple[float,float]]) -> float:
    total = 0.0
    prev = depot
    for p in sequence:
        total += dist(prev, p)
        prev = p
    total += dist(prev, depot)
    return total

# Estima a menor rota possível para um conjunto de pontos

def estimate_min_route(depot: Tuple[float,float], points: List[Tuple[float,float]]) -> float:
    n = len(points)
    if n == 0:
        return 0.0
    
    if n <= 8:
        best = float('inf')
        for perm in itertools.permutations(points):
            d = route_distance_from_sequence(depot, list(perm))
            if d < best:
                best = d
        return best
    
    best = float('inf')
    for start_idx in range(min(5, n)):
        unvisited = points.copy()
        seq = []
        current = depot
        
        p = unvisited.pop(start_idx)
        seq.append(p)
        current = p
        while unvisited:
            
            nearest_idx = min(range(len(unvisited)), key=lambda i: dist(current, unvisited[i]))
            current = unvisited.pop(nearest_idx)
            seq.append(current)
        d = route_distance_from_sequence(depot, seq)
        if d < best:
            best = d
    return best



def allocate_trips(orders: List[Order], drone_capacity: float, drone_range_km: float, depot=(0.0,0.0)) -> Tuple[List[Trip], List[List[Trip]]]:

    orders_sorted = sorted(orders, key=lambda o: (PriorityOrder.get(o.priority, 2), dist(depot, o.coord())))

    trips: List[Trip] = []

    for o in orders_sorted:
        placed = False

        trips_sorted = sorted(trips, key=lambda t: (drone_capacity - t.total_weight))
        for t in trips_sorted:
            if t.total_weight + o.weight > drone_capacity:
                continue
        
            pts = [order.coord() for order in t.orders] + [o.coord()]
            est = estimate_min_route(depot, pts)
            if est <= drone_range_km + 1e-9:
                t.add_order(o)
                placed = True
                break
        if not placed:
          
            single_route = estimate_min_route(depot, [o.coord()])
            if o.weight <= drone_capacity and single_route <= drone_range_km + 1e-9:
                newt = Trip()
                newt.add_order(o)
                trips.append(newt)
            else:
                
                raise ValueError(f"Order {o.id} cannot be served: weight {o.weight} or single-route {single_route:.2f}km exceeds drone limits")

    return trips


def assign_trips_to_drones(trips: List[Trip], drones_count: int) -> List[List[Trip]]:
    drones = [[] for _ in range(drones_count)]
    counts = [0]*drones_count
    for t in trips:
        idx = min(range(drones_count), key=lambda i: counts[i])
        drones[idx].append(t)
        counts[idx] += 1
    return drones


def summarize_allocation(trips: List[Trip], drones_allocation: List[List[Trip]], depot=(0,0)):
    print(f"Total trips: {len(trips)}")
    for i, drone_trips in enumerate(drones_allocation):
        print(f"\nDrone {i+1} - {len(drone_trips)} trips")
        for j, t in enumerate(drone_trips, start=1):
            coords = [o.coord() for o in t.orders]
            ids = [o.id for o in t.orders]
            w = t.total_weight
            est = estimate_min_route(depot, coords)
            print(f"  Trip {j}: orders={ids}, weight={w:.2f}kg, est_route={est:.2f}km, coords={coords}")

# Exemplo de uso com dados amostrais
if __name__ == '__main__':
    
    DRONES_COUNT = 3
    DRONE_CAPACITY = 5.0  # kg
    DRONE_RANGE_KM = 20.0  # km/carga
    DEPOT = (0.0, 0.0)

    # Gerar pedidos de exemplo
    random.seed(42)
    orders_sample: List[Order] = []
    for i in range(1, 21):
        x = random.uniform(-6, 6)
        y = random.uniform(-6, 6)
        weight = random.choice([0.5, 1.0, 1.5, 2.0])
        priority = random.choices(["alta", "media", "baixa"], weights=[0.2,0.3,0.5])[0]
        orders_sample.append(Order(id=i, x=x, y=y, weight=weight, priority=priority))

    print("Parâmetros:")
    print(f"  drones={DRONES_COUNT}, capacity={DRONE_CAPACITY}kg, range={DRONE_RANGE_KM}km\n")

    try:
        trips = allocate_trips(orders_sample, DRONE_CAPACITY, DRONE_RANGE_KM, depot=DEPOT)
        drones_alloc = assign_trips_to_drones(trips, DRONES_COUNT)
        summarize_allocation(trips, drones_alloc, depot=DEPOT)
    except ValueError as e:
        print("Erro ao alocar pedidos:", e)
