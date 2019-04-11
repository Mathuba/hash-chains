from hash_chains import QueryProcessor, Query, LinkedList
from copy import deepcopy
import pytest


@pytest.fixture
def empty_query_processor():
    return QueryProcessor()


@pytest.fixture
def query_processor(scope="module"):
    return QueryProcessor(5)


def test_initial_bucket_count(query_processor):
    assert query_processor.bucket_count == 5


def test_elems_size(query_processor):
    assert query_processor.elems == [None, None, None, None, None]


def test_add_is_accepted(query_processor):
    add_cmd = query_processor.read_query('add MathubaMzwandil')
    assert add_cmd.type == 'add'
    assert add_cmd.s == 'MathubaMzwandil'


def test_find_is_accepted(query_processor):
    find_cmd = query_processor.read_query('find Mathuba')
    assert find_cmd.type == 'find'
    assert find_cmd.s == 'Mathuba'


def test_del_is_accepted(query_processor):
    del_cmd = query_processor.read_query('del Mathuba')
    assert del_cmd.type == 'del'
    assert del_cmd.s == 'Mathuba'


def test_check_is_accepted(query_processor):
    check_cmd = query_processor.read_query('check 4')
    assert check_cmd.type == 'check'
    assert check_cmd.ind == 4


def test_no_other_command_accepted(query_processor):
    illegal_cmd = query_processor.read_query('add        ')
    assert illegal_cmd.type is None
    assert illegal_cmd.s is None


def test_correct_word_length_accepted(query_processor):
    long_string = query_processor.read_query('add MathubaMzwandile')
    assert long_string.s is None


def test_correct_hash_value_returned(query_processor):
    assert query_processor._hash_func('Mathuba') == 2


def test_correct_hash_value_two():
    proc_two = QueryProcessor(41)
    assert proc_two._hash_func('NLZLNyXoXoIC') == 15


def test_special_characters_return_no_hash_value(query_processor):
    assert query_processor._hash_func('Mathu(ba') is None


def test_add_creates_new_list_in_empty_slot(query_processor):
    add_cmd = query_processor.read_query('add MathubaMzwandil')
    query_processor.process_query(add_cmd)
    add_list = query_processor.elems[2]
    add_node = add_list.head
    assert isinstance(add_list, LinkedList)
    assert add_node.data == 'MathubaMzwandil'
    assert add_node.next is None


def test_add_new_size_is_one(query_processor):
    add_cmd = query_processor.read_query('add MathubaMzwandil')
    query_processor.process_query(add_cmd)
    add_list = query_processor.elems[2]
    add_node = add_list.head
    assert add_list.size == 1


def test_add_not_created_for_invalid_length(query_processor):
    add_cmd = query_processor.read_query('add MathubaMzwandile')
    query_processor.process_query(add_cmd)
    add_list = query_processor.elems[3]
    assert add_list is None


def test_add_duplicate_value_not_added(query_processor, capsys):
    add_cmd = query_processor.read_query('add test')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add test')
    query_processor.process_query(add_cmd)
    del_cmd = query_processor.read_query('del test')
    query_processor.process_query(del_cmd)
    find_cmd = query_processor.read_query('find test')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    add_list = query_processor.elems[2]
    assert add_list is None
    assert captured.out == "no\n"


def test_list_prepended_in_existing_slot(query_processor):
    add_cmd = query_processor.read_query('add MathubaMzwandil')
    ant_cmd = query_processor.read_query('add JGxqTHXXed')
    query_processor.process_query(add_cmd)
    query_processor.process_query(ant_cmd)
    add_list = query_processor.elems[2]
    add_node = add_list.head
    assert add_list.size == 2
    assert add_node.next.data == 'MathubaMzwandil'
    assert add_node.data == 'JGxqTHXXed'


def test_add_ignores_empty_string(query_processor):
    add_cmd = query_processor.read_query('add')
    query_processor.process_query(add_cmd)
    assert query_processor.elems == [None, None, None, None, None]


def test_add_to_slot_zero(query_processor):
    add_cmd = query_processor.read_query('add FErhDFUKGkOAWPE')
    query_processor.process_query(add_cmd)
    add_list = query_processor.elems[0]
    add_node = add_list.head
    assert isinstance(add_list, LinkedList)
    assert add_node.data == 'FErhDFUKGkOAWPE'
    assert add_node.next is None


