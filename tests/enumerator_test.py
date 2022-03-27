import pytest
from pyby import Enumerator, Enumerable, EnumerableDict


@pytest.fixture
def enumerated_list():
    return Enumerator([1, 2, 3])


@pytest.fixture
def enumerated_dict():
    return Enumerator({"a": 1, "b": 2, "c": 3})


def test_an_enumerator_responds_to_next():
    assert Enumerator([]).respond_to("next")


def test_repr(enumerated_list):
    assert repr(enumerated_list) == "Enumerator([1, 2, 3])"


def test_an_enumerated_list_can_be_iterated(enumerated_list):
    assert enumerated_list.next() == 1
    assert enumerated_list.next() == 2
    assert enumerated_list.next() == 3


def test_an_enumerated_list_can_be_rewound(enumerated_list):
    assert enumerated_list.next() == 1
    assert enumerated_list.next() == 2
    assert enumerated_list.rewind() == enumerated_list
    assert enumerated_list.next() == 1


def test_an_enumerated_dict_can_be_iterated(enumerated_dict):
    assert enumerated_dict.next() == "a"
    assert enumerated_dict.next() == "b"
    assert enumerated_dict.next() == "c"


def test_an_enumerated_dict_can_be_rewound(enumerated_dict):
    assert enumerated_dict.next() == "a"
    assert enumerated_dict.next() == "b"
    assert enumerated_dict.rewind() == enumerated_dict
    assert enumerated_dict.next() == "a"


def test_an_enumerator_is_an_enumerable(enumerated_list):
    assert isinstance(enumerated_list, Enumerable)


def test_an_enumerator_is_enumerable(enumerated_list, seen):
    enumerated_list.each(seen)
    assert seen == [1, 2, 3]


def test_enumerating_an_enumerator_is_not_affected_by_invoking_next(enumerated_list, seen):
    assert enumerated_list.next() == 1
    enumerated_list.each(seen)
    assert seen == [1, 2, 3]
    assert enumerated_list.next() == 2


def test_an_enumerator_is_iterable(enumerated_list, enumerated_dict):
    assert list(map(_identity, enumerated_list)) == [1, 2, 3]
    assert list(map(_identity, enumerated_dict)) == ["a", "b", "c"]

    enum = Enumerator(EnumerableDict({"a": 1, "b": 2, "c": 3}))
    assert list(map(_identity, enum)) == [("a", 1), ("b", 2), ("c", 3)]


def test_each_without_a_function_returns_a_new_enumerator(enumerated_list):
    new_enum = enumerated_list.each()
    assert isinstance(new_enum, Enumerator)
    assert new_enum != enumerated_list


def test_each_can_be_chained(enumerated_list):
    result = enumerated_list.each().each().each().map(lambda value: value * 2)
    assert result == [2, 4, 6]


def test_the_return_type_of_an_enumerable_iterable_is_used():
    enum = Enumerator(EnumerableDict({"a": 1, "b": None, "c": 3, None: 4}))
    result = enum.compact()
    assert result == {"a": 1, "c": 3, None: 4}


def test_the_return_type_defaults_to_a_list_for_normal_iterables():
    enum = Enumerator({"a": 1, "b": None, "c": 3, None: 4})
    result = enum.compact()
    assert result == ["a", "b", "c"]


def _identity(value):
    return value
