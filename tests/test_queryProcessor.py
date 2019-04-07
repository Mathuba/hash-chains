from hash_chains import QueryProcessor, Query
import pytest


@pytest.fixture
def empty_query_processor():
    return QueryProcessor()


@pytest.fixture
def query_processor():
    return QueryProcessor(5)


def test_initial_bucket_count(query_processor):
    assert query_processor.bucket_count == 5


def test_elems_size(query_processor):
    assert query_processor.elems == [None, None, None, None, None]


def test_add_is_accepted(query_processor):
    add_cmd = query_processor.read_query(1)
    assert add_cmd.type == 'add'
    assert add_cmd.s == 'Mathuba'


def test_find_is_accepted(query_processor):
    find_cmd = query_processor.read_query(2)
    assert find_cmd.type == 'find'
    assert find_cmd.s == 'Mathuba'


def test_del_is_accepted(query_processor):
    del_cmd = query_processor.read_query(3)
    assert del_cmd.type == 'del'
    assert del_cmd.s == 'Mathuba'


def test_check_is_accepted(query_processor):
    check_cmd = query_processor.read_query(4)
    assert check_cmd.type == 'check'
    assert check_cmd.ind == 4


def test_no_other_command_accepted(query_processor):
    illegal_cmd = query_processor.read_query(5)
    assert illegal_cmd.type is None
    assert illegal_cmd.s is None
