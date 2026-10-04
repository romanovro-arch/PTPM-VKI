import unittest
from Delivery import calculate_delivery_cost


class TestDeliveryService(unittest.TestCase):

    def test_standard_delivery_light_package(self):
        cost, delivery_date = calculate_delivery_cost(2.0, 100, "обычный", False)
        self.assertEqual(cost, 700)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_standard_delivery_medium_weight(self):
        cost, delivery_date = calculate_delivery_cost(10.0, 200, "обычный", False)
        self.assertEqual(cost, 1440)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_standard_delivery_heavy_weight(self):
        cost, delivery_date = calculate_delivery_cost(25.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_fragile_package_surcharge(self):
        cost, delivery_date = calculate_delivery_cost(3.0, 100, "хрупкий", False)
        self.assertEqual(cost, 1000)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_dangerous_package_surcharge(self):
        cost, delivery_date = calculate_delivery_cost(4.0, 100, "опасный", False)
        self.assertEqual(cost, 1700)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_long_distance_transit_days(self):
        cost, delivery_date = calculate_delivery_cost(2.0, 1500, "обычный", False)
        self.assertEqual(cost, 7700)
        self.assertEqual(delivery_date, "2026-09-06")

    def test_boundary_min_weight(self):
        cost, delivery_date = calculate_delivery_cost(0.1, 10, "обычный", False)
        self.assertEqual(cost, 250)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_boundary_max_weight(self):
        cost, delivery_date = calculate_delivery_cost(50.0, 10, "обычный", False)
        self.assertEqual(cost, 375)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_boundary_min_distance(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 1, "обычный", False)
        self.assertEqual(cost, 205)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_boundary_max_distance(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 5000, "обычный", False)
        self.assertEqual(cost, 25200)
        self.assertEqual(delivery_date, "2026-09-13")

    def test_weight_threshold_5kg(self):
        cost, delivery_date = calculate_delivery_cost(5.0, 100, "обычный", False)
        self.assertEqual(cost, 700)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_weight_threshold_20kg(self):
        cost, delivery_date = calculate_delivery_cost(20.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_invalid_weight_below_min(self):
        cost, delivery_date = calculate_delivery_cost(0.05, 100, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(delivery_date, "0000-00-00")

    def test_invalid_weight_negative(self):
        cost, delivery_date = calculate_delivery_cost(-5.0, 100, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(delivery_date, "0000-00-00")

    def test_invalid_weight_above_max(self):
        cost, delivery_date = calculate_delivery_cost(50.1, 100, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(delivery_date, "0000-00-00")

    def test_invalid_distance_zero(self):
        cost, delivery_date = calculate_delivery_cost(5.0, 0, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(delivery_date, "0000-00-00")

    def test_invalid_distance_negative(self):
        cost, delivery_date = calculate_delivery_cost(5.0, -100, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(delivery_date, "0000-00-00")

    def test_invalid_distance_above_max(self):
        cost, delivery_date = calculate_delivery_cost(5.0, 5001, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(delivery_date, "0000-00-00")

    def test_invalid_package_type(self):
        cost, delivery_date = calculate_delivery_cost(5.0, 100, "документы", False)
        self.assertEqual(cost, -1)
        self.assertEqual(delivery_date, "0000-00-00")

    # Тесты, выявляющие дефекты в реализации Delivery.py
    def test_express_delivery_cost_surcharge(self):
        cost_std, _ = calculate_delivery_cost(2.0, 100, "обычный", False)
        cost_exp, _ = calculate_delivery_cost(2.0, 100, "обычный", True)
        self.assertGreater(
            cost_exp,
            cost_std,
            "Экспресс-доставка должна быть дороже стандартной, а не со скидкой 50%"
        )

    def test_express_delivery_minimum_one_day(self):
        _, delivery_date = calculate_delivery_cost(2.0, 100, "обычный", True)
        self.assertEqual(
            delivery_date,
            "2026-09-04",
            "Срок экспресс-доставки должен составлять не менее 1 дня, а не 0 дней (день в день 2026-09-03)"
        )

    def test_package_type_case_insensitivity(self):
        cost, delivery_date = calculate_delivery_cost(2.0, 100, "Обычный", False)
        self.assertEqual(
            cost,
            700,
            "Тип посылки должен обрабатываться без учета регистра"
        )

    def test_invalid_input_types_graceful_handling(self):
        cost, delivery_date = calculate_delivery_cost("десять", 100, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(delivery_date, "0000-00-00")


if __name__ == "__main__":
    unittest.main()