def test_find_first_string_added_to_index_four(query_processor, capsys):
    add_cmd_one = query_processor.read_query('add lcLYbKEYIBUWQw')
    query_processor.process_query(add_cmd_one)
    add_cmd_one = query_processor.read_query('add Bcmp')
    query_processor.process_query(add_cmd_one)
    find_cmd = query_processor.read_query('find lcLYbKEYIBUWQw')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    assert captured.out == "yes\n"


def test_find_last_string_added_to_index_zero(query_processor, capsys):
    add_cmd_one = query_processor.read_query('add cAAssOrJmS')
    query_processor.process_query(add_cmd_one)
    add_cmd_one = query_processor.read_query('add sodomLhz')
    query_processor.process_query(add_cmd_one)
    find_cmd = query_processor.read_query('find sodomLhz')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    assert captured.out == "yes\n"


def test_find_from_empty_index_one(query_processor, capsys):
    add_cmd_one = query_processor.read_query('add mDYecCudUYIFeRg')
    query_processor.process_query(add_cmd_one)
    find_cmd = query_processor.read_query('find XpuCIJKZwu')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    assert captured.out == "no\n"


def test_find_last_string_added_to_index_four(query_processor, capsys):
    add_cmd_one = query_processor.read_query('add lcLYbKEYIBUWQw')
    query_processor.process_query(add_cmd_one)
    add_cmd_one = query_processor.read_query('add Bcmp')
    query_processor.process_query(add_cmd_one)
    find_cmd = query_processor.read_query('find Bcmp')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    assert captured.out == "yes\n"


def test_find_first_string_added_to_index_zero(query_processor, capsys):
    add_cmd_one = query_processor.read_query('add cAAssOrJmS')
    query_processor.process_query(add_cmd_one)
    add_cmd_one = query_processor.read_query('add sodomLhz')
    query_processor.process_query(add_cmd_one)
    find_cmd = query_processor.read_query('find  cAAssOrJmS')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    assert captured.out == "yes\n"


def test_find_command_with_no_string(query_processor, capsys):
    add_cmd_one = query_processor.read_query('add cAAssOrJmS')
    query_processor.process_query(add_cmd_one)
    add_cmd_one = query_processor.read_query('add sodomLhz')
    query_processor.process_query(add_cmd_one)
    find_cmd = query_processor.read_query('find           ')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_find_command_with_invalid_string_length(query_processor, capsys):
    add_cmd_one = query_processor.read_query('add cAAssOrJmS')
    query_processor.process_query(add_cmd_one)
    add_cmd_one = query_processor.read_query('add sodomLhz')
    query_processor.process_query(add_cmd_one)
    find_cmd = query_processor.read_query('find MathubaMzwandile')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_find_command_with_string_with_special_chars(query_processor, capsys):
    add_cmd_one = query_processor.read_query('add cAAssOrJmS')
    query_processor.process_query(add_cmd_one)
    add_cmd_one = query_processor.read_query('add sodomLhz')
    query_processor.process_query(add_cmd_one)
    find_cmd = query_processor.read_query('find  cAAssOr)JmS')
    query_processor.process_query(find_cmd)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_del_for_string_added_to_slot_zero(query_processor):
    add_cmd = query_processor.read_query('add VyJAnSDWRDx')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add FErhDFUKGkOAWPE')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add XTua')
    query_processor.process_query(add_cmd)
    del_cmd = query_processor.read_query('del VyJAnSDWRDx')
    query_processor.process_query(del_cmd)
    add_list = query_processor.elems[0]
    add_node = add_list.head
    assert add_node.data == 'XTua'
    assert add_node.next.data == 'FErhDFUKGkOAWPE'


def test_del_for_last_string_added_to_slot_four(query_processor):
    add_cmd = query_processor.read_query('add Mr')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add Y')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add KJdWfQygOx')
    query_processor.process_query(add_cmd)
    del_cmd = query_processor.read_query('del KJdWfQygOx')
    query_processor.process_query(del_cmd)
    add_list = query_processor.elems[4]
    add_node = add_list.head
    assert add_list.size == 2
    assert add_node.data == 'Y'
    assert add_node.next.data == 'Mr'


def test_del_for_string_added_to_slot_one(query_processor):
    add_cmd = query_processor.read_query('add dFDyzlw')
    query_processor.process_query(add_cmd)
    del_cmd = query_processor.read_query('del dFDyzlw')
    query_processor.process_query(del_cmd)
    add_list = query_processor.elems[1]
    assert add_list is None


