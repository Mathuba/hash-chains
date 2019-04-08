from hash_chains import QueryProcessor, Query, LinkedList
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
    assert add_cmd.s == 'MathubaMzwandil'


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
    illegal_cmd = query_processor.read_query(6)
    assert illegal_cmd.type is None
    assert illegal_cmd.s is None


def test_correct_word_length_accepted(query_processor):
    long_string = query_processor.read_query(5)
    # assert long_string.type is None
    assert long_string.s is None


def test_correct_hash_value_returned(query_processor):
    assert query_processor._hash_func('Mathuba') == 2


def test_correct_hash_value_two():
    proc_two = QueryProcessor(41)
    assert proc_two._hash_func('NLZLNyXoXoIC') == 15


def test_special_characters_return_no_hash_value(query_processor):
    assert query_processor._hash_func('Mathu(ba') is None


def test_add_creates_new_list_in_empty_slot(query_processor):
    add_cmd = query_processor.read_query(1)
    query_processor.process_query(add_cmd)
    add_list = query_processor.elems[2]
    add_node = add_list.head
    assert isinstance(add_list, LinkedList)
    assert add_node.data == 'MathubaMzwandil'
    assert add_node.next is None


def test_add_new_size_is_one(query_processor):
    add_cmd = query_processor.read_query(1)
    query_processor.process_query(add_cmd)
    add_list = query_processor.elems[2]
    add_node = add_list.head
    assert add_list.size == 1


def test_add_not_created_for_invalid_length(query_processor):
    add_cmd = query_processor.read_query(5)
    query_processor.process_query(add_cmd)
    add_list = query_processor.elems[3]
    assert add_list is None


def test_list_prepended_in_existing_slot(query_processor):
    add_cmd = query_processor.read_query(1)
    ant_cmd = query_processor.read_query(7)
    query_processor.process_query(add_cmd)
    query_processor.process_query(ant_cmd)
    add_list = query_processor.elems[2]
    add_node = add_list.head
    assert add_list.size == 2
    assert add_node.next.data == 'MathubaMzwandil'
    assert add_node.data == 'JGxqTHXXed'


def test_add_ignores_empty_string(query_processor):
    add_cmd = query_processor.read_query(6)
    query_processor.process_query(add_cmd)
    assert query_processor.elems == [None, None, None, None, None]


def test_add_to_slot_zero(query_processor):
    add_cmd = query_processor.read_query(8)
    query_processor.process_query(add_cmd)
    add_list = query_processor.elems[0]
    add_node = add_list.head
    assert isinstance(add_list, LinkedList)
    assert add_node.data == 'FErhDFUKGkOAWPE'
    assert add_node.next is None
