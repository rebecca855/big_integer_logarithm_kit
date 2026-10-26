import unittest

from big_integer_logarithm_kit import floor_log_b, IntegerLogarithmError


class TestFloorLogB(unittest.TestCase):
    # --- happy path: exact powers of b ---
    def test_base2_exact_powers(self):
        for k in range(0, 20):
            with self.subTest(k=k):
                self.assertEqual(floor_log_b(2 ** k, 2), k)

    def test_base10_exact_powers(self):
        for k in range(0, 20):
            with self.subTest(k=k):
                self.assertEqual(floor_log_b(10 ** k, 10), k)

    def test_base16_exact_powers(self):
        for k in range(0, 16):
            with self.subTest(k=k):
                self.assertEqual(floor_log_b(16 ** k, 16), k)

    # --- floor behaviour: n between consecutive powers ---
    def test_base2_floor_between_powers(self):
        self.assertEqual(floor_log_b(7, 2), 2)
        self.assertEqual(floor_log_b(8, 2), 3)
        self.assertEqual(floor_log_b(9, 2), 3)
        self.assertEqual(floor_log_b(15, 2), 3)
        self.assertEqual(floor_log_b(16, 2), 4)

    def test_base10_floor_between_powers(self):
        self.assertEqual(floor_log_b(9, 10), 0)
        self.assertEqual(floor_log_b(10, 10), 1)
        self.assertEqual(floor_log_b(99, 10), 1)
        self.assertEqual(floor_log_b(100, 10), 2)
        self.assertEqual(floor_log_b(101, 10), 2)
        self.assertEqual(floor_log_b(999, 10), 2)

    def test_base3_small(self):
        self.assertEqual(floor_log_b(1, 3), 0)
        self.assertEqual(floor_log_b(2, 3), 0)
        self.assertEqual(floor_log_b(3, 3), 1)
        self.assertEqual(floor_log_b(8, 3), 1)
        self.assertEqual(floor_log_b(9, 3), 2)
        self.assertEqual(floor_log_b(26, 3), 2)
        self.assertEqual(floor_log_b(27, 3), 3)

    # --- large n: the actual reason this library exists ---
    def test_huge_base10(self):
        # 10 ** 1000 - 1 still floors to 999
        self.assertEqual(floor_log_b(10 ** 1000 - 1, 10), 999)
        self.assertEqual(floor_log_b(10 ** 1000, 10), 1000)
        self.assertEqual(floor_log_b(10 ** 1000 + 1, 10), 1000)

    def test_huge_base2(self):
        self.assertEqual(floor_log_b(2 ** 5000 - 1, 2), 4999)
        self.assertEqual(floor_log_b(2 ** 5000, 2), 5000)
        self.assertEqual(floor_log_b(2 ** 5000 + 1, 2), 5000)

    def test_huge_base7(self):
        self.assertEqual(floor_log_b(7 ** 300 - 1, 7), 299)
        self.assertEqual(floor_log_b(7 ** 300, 7), 300)
        self.assertEqual(floor_log_b(7 ** 300 + 1, 7), 300)

    # --- n == 1, the degenerate-but-defined case ---
    def test_n_one_is_zero(self):
        for b in (2, 3, 10, 16, 100):
            with self.subTest(b=b):
                self.assertEqual(floor_log_b(1, b), 0)

    # --- error handling: these ARE implemented, so we test them ---
    def test_n_zero_raises(self):
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(0, 2)

    def test_n_negative_raises(self):
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(-5, 2)

    def test_base_one_raises(self):
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(10, 1)

    def test_base_zero_raises(self):
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(10, 0)

    def test_base_negative_raises(self):
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(10, -2)

    def test_bool_arguments_rejected(self):
        # bool is a subclass of int; we explicitly exclude it so callers
        # don't silently get log-base-True.
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(10, True)
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(False, 2)

    def test_non_int_n_rejected(self):
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(2.5, 2)
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b("16", 2)

    def test_non_int_b_rejected(self):
        with self.assertRaises(IntegerLogarithmError):
            floor_log_b(16, 2.0)

    # --- type of the return value ---
    def test_returns_python_int(self):
        result = floor_log_b(1024, 2)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 10)


if __name__ == "__main__":
    unittest.main()