def test_del_twice_for_same_string_added_to_slot_four(query_processor):
    add_cmd = query_processor.read_query('add Mr')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add Y')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add KJdWfQygOx')
    query_processor.process_query(add_cmd)
    del_cmd = query_processor.read_query('del KJdWfQygOx')
    query_processor.process_query(del_cmd)
    del_cmd = query_processor.read_query('del KJdWfQygOx')
    query_processor.process_query(del_cmd)
    add_list = query_processor.elems[4]
    add_node = add_list.head
    assert add_list.size == 2
    assert add_node.data == 'Y'
    assert add_node.next.data == 'Mr'


def test_del_command_only(query_processor):
    del_cmd = query_processor.read_query('del         ')
    query_processor.process_query(del_cmd)
    assert query_processor.elems == [None, None, None, None, None]


def test_del_for_invalid_string(query_processor):
    add_cmd_one = query_processor.read_query('add cAAssOrJmS')
    query_processor.process_query(add_cmd_one)
    del_cmd = query_processor.read_query('del cAAssOr)JmS')
    query_processor.process_query(del_cmd)
    add_list = query_processor.elems[0]
    add_node = add_list.head
    assert add_list.size == 1
    assert add_node.data == 'cAAssOrJmS'
    assert add_node.next is None


def test_check_for_seven_values_in_slot_zero(query_processor, capsys):
    add_cmd = query_processor.read_query('add CbTIAcpmSzJ')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add FrXkdAemjzcN')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add ZxzChw')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add RupdekycY')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add VyJAnSDWRDx')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add DkZWMOtgjZYTJt')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add GN')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add ZxzChw')
    query_processor.process_query(add_cmd)
    check_cmd = query_processor.read_query('check 0')
    query_processor.process_query(check_cmd)
    check_list = query_processor.elems[0]
    assert check_list.size == 7
    captured = capsys.readouterr()
    assert captured.out == "GN DkZWMOtgjZYTJt VyJAnSDWRDx RupdekycY ZxzChw FrXkdAemjzcN CbTIAcpmSzJ \n"


def test_check_for_no_values_in_slot_one(query_processor, capsys):
    check_cmd = query_processor.read_query('check 1')
    query_processor.process_query(check_cmd)
    captured = capsys.readouterr()
    assert captured.out == "\n"


def test_check_for_six_values_in_slot_two(query_processor, capsys):
    add_cmd = query_processor.read_query('add PoMdzEldVw')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add mrnDJQAKylA')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add mDYecCudUYIFeRg')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add nlqxNQg')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add ynvdyvH')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add eOSKlmbbLjko')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add jRzZEKpSxjsS')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add HBtun')
    query_processor.process_query(add_cmd)
    check_cmd = query_processor.read_query('check 2')
    query_processor.process_query(check_cmd)
    check_list = query_processor.elems[2]
    assert check_list.size == 8
    captured = capsys.readouterr()
    assert captured.out == "HBtun jRzZEKpSxjsS eOSKlmbbLjko ynvdyvH nlqxNQg mDYecCudUYIFeRg mrnDJQAKylA PoMdzEldVw \n"


def test_check_for_three_values_in_slot_three(query_processor, capsys):
    add_cmd = query_processor.read_query('add psUGGlL')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add TWeYadvt')
    query_processor.process_query(add_cmd)
    add_cmd = query_processor.read_query('add rBNXcO')
    query_processor.process_query(add_cmd)
    check_cmd = query_processor.read_query('check 3')
    query_processor.process_query(check_cmd)
    check_list = query_processor.elems[3]
    assert check_list.size == 3
    captured = capsys.readouterr()
    assert captured.out == "rBNXcO TWeYadvt psUGGlL \n"


def test_check_for_one_value_in_slot_four(query_processor, capsys):
    add_cmd = query_processor.read_query('add TEJH')
    query_processor.process_query(add_cmd)
    check_cmd = query_processor.read_query('check 4')
    query_processor.process_query(check_cmd)
    check_list = query_processor.elems[4]
    assert check_list.size == 1
    captured = capsys.readouterr()
    assert captured.out == "TEJH \n"


def test_check_command_only(query_processor):
    check_cmd = query_processor.read_query('check         ')
    query_processor.process_query(check_cmd)
    assert query_processor.elems == [None, None, None, None, None]


def test_check_invalid_hash_table_index(query_processor):
    check_cmd = query_processor.read_query('check 10')
    query_processor.process_query(check_cmd)
    assert query_processor.elems == [None, None, None, None, None]





