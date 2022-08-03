# Name: Patrick Kramer
# OSU Email: kramepat@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: 8/9/22
# Description: Implementation of Separate Chaining HashMap


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the given key/value pair. If the key is already present,
        update the value to the new value. If not, add to hash map.
        """
        # Get index by hashing key and modding by array size
        hash_value = self._hash_function(key)
        idx = hash_value % self._capacity

        # Check the bucket at found index for key
        if (self._buckets[idx].contains(key) != None):
            # Found node in SLL at idx
            self._buckets[idx].contains(key).value = value
        else:
            # Key not found. Create new Node
            self._buckets[idx].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the table.
        Iterate through all indexes and increment empty bucket count
        for each SLL with length 0.
        """
        count = 0
        for i in range(self._capacity):
            if (self._buckets[i].length() == 0):
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load facter.
        Load factor = total elements / number of buckets
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears all contents. Leaves capacity as is.
        Iterate through all indexes and set each bucket head to None and size
        to 0.
        """
        for i in range(self._capacity):
            self._buckets[i]._head = None
            self._buckets[i]._size = 0
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of hash table. All existing key / value pairs must
        be rehashed.
        """
        # Do nothing if new capacity is less than 1
        if (new_capacity < 1):
            return

        # Check that new_capacity is prime. If not, make it the next largest prime.
        if (self._is_prime(new_capacity) == False):
            new_capacity = self._next_prime(new_capacity)

        # Make new bucket array with new_capacity size
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        # Iterate through current hash_map and rehash into new bucket array
        for i in range(self._capacity):
            for j in self._buckets[i]:
                new_idx = self._hash_function(j.key) % new_capacity
                new_buckets[new_idx].insert(j.key, j.value)

        self._buckets = new_buckets
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        Return value associated with provided key.
        Return None if key not present.
        """
        # Get index by hashing key and modding by array size
        hash_value = self._hash_function(key)
        idx = hash_value % self._capacity

        # Check the bucket at found index for key
        if (self._buckets[idx].contains(key) != None):
            # Found node in SLL at idx
            return self._buckets[idx].contains(key).value
        else:
            # Key not found.
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the map. Else returns False.
        """
        # Get index by hashing key and modding by array size
        hash_value = self._hash_function(key)
        idx = hash_value % self._capacity

        # Check the bucket at found index for key
        if (self._buckets[idx].contains(key) != None):
            # Found node in SLL at idx
            return True
        else:
            # Key not found.
            return False

    def remove(self, key: str) -> None:
        """
        Removes key / value pair from Hash Map using given key.
        """
        # Get index by hashing key and modding by array size
        hash_value = self._hash_function(key)
        idx = hash_value % self._capacity

        # Try to remove key from LL at that idx
        if (self._buckets[idx].remove(key)):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Create and return a dynamic array of all elements in the HashMap.
        """
        # Create array
        keys_with_values = DynamicArray()

        # Iterate through all SLLs in the Buckets array and add key/value pairs to new array
        for i in range(self._capacity):
            for j in self._buckets[i]:
                keys_with_values.append((j.key, j.value))

        return keys_with_values


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receive an array, and return a tuple of a list of the modes as well
    as the frequency that those items appeared in the array.

    Create a hash map, and add each array element to the map with its value
    as the hashmap key and its frequency as the hashmap value.

    Keep track of a running max frequency.
    Once all items have been added, return an array of all map keys
    that have a value equal to the max frequency, as well as that max.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length())
    max_count = 0

    for i in range(da.length()):
        if (map.contains_key(da[i])):
            # Item already in map. Incrememnt value and update max_count if necessary.
            cur_freq = map.get(da[i])
            map.put(da[i], cur_freq + 1)
            if (cur_freq + 1 > max_count):
                max_count = cur_freq + 1
        else:
            # Item not in map. Add with value of 1
            map.put(da[i], 1)
            if (max_count == 0):
                max_count = 1

    # Iterate through map and add all elements with value equal to max to mode_list
    modes = DynamicArray()
    for i in range(map._capacity):
        for j in map._buckets[i]:
            if (j.value == max_count):
                modes.append(j.key)

    return (modes, max_count)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
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
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
