import unittest
from simulador_drones import dist, estimate_min_route, Order, allocate_trips

class TestSimuladorDrones(unittest.TestCase):

    def test_dist(self):
        self.assertEqual(dist((0,0),(3,4)), 5)

    def test_estimate_min_route_single(self):
        d = estimate_min_route((0,0), [(3,4)])
        self.assertEqual(d, 10)  # ida e volta

    def test_allocate_single_order_valid(self):
        orders = [Order(1, 1, 1, 1.0, "alta")]
        trips = allocate_trips(orders, drone_capacity=5.0, drone_range_km=20.0)
        self.assertEqual(len(trips), 1)
        self.assertEqual(len(trips[0].orders), 1)

    def test_allocate_order_exceeds_capacity(self):
        orders = [Order(1, 1, 1, 10.0, "alta")]  # 10kg excede
        with self.assertRaises(ValueError):
            allocate_trips(orders, drone_capacity=5.0, drone_range_km=20.0)

    def test_allocate_order_exceeds_range(self):
        orders = [Order(1, 50, 0, 1.0, "alta")]  # longe demais
        with self.assertRaises(ValueError):
            allocate_trips(orders, drone_capacity=5.0, drone_range_km=20.0)

if __name__ == '__main__':
    unittest.main()

