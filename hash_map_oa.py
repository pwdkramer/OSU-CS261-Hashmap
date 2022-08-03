# Name: Patrick Kramer
# OSU Email: kramepat@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: 8/9/22
# Description: Implementation of Open Addressing HashMap


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Updates key/value pair in hash map. Updates value if key already
        exits, if not, add the key/value pair. Resize to double
        if load factor >= 0.5.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if (self.table_load() >= 0.5):
            self.resize_table(self._capacity * 2)

        # Get initial index
        init_idx = self._hash_function(key) % self._capacity

        # Quadratic probing until element is added
        updated = False
        j = 0
        while (updated == False):
            cur_idx = (init_idx + (j ** 2)) % self._capacity
            if (self._buckets[cur_idx] == None):
                # No item at index. Add new item.
                new_entry = HashEntry(key, value)
                self._buckets[cur_idx] = new_entry
                self._size += 1
                updated = True
            elif (self._buckets[cur_idx].is_tombstone == True):
                # Deleted item at index. Add new item
                new_entry = HashEntry(key, value)
                self._buckets[cur_idx] = new_entry
                self._size += 1
                updated = True
            elif (self._buckets[cur_idx].key == key):
                # Key already in array. Update value.
                self._buckets[cur_idx].value = value
                updated = True
            else:
                # Different item occupying index. Continue quadratic probing.
                j += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load facter.
        Load factor = total elements / number of buckets
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the table.
        Iterate through all indexes and increment empty bucket count
        for each None or is_tombstone = True.
        """
        count = 0
        for i in range(self._capacity):
            if (self._buckets[i] == None or self._buckets[i].is_tombstone == True):
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Update capacity of hash_table. All existing key/value pairs must
        be rehashed into new array. New_capacity must be larger than current size
        and if not a prime, update it to the next largest prime.
        """
        # Do nothing if new_capacity is less than num of elements
        if (new_capacity < self._size):
            return

        # Check that new_capacity is prime. If not, make it the next largest prime.
        if (self._is_prime(new_capacity) == False):
            new_capacity = self._next_prime(new_capacity)

        # Make new bucket array with new_capacity size
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        # remember to rehash non-deleted entries into new table
        for i in range(self._capacity):
            if (self._buckets[i] == None):
                # Keep moving
                continue
            elif (self._buckets[i].is_tombstone == True):
                # Keep moving
                continue
            else:
                # Add item to new array
                new_entry = HashEntry(self._buckets[i].key, self._buckets[i].value)
                init_idx = self._hash_function(self._buckets[i].key) % new_capacity
                j = 0
                added = False
                while (added == False):
                    cur_idx = (init_idx + (j ** 2)) % new_capacity
                    if (new_buckets[cur_idx] == None):
                        # No item at index. Add new item.
                        new_buckets[cur_idx] = new_entry
                        added = True
                    else:
                        # Different item occupying index. Continue quadratic probing.
                        j += 1

        self._buckets = new_buckets
        self._capacity = new_capacity

        # # Check the load factor and do it all again if >= 0.5
        # if (self.table_load() >= 0.5):
        #     # Here we go again...
        #     new_capacity = self._capacity * 2
        #     if (self._is_prime(new_capacity) == False):
        #         new_capacity = self._next_prime(new_capacity)
            
        #     # Make new bucket array with new_capacity size
        #     new_buckets = DynamicArray()
        #     for _ in range(new_capacity):
        #         new_buckets.append(None)

        #     # remember to rehash non-deleted entries into new table
        #     for i in range(self._capacity):
        #         if (self._buckets[i] == None):
        #             # Keep moving
        #             continue
        #         elif (self._buckets[i].is_tombstone == True):
        #             # Keep moving
        #             continue
        #         else:
        #             # Add item to new array
        #             new_entry = HashEntry(self._buckets[i].key, self._buckets[i].value)
        #             init_idx = self._hash_function(self._buckets[i].key) % new_capacity
        #             j = 0
        #             added = False
        #             while (added == False):
        #                 cur_idx = (init_idx + (j ** 2)) % new_capacity
        #                 if (new_buckets[cur_idx] == None):
        #                     # No item at index. Add new item.
        #                     new_buckets[cur_idx] = new_entry
        #                     added = True
        #                 else:
        #                     # Different item occupying index. Continue quadratic probing.
        #                     j += 1

        #     self._buckets = new_buckets
        #     self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        Returns value associated with key. Return None if not in hash map.
        """
        value = None

        init_idx = self._hash_function(key) % self._capacity
        j = 0
        done = False
        # Search via quadratic probing until key is found or an empty spot is found
        while (done == False):
            cur_idx = (init_idx + (j ** 2)) % self._capacity
            if (self._buckets[cur_idx] == None):
                # Item not in array
                done = True
            elif (self._buckets[cur_idx].key == key):
                # Key found. Check if it's a tombstone.
                if (self._buckets[cur_idx].is_tombstone == True):
                    # Item existed but was deleted. Continue quadratic probing.
                    j += 1
                else:
                    # Key found
                    value = self._buckets[cur_idx].value
                    done = True
            else:
                # Different key occupying index. Continue quadratic probing
                j += 1

        return value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the map. Else returns false.
        """
        value = False

        init_idx = self._hash_function(key) % self._capacity
        j = 0
        done = False
        # Search via quadratic probing until key is found or an empty spot is found
        while (done == False):
            cur_idx = (init_idx + (j ** 2)) % self._capacity
            if (self._buckets[cur_idx] == None):
                # Item not in array
                done = True
            elif (self._buckets[cur_idx].key == key):
                # Key found. Check if it's a tombstone.
                if (self._buckets[cur_idx].is_tombstone == True):
                    # Item existed but was deleted. Continue quadratic probing.
                    j += 1
                else:
                    # Key found
                    value = True
                    done = True
            else:
                # Different key occupying index. Continue quadratic probing
                j += 1

        return value

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the map.
        If key not in hash map, does nothing.
        """
        init_idx = self._hash_function(key) % self._capacity
        j = 0
        done = False
        # Search via quadratic probing until key is found or an empty spot is found
        while (done == False):
            cur_idx = (init_idx + (j ** 2)) % self._capacity
            if (self._buckets[cur_idx] == None):
                # Item not in array
                done = True
            elif (self._buckets[cur_idx].key == key):
                # Key found. Check if it's a tombstone.
                if (self._buckets[cur_idx].is_tombstone == True):
                    # Item existed but was deleted. Continue quadratic probing.
                    j += 1
                else:
                    # Key found, delete it.
                    self._buckets[cur_idx].is_tombstone = True
                    self._size -= 1
                    done = True
            else:
                # Different key occupying index. Continue quadratic probing
                j += 1

    def clear(self) -> None:
        """
        Clears all contents of map. Capacity remains unchanged.
        """
        for i in range(self._capacity):
            self._buckets[i] = None

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Create and return a dynamic array of all elements in the HashMap.
        """
        # Create array
        keys_with_values = DynamicArray()

        # Search through all buckets. Add all key/value pairs that aren't tombstones.
        for i in range(self._capacity):
            if (self._buckets[i] != None):
                if (self._buckets[i].is_tombstone == False):
                    keys_with_values.append((self._buckets[i].key, self._buckets[i].value))

        return keys_with_values


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

        if m.table_load() > 0.5:
            # print(f"Table Size: {m._size}, Table Capacity: {m._capacity}")
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
