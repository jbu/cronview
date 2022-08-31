import unittest
import cronview


class TestEncoding(unittest.TestCase):
    def test_base(self):
        """
        Test the base crontab spec of "*/15 0 1,15 * 1-5"
        """
        self.assertEqual(
            cronview.generate_times("*/15", "0-59"), ["0", "15", "30", "45"]
        )
        self.assertEqual(cronview.generate_times("0", "0-23"), ["0"])
        self.assertEqual(cronview.generate_times("1,15", "1-31"), ["1", "15"])
        self.assertEqual(
            cronview.generate_times("*", "1-12", name_substs=cronview.month_substs),
            [str(i) for i in range(1, 13)],
        )
        self.assertEqual(
            cronview.generate_times("1-5", "0-7", name_substs=cronview.day_substs),
            [str(i) for i in range(1, 6)],
        )

    def test_name_substs(self):
        """
        Testing name substitutions like tue-thu
        """
        self.assertEqual(
            cronview.generate_times("tue-thu", "0-7", name_substs=cronview.day_substs),
            ["2", "3", "4"],
        )

    def test_sunday(self):
        """
        Sunday can be either 0 or 7. This at least documents the behaviour.
        """
        self.assertEqual(
            cronview.generate_times("sun", "0-7", name_substs=cronview.day_substs),
            ["0"],
        )
        self.assertEqual(
            cronview.generate_times("0", "0-7", name_substs=cronview.day_substs), ["0"]
        )
        self.assertEqual(
            cronview.generate_times("7", "0-7", name_substs=cronview.day_substs), ["7"]
        )

    def test_bad_range(self):
        self.assertRaisesRegex(
            Exception,
            "Time specified outside given range",
            cronview.generate_times,
            "9",
            "0-7",
            name_substs=cronview.day_substs,
        )

    def test_bad_substitution(self):
        self.assertRaisesRegex(
            Exception,
            "Name subtitution failed for",
            cronview.generate_times,
            "xyz",
            "0-7",
            name_substs=cronview.day_substs,
        )


if __name__ == "__main__":
    unittest.main()
