# python3
import sys

class ListNode:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def prepend(self, value):
        self.head = ListNode(data=value, next=self.head)
        self.size += 1

    def find(self, value):
        current = self.head
        while current and current.data != value:
            current = current.next
        return current

    def remove(self, value):
        current = self.head
        if current and current.data == value:
            self.head = current.next
            current = None
            self.size -= 1
            return
        previous = None
        while current and current.data != value:
            previous = current
            current = current.next

        if current is None:
            return

        previous.next = current.next
        current = None
        self.size -= 1

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()


class Query:

    def __init__(self, query):
        self._valid_cmd = ['add', 'find', 'del', 'check']
        if len(query) == 2:
            self.type = query[0]
            if self.type in self._valid_cmd and 0 < len(query[1]) <= 15:
                if self.type == 'check':
                    self.ind = int(query[1])
                else:
                    if 0 < len(query[1]) <= 15:
                        self.s = query[1]
            else:
                self.type = None
                self.s = None
        else:
            self.type = None
            self.s = None


class QueryProcessor:
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.bucket_count = bucket_count
        self.elems = [None] * self.bucket_count

    def _hash_func(self, s):
        ans = 0
        for c in reversed(s):
            if 'a' <= c <= 'z' or 'A' <= c <= 'Z':
                a = ans * self._multiplier + ord(c)
            else:
                ans = None
                return ans
            ans = ((a % self._prime) + self._prime) % self._prime
        return ans % self.bucket_count

    def search_table(self, q_string):
        search_hash = self._hash_func(q_string)
        if search_hash:
            search_list = self.elems[search_hash]
            if not search_list:
                return search_list
            else:
                found = search_list.find(q_string)
            return found

    def write_search_result(self, q_string):
        search_hash = self._hash_func(q_string)
        if search_hash is not None:
            search_list = self.elems[search_hash]
            if not search_list:
                string_found = None
            else:
                string_found = search_list.find(q_string)

            print('yes' if string_found else 'no')

    def delete_string(self, q_string):
        hash_value = self._hash_func(q_string)
        if hash_value is not None:
            del_list = self.elems[hash_value]
            if del_list:
                del_list.remove(q_string)
                if del_list.size == 0 and self.elems[hash_value] is not None:
                    self.elems[hash_value] = None

    def write_chain(self, hash_val):
        chain_list = self.elems[hash_val]
        if chain_list is not None:
            chain_list.print_list()
        else:
            print()

    def add_to_hash_table(self, q_string):
        hash_value = self._hash_func(q_string)
        if self.elems[hash_value] is None:
            new_list = LinkedList()
            new_list.prepend(q_string)
            self.elems[hash_value] = new_list
            return
        lst_exists = self.elems[hash_value]
        if lst_exists.find(q_string) is None:
            lst_exists.prepend(q_string)
            self.elems[hash_value] = lst_exists

    def read_query(self, test_cmd=None):
        if test_cmd is None:
            return Query(input().split())
        else:
            return Query(test_cmd.split())

    def process_query(self, query):
        if query.type is not None:
            if query.type == "check":
                if 0 <= query.ind <= self.bucket_count:
                    self.write_chain(query.ind)
            else:
                try:
                    ind = self.elems.index(query.s)
                except ValueError:
                    ind = -1
                if query.s is not None:
                    if query.type == 'find':
                        self.write_search_result(query.s)
                    elif query.type == 'add':
                        self.add_to_hash_table(query.s)
                    elif query.type == 'del':
                        self.delete_string(query.s)

    def process_queries(self, test_file):
        if not test_file:
            n = int(input())
            for i in range(n):
                self.process_query(self.read_query())
        else:
            n = int(test_file.readline().rstrip())
            for line in test_file:
                self.process_query(self.read_query(line))

    
def main():
    script = len(sys.argv)
    filename = sys.argv[1:]
    if len(sys.argv) == 1:
        bucket_count = int(input())
        proc = QueryProcessor(bucket_count)
        proc.process_queries(filename)
    else:
        test_file = filename[0]
        with open(test_file, 'r') as reader:
            bucket_count = int(reader.readline().rstrip())
            proc = QueryProcessor(bucket_count)
            proc.process_queries(reader)


if __name__ == '__main__':
    # bucket_count = int(input())
    # proc = QueryProcessor(bucket_count)
    # proc.process_queries()
    main()
