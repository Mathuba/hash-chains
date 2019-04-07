# python3


class ListNode:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def prepend(self, value):
        self.head = ListNode(data=value, next=self.head)

    def find(self, value):
        current = self.head
        while current and current.data != value:
            current = current.next
        return current

    def remove(self, value):
        current = self.head
        previous = None
        while current and current.data != value:
            previous = current
            current = current.next
        if previous is None:
            self.head = current.next
        elif current:
            previous.next = current.next
            current.next = None

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=' ')
        print()


class Query:

    def __init__(self, query):
        self._valid_cmd = ['add', 'find', 'del', 'check']
        self.type = query[0]
        if self.type in self._valid_cmd:
            if self.type == 'check':
                self.ind = int(query[1])
            else:
                self.s = query[1]
        else:
            self.type = None
            self.s = None


class QueryProcessor:
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.bucket_count = bucket_count
        # store all strings in one list
        self.elems = [None] * self.bucket_count

    def _hash_func(self, s):
        ans = 0
        for c in reversed(s):
            ans = (ans * self._multiplier + ord(c)) % self._prime
        return ans % self.bucket_count

    def write_search_result(self, was_found):
        print('yes' if was_found else 'no')

    def write_chain(self, chain):
        print(' '.join(chain))

    def read_query(self, test_num=None):
        if test_num is None:
            return Query(input().split())

        if test_num == 1:
            return Query('add Mathuba'.split())
        elif test_num == 2:
            return Query('find Mathuba'.split())
        elif test_num == 3:
            return Query('del Mathuba'.split())
        elif test_num == 4:
            return Query('check 4'.split())
        else:
            return Query('illegal commans'.split())

    def process_query(self, query):
        if query.type == "check":
            # use reverse order, because we append strings to the end
            self.write_chain(cur for cur in reversed(self.elems)
                        if self._hash_func(cur) == query.ind)
        else:
            try:
                ind = self.elems.index(query.s)
            except ValueError:
                ind = -1
            if query.type == 'find':
                self.write_search_result(ind != -1)
            elif query.type == 'add':
                if ind == -1:
                    self.elems.append(query.s)
            else:
                if ind != -1:
                    self.elems.pop(ind)

    def process_queries(self):
        n = int(input())
        for i in range(n):
            self.read_query()  # should be deleted eventually
            #self.process_query(self.read_query())


if __name__ == '__main__':
    bucket_count = int(input())
    proc = QueryProcessor(bucket_count)
    proc.process_queries()
