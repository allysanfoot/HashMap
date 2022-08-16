# Description: This file contains data for a hash table that utilizes open addressing and
# quadratic probing for resolving collisions.
# There is one class: HashMap, which represents a DynamicArray that contains LinkedLists at each index.
# The HashMap class contains several methods to interact with the table and the LinkedLists, including:
# (1) empty_buckets: returns the number of empty buckets in the hash table
# (2) table_load: returns the current hash table load factor
# (3) clear: clears the contents of the hash map without changing the underlying capacity
# (4) put: updates the key/value pairs in the hash map
# (5) contains_key: confirms if a given key is in the hash map
# (6) get: returns the value associated with the given key
# (7) remove: removes the given key and its associated value from the hash map
# (8) resize_table: changes the capacity of the internal hash table
# (9) get_keys: returns a DynamicArray that contains all the keys stored in the hash map

from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the contents of the hash map; it does not change the underlying hash table capacity.
        """
        # reset the buckets with an empty DynamicArray
        self.buckets = DynamicArray()

        # go through the new array and append a LinkedList at each index
        for _ in range(self.capacity):
            self.buckets.append(LinkedList())

        # reset the size
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key or None if the key is not found.
        """
        # get the LinkedList using the given key
        linked_list = self.get_linked_list(key)

        # return result
        return linked_list.contains(key)

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. Replaces the given key's old value with the new given value
        if the key already exists in the hash map. Otherwise, it will add the new key/value pair.
        """
        # get the LinkedList using the given key
        linked_list = self.get_linked_list(key)

        # replace value at given key if key is already in the map
        if linked_list.contains(key):
            linked_list.remove(key)
            linked_list.insert(key, value)
        # otherwise just add it to the map
        else:
            linked_list.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map; does nothing if key is not found.
        """
        # get the LinkedList using the given key
        linked_list = self.get_linked_list(key)

        if linked_list.contains(key):
            linked_list.remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map; otherwise returns False.
        """
        # get the LinkedList using the given key
        linked_list = self.get_linked_list(key)

        return True if linked_list.contains(key) is not None else False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        # create a counter for the number of empty buckets
        empty_bucket_count = 0

        # loop through the table and count the number of empty buckets encountered
        for index in range(self.capacity):
            if self.buckets[index].length() == 0:
                empty_bucket_count +=1

        return empty_bucket_count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        # easy-peasy
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs will transfer to the new
        hash table, and all hash table links will be rehashed. Does nothing if the new capacity is less than 1.
        """
        if new_capacity < 1:
            return

        # store current hash table
        curr_table = self.buckets

        # reset table with new capacity and other attributes
        self.buckets = DynamicArray()
        self.size = 0
        self.capacity = new_capacity
        for _ in range(new_capacity):
            self.buckets.append(LinkedList())

        # rehash each link into the new buckets
        for index in range(curr_table.length()):
            for node in curr_table[index]:
                self.put(node.key, node.value)

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all of the keys stored in the hash map.
        """
        # create array to cache keys
        keys_array = DynamicArray()

        for index in range(self.capacity):
            # iterate through each node in linked list at bucket
            for node in self.buckets[index]:
                keys_array.append(node.key)

        return keys_array

    def get_linked_list(self, key: str) -> object:
        """
        Args:
            key: a string that represents a key from a possible node within a LinkedList at an index in the HashMap

        Returns: the LinkedList associated with a key or None if no key exists
        """
        # hash the key with the HashMap's function
        hash = self.hash_function(key)
        # get the index for the given key
        index = hash % self.capacity
        # get the LinkedList at the calculated index
        linked_list = self.buckets[index]

        return linked_list


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)
    #
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
