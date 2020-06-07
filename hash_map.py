# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================
# Layout and design from CS 261 skeleton code
# Author: Ray Franklin
# Date: 06/06/2020
# with help from https://stackabuse.com/


class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        # iterate over table and replace each node with a new empty one
        for i in range(self.capacity):
            self._buckets[i] = LinkedList()

        self.size = 0  # reset the size to empty (zero)

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        index = self.get_index(key)
        node = self._buckets[index].contains(key)
        if node:
            return node.value
        return None

    def get_node(self, key):
        """
        Returns the SLNode object with the given key
        :param key: the value of the kye to look for
        :return: The SLNode associated with the key. None if it is not found
        """
        index = self.get_index(key)
        node = self._buckets[index].contains(key)
        if node:
            return node
        return None

    def get_index(self, key):
        """
        Returns the index of the hashed key.
        :param key: The key to has for an index
        :return: The index of the hashed key
        """
        return self._hash_function(key) % self.capacity

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        buckets = self._buckets  # store the old list
        self.capacity = capacity  # update to the new capacity
        self._buckets = []  # empty the list
        self.size = 0

        # create our new table with empty nodes
        for i in range(capacity):
            self._buckets.append(LinkedList())

        # check each bucket to see if it has values in it
        for linked_list in buckets:
            # if we find a value, check each one and rehash to our new table
            if linked_list.head is not None:
                # add each old value into the new buckets
                curr = linked_list.head
                while curr is not None:
                    self.put(curr.key, curr.value)
                    curr = curr.next

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        current_node = self.get_node(key)
        # key already exists, update its value
        if current_node:
            current_node.value = value
        else:
            # doesn't exits, add a new node
            index = self.get_index(key)  # hash out our location

            # add in the key to our linked list indexed at that bucket
            self._buckets[index].add_front(key, value)
            self.size += 1  # update the size for each pair added

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        index = self.get_index(key)
        self._buckets[index].remove(key)

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise
        """
        if self.get(key):
            return True
        return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        total = 0
        for bucket in self._buckets:
            if bucket.head is None:
                total += 1
        return total

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return float(self.size / self.capacity)

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
