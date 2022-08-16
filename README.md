# HashMap

## Chaining
This implementation utilizes LinkedLists. 
There is one class, HashMap, which represents a DynamicArray that contains LinkedLists at each index. 
The HashMap class contains several methods to interact with the table and the LinkedLists, including:

### (1) empty_buckets: 
returns the number of empty buckets in the hash table
### (2) table_load: 
returns the current hash table load factor
### (3) clear: 
clears the contents of the hash map without changing the underlying capacity
### (4) put: 
updates the key/value pairs in the hash map
### (5) contains_key: 
confirms if a given key is in the hash map
### (6) get: 
returns the value associated with the given key
### (7) remove: 
removes the given key and its associated value from the hash map
### (8) resize_table: 
changes the capacity of the internal hash table
### (9) get_keys: 
returns a DynamicArray that contains all the keys stored in the hash map

## Open Addressing
This file contains the implementation of a HashMap that utilizes open addressing and quadratic probing for resolving collisions.

There are two classes: one called HashEntry that represents a key, value pair entry into the
hash table and HashMap, which represents a DynamicArray that contains HashEntries. The HashMap
class contains several methods to interact with the table and its entries, including:

### (1) empty_buckets: 
returns the number of empty buckets in the hash table
### (2) table_load: 
returns the current hash table load factor
### (3) clear: 
clears the contents of the hash map without changing the underlying capacity
### (4) put: 
updates the key/value pairs in the hash map
### (5) contains_key: 
confirms if a given key is in the hash map
### (6) get: 
returns the value associated with the given key
### (7) remove: 
removes the given key and its associated value from the hash map
### (8) resize_table: 
changes the capacity of the internal hash table
### (9) get_keys: 
returns a DynamicArray that contains all the keys stored in the hash map
