# Description: This file contains data for a hash table that utilizes open addressing and quadratic probing for resolving collisions.

# There are two classes: one called HashEntry that represents a key, value pair entry into the
# hash table and HashMap, which represents a DynamicArray that contains HashEntries. The HashMap
# class contains several methods to interact with the table and its entries, including:
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


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the contents of the hash map; it does not change the underlying hash table capacity.
        """
        # reset the size
        self.size = 0

        for i in range(self.capacity):
            self.buckets.set_at_index(i, None)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key or None if the key is not found.
        """
        # quadratic probing required
        # get index from hash
        index = self.get_hash_index(key) % self.capacity
        # set counter
        counter = 0

        if self.buckets[index] is None:
            return
        elif self.buckets[index].is_tombstone:
            return
        elif self.buckets[index].key == key:
            return self.buckets[index].value

        # rehash and get new index if key not yet found
        counter += 1
        new_index = (index + counter ** 2) % self.capacity

        # returns the value if key is found with first rehashing of the new index
        if self.buckets[new_index] is None:
            return
        elif self.buckets[new_index].is_tombstone:
            return
        elif self.buckets[new_index].key == key:
            return self.buckets[new_index].value

        # keep probing until the correct key is reached or if counter reaches capacity
        while self.buckets[new_index].key != key and counter <= self.capacity:
            counter += 1
            new_index = (index + counter ** 2) % self.capacity
            if self.buckets[new_index] is None:
                return
            elif self.buckets[new_index].is_tombstone:
                return

        # returns None if tombstone is flagged True or appropriate value if the key is found
        if self.buckets[new_index].is_tombstone:
            return
        else:
            return self.buckets[new_index].value

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a key / value pair must be added.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required

        # get load factor
        load_factor = self.table_load()

        # resize if load factor is >= 0.5
        if load_factor >= 0.5:
            self.resize_table(self.capacity * 2)

        # set counter
        counter = 0

        # get index from hash
        index = self.get_hash_index(key) % self.capacity

        # insert value at index if the spot there is empty
        if self.buckets[index] is None:
            self.buckets[index] = HashEntry(key, value)
            self.size += 1
        elif self.buckets[index].key == key:
            self.buckets[index] = HashEntry(key, value)
        elif self.buckets[index].is_tombstone:
            self.buckets[index] = HashEntry(key, value)
            self.size += 1
        else:
            # keep rehashing index and probing until a free spot is found, then insert key/value pair
            counter += 1
            new_index = (index + counter ** 2) % self.capacity
            while self.buckets[new_index] is not None and counter <= self.capacity:
                # replace value if key is already in table
                if self.buckets[new_index].key == key:
                    self.buckets[new_index] = HashEntry(key, value)
                    break
                # replace value at tombstone locations
                elif self.buckets[new_index].is_tombstone:
                    self.buckets[index] = HashEntry(key, value)
                    self.size += 1
                    break
                counter += 1
                new_index = (index + counter ** 2) % self.capacity
            # add value at locations where nothing is there yet
            if self.buckets[new_index] is None:
                self.buckets[new_index] = HashEntry(key, value)
                self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not
        in the hash map, the method does nothing.
        """
        # quadratic probing required

        # set counter
        counter = 0

        # get index from hash
        index = self.get_hash_index(key) % self.capacity

        # insert value at index if the spot there is empty
        if self.buckets[index] is None:
            return
        elif self.buckets[index].key == key:
            if self.buckets[index].is_tombstone is False:
                self.buckets[index].is_tombstone = True
                self.size -= 1
        else:
            # otherwise, keep rehashing index and probing until key is found
            counter += 1
            new_index = (index + counter ** 2) % self.capacity
            while self.buckets[new_index] is not None and counter <= self.capacity:
                # update tombstone flag for a HashEntry if the appropriate key is found and
                # the tombstone flag hasn't already been updated
                if self.buckets[new_index].key == key:
                    if self.buckets[new_index].is_tombstone is False:
                        self.buckets[new_index].is_tombstone = True
                        self.size -= 1
                counter += 1
                new_index = (index + counter ** 2) % self.capacity
            # do nothing if key is not found
            if self.buckets[new_index] is None:
                return

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        """
        # quadratic probing required

        # get index from hash
        index = self.get_hash_index(key)
        # set counter
        counter = 0

        if self.buckets[index] is None:
            return False
        elif self.buckets[index].key == key:
            return True

        # rehash and get new index if key not yet found
        counter += 1
        new_index = (index + counter ** 2) % self.capacity

        # check if key is found with first rehashing of index
        if self.buckets[new_index] is None:
            return False
        elif self.buckets[new_index].key == key:
            return True

        # keep rehashing and probing until key is found
        while self.buckets[new_index].key != key and counter <= self.capacity:
            counter += 1
            new_index = (index + counter ** 2) % self.capacity
            if self.buckets[new_index] is None:
                return False

        if self.buckets[new_index].key == key:
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        # god bless Hannah Boehm for this idea
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs will transfer to the new
        hash table, and all hash table links will be rehashed. Does nothing if the new capacity is less than 1.
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1 or new_capacity < self.size:
            return

        # store current hash table
        curr_table = self.buckets

        # reset buckets and other attributes
        self.buckets = DynamicArray()
        self.size = 0
        self.capacity = new_capacity
        for i in range(new_capacity):
            self.buckets.append(None)

        # rehash and refill the buckets
        for i in range(curr_table.length()):
            if curr_table[i] is not None and curr_table[i].is_tombstone is False:
                self.put(curr_table[i].key, curr_table[i].value)


    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all of the keys stored in the hash map.
        """
        # create array to cache keys
        keys_array = DynamicArray()

        # go through each bucket and its LinkedLists to add the keys to the array
        for index in range(self.capacity):
            if self.buckets[index] is not None and self.buckets[index].is_tombstone is False:
                keys_array.append(self.buckets[index].key)

        return keys_array

    def get_hash_index(self, key: str) -> int:
        """
        Args:
            key: a string that represents a key from a possible position within the HashMap

        Returns: a number that represents an index in the HashMap
        """
        # hash the key with the HashMap's function
        hash = self.hash_function(key)
        # get the index for the given key
        index = hash % self.capacity

        return index


if __name__ == "__main__":

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # # this test assumes that put() has already been correctly implemented
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)

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

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
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

    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    #
    # m.resize_table(1)
    # print(m.get_keys())
    #
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
