import unittest

from BaseStructures import (
    DataMapper,
    EnumDataMapper,
    NotACallableError,
    OutputType,
    OutputTypeError,
)
from Enum import Enum


class TestDataMapper(unittest.TestCase):
    def setUp(self):
        self.data = DataMapper({0: "0"})
        self.data_multiple = DataMapper({0: ["0", "1"]})

    def test_equals(self):
        self.assertEqual(self.data, self.data)
        self.assertEqual(self.data_multiple, self.data_multiple)

    def test_contains(self):
        def _wrong_contains():
            "0" in self.data

        def _wrong_contains_multiple():
            "0" in self.data_multiple

        self.assertTrue(0 in self.data)
        self.assertTrue(0 in self.data_multiple)
        self.assertRaises(TypeError, _wrong_contains)
        self.assertRaises(TypeError, _wrong_contains_multiple)

    def test_getitem(self):
        def _wrong_getitem():
            return self.data["0"]

        def _wrong_getitem_multiple():
            return self.data_multiple["0"]

        self.assertEqual(self.data[0], "0")
        self.assertEqual(self.data_multiple[0], ["0", "1"])
        self.assertRaises(TypeError, _wrong_getitem)
        self.assertRaises(TypeError, _wrong_getitem_multiple)

    def test_setitem(self):
        def _wrong_setitem():
            self.data["0"] = "0"

        def _wrong_setitem_multiple():
            self.data_multiple["0"] = ["0", "1"]

        self.data[0] = "0"
        self.data_multiple[0] = ["0"]
        self.assertRaises(TypeError, _wrong_setitem)
        self.assertRaises(TypeError, _wrong_setitem_multiple)

    def test_output_type(self):
        self.assertEqual(self.data.output_type, OutputType.SINGLE)
        self.assertEqual(self.data_multiple.output_type, OutputType.MULTIPLE)

    def test_apply(self):
        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data.apply(lambda x: int(x)), DataMapper({0: 0}))
        self.assertEqual(self.data_multiple.apply(lambda x: len(x)), DataMapper({0: 2}))

    def test_applymap(self):
        def _wrong_applymap():
            return self.data.applymap(lambda x: int(x))

        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(OutputTypeError, _wrong_applymap)
        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data_multiple.applymap(lambda x: int(x)), DataMapper({0: [0, 1]}))

    def test_filter(self):
        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data.filter(lambda x: x != "0"), DataMapper({}))
        self.assertEqual(self.data_multiple.filter(lambda x: "3" in x), DataMapper({}))


class _TestDataMapper(DataMapper):
    BASE_CLASS = str


class TestInheritDataMapper(unittest.TestCase):
    def setUp(self):
        self.data = _TestDataMapper({"0": "0"})
        self.data_multiple = _TestDataMapper({"0": ["0", "1"]})

    def test_equals(self):
        self.assertEqual(self.data, self.data)
        self.assertEqual(self.data_multiple, self.data_multiple)

    def test_contains(self):
        def _wrong_contains():
            0 in self.data

        def _wrong_contains_multiple():
            0 in self.data_multiple

        self.assertTrue("0" in self.data)
        self.assertTrue("0" in self.data_multiple)
        self.assertRaises(TypeError, _wrong_contains)
        self.assertRaises(TypeError, _wrong_contains_multiple)

    def test_getitem(self):
        def _wrong_getitem():
            return self.data[0]

        def _wrong_getitem_multiple():
            return self.data_multiple[0]

        self.assertEqual(self.data["0"], "0")
        self.assertEqual(self.data_multiple["0"], ["0", "1"])
        self.assertRaises(TypeError, _wrong_getitem)
        self.assertRaises(TypeError, _wrong_getitem_multiple)

    def test_setitem(self):
        def _wrong_setitem():
            self.data[0] = "0"

        def _wrong_setitem_multiple():
            self.data_multiple[0] = ["0", "1"]

        self.data["0"] = "0"
        self.data_multiple["0"] = "0"
        self.assertRaises(TypeError, _wrong_setitem)

    def test_output_type(self):
        self.assertEqual(self.data.output_type, OutputType.SINGLE)
        self.assertEqual(self.data_multiple.output_type, OutputType.MULTIPLE)

    def test_apply(self):
        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data.apply(lambda x: int(x)), _TestDataMapper({"0": 0}))
        self.assertEqual(self.data_multiple.apply(lambda x: len(x)), _TestDataMapper({"0": 2}))

    def test_applymap(self):
        def _wrong_applymap():
            return self.data.applymap(lambda x: int(x))

        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(OutputTypeError, _wrong_applymap)
        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(
            self.data_multiple.applymap(lambda x: int(x)), _TestDataMapper({"0": [0, 1]})
        )

    def test_filter(self):
        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data.filter(lambda x: x != "0"), _TestDataMapper({}))
        self.assertEqual(self.data_multiple.filter(lambda x: "3" in x), _TestDataMapper({}))


class _TestEnum(Enum):
    A = 0
    B = 1


