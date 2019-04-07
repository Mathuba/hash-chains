from hash_chains import QueryProcessor
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