class TestEnumDataMapper(unittest.TestCase):
    def setUp(self):
        self.data = EnumDataMapper({_TestEnum.A: "0"})
        self.data_multiple = EnumDataMapper({_TestEnum.A: ["0", "1"]})

    def test_equals(self):
        self.assertEqual(self.data, self.data)
        self.assertEqual(self.data_multiple, self.data_multiple)

    def test_contains(self):
        def _wrong_contains():
            0 in self.data

        def _wrong_contains_multiple():
            0 in self.data_multiple

        self.assertTrue(_TestEnum.A in self.data)
        self.assertTrue(_TestEnum.A in self.data_multiple)
        self.assertRaises(TypeError, _wrong_contains)
        self.assertRaises(TypeError, _wrong_contains_multiple)

    def test_getitem(self):
        def _wrong_getitem():
            return self.data[0]

        def _wrong_getitem_multiple():
            return self.data_multiple[0]

        self.assertEqual(self.data[_TestEnum.A], "0")
        self.assertEqual(self.data_multiple[_TestEnum.A], ["0", "1"])
        self.assertRaises(TypeError, _wrong_getitem)
        self.assertRaises(TypeError, _wrong_getitem_multiple)

    def test_setitem(self):
        def _wrong_setitem():
            self.data[0] = "0"

        def _wrong_setitem_multiple():
            self.data_multiple[0] = "0"

        self.data[_TestEnum.A] = "0"
        self.data_multiple[_TestEnum.A] = ["0", "1"]
        self.assertRaises(TypeError, _wrong_setitem)
        self.assertRaises(TypeError, _wrong_setitem_multiple)

    def test_output_type(self):
        self.assertEqual(self.data.output_type, OutputType.SINGLE)
        self.assertEqual(self.data_multiple.output_type, OutputType.MULTIPLE)

    def test_fill_missing_members(self):
        self.assertEqual(
            self.data.fill_missing_members(None),
            EnumDataMapper({_TestEnum.A: "0"}),
        )

    def test_apply(self):
        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data.apply(lambda x: int(x)), EnumDataMapper({_TestEnum.A: 0}))
        self.assertEqual(
            self.data_multiple.apply(lambda x: len(x)), EnumDataMapper({_TestEnum.A: 2})
        )

    def test_applymap(self):
        def _wrong_applymap():
            return self.data.applymap(lambda x: int(x))

        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(OutputTypeError, _wrong_applymap)
        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(
            self.data_multiple.applymap(lambda x: int(x)), EnumDataMapper({_TestEnum.A: [0, 1]})
        )

    def test_filter(self):
        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data.filter(lambda x: x != "0"), EnumDataMapper({}))
        self.assertEqual(self.data_multiple.filter(lambda x: "3" in x), EnumDataMapper({}))


class _TestEnumDataMapper(EnumDataMapper):
    BASE_CLASS = _TestEnum


class TestInheritEnumDataMapper(unittest.TestCase):
    def setUp(self):
        self.data = _TestEnumDataMapper({_TestEnum.A: "0"})
        self.data_multiple = _TestEnumDataMapper({_TestEnum.A: ["0", "1"]})

    def test_equals(self):
        self.assertEqual(self.data, self.data)
        self.assertEqual(self.data_multiple, self.data_multiple)

    def test_contains(self):
        def _wrong_contains():
            0 in self.data

        def _wrong_contains_multiple():
            0 in self.data_multiple

        self.assertTrue(_TestEnum.A in self.data)
        self.assertTrue(_TestEnum.A in self.data_multiple)
        self.assertRaises(TypeError, _wrong_contains)
        self.assertRaises(TypeError, _wrong_contains_multiple)

    def test_getitem(self):
        def _wrong_getitem():
            return self.data[0]

        def _wrong_getitem_multiple():
            return self.data_multiple[0]

        self.assertEqual(self.data[_TestEnum.A], "0")
        self.assertEqual(self.data_multiple[_TestEnum.A], ["0", "1"])
        self.assertRaises(TypeError, _wrong_getitem)
        self.assertRaises(TypeError, _wrong_getitem_multiple)

    def test_setitem(self):
        def _wrong_setitem():
            self.data[0] = "0"

        def _wrong_setitem_multiple():
            self.data_multiple[0] = ["0", "1"]

        def _wrong_setitem_other_enum():
            class _TestEnum2(Enum):
                A = 0

            self.data[_TestEnum2.A] = "0"

        def _wrong_setitem_other_enum_multiple():
            class _TestEnum2(Enum):
                A = 0

            self.data_multiple[_TestEnum2.A] = "0"

        self.data[_TestEnum.A] = "0"
        self.data_multiple[_TestEnum.A] = ["0", "1"]
        self.assertRaises(TypeError, _wrong_setitem)
        self.assertRaises(TypeError, _wrong_setitem_multiple)
        self.assertRaises(TypeError, _wrong_setitem_other_enum)
        self.assertRaises(TypeError, _wrong_setitem_other_enum_multiple)

    def test_output_type(self):
        self.assertEqual(self.data.output_type, OutputType.SINGLE)
        self.assertEqual(self.data_multiple.output_type, OutputType.MULTIPLE)

    def test_fill_missing_members(self):
        self.assertEqual(
            self.data.fill_missing_members(None),
            EnumDataMapper({_TestEnum.A: "0", _TestEnum.B: None}),
        )

    def test_apply(self):
        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data.apply(lambda x: int(x)), _TestEnumDataMapper({_TestEnum.A: 0}))
        self.assertEqual(
            self.data_multiple.apply(lambda x: len(x)), _TestEnumDataMapper({_TestEnum.A: 2})
        )

    def test_applymap(self):
        def _wrong_applymap():
            return self.data.applymap(lambda x: int(x))

        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(OutputTypeError, _wrong_applymap)
        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(
            self.data_multiple.applymap(lambda x: int(x)),
            _TestEnumDataMapper({_TestEnum.A: [0, 1]}),
        )

    def test_filter(self):
        def _wrong_callable():
            return self.data.apply("")

        self.assertRaises(NotACallableError, _wrong_callable)
        self.assertEqual(self.data.filter(lambda x: x != "0"), _TestEnumDataMapper({}))
        self.assertEqual(self.data_multiple.filter(lambda x: "3" in x), _TestEnumDataMapper({}))


if __name__ == "__main__":
    unittest.main()
