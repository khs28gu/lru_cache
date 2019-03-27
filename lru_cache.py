from node import Node

class LRUCache:

    def __init__(self, maximum_capacity):
        self.maximum_capacity = maximum_capacity
        self.current_capacity = 0
        self.cache = dict()
        self.head = None
        self.tail = None

    def insert_at_start(self, node):
        # Format node to become the new head
        node.previous = None

        # Current head becomes second element in linked list
        node.next = self.head
        
        # To handle circular reference and make sure objects are equal
        node.next.previous = node
        
        # Set hash lookup for new head and old head
        self.cache[node.key] = node
        self.cache[node.next.key] = node.next

        # Set node to be new head
        self.head = node

    def move_from_middle(self, node):
        node.next.previous = node.previous
        node.previous.next = node.next

        self.insert_at_start(node)
    
    def replace_tail(self):
        self.tail = self.tail.previous
        self.tail.next = None
        self.cache[self.tail.key] = self.tail

    def delete_last_used(self):
        del self.cache[self.tail.key]
        self.replace_tail()
    
    def add_to_cache(self, node):
        # This method is only used if key does exist
        if self.current_capacity == 0:
            self.head = node
            self.tail = node
            self.cache[self.head.key] = self.head
            self.current_capacity += 1

        elif self.current_capacity == 1 and self.maximum_capacity == 1:
            del self.cache[self.head.key]
            self.head = node
            self.tail = node
            self.cache[self.head.key] = self.head
            
        elif self.current_capacity == 1:
            self.tail = self.head
            self.tail.previous = node
            
            node.next = self.tail
            
            self.head = node
            self.cache[self.head.key] = self.head
            self.cache[self.tail.key] = self.tail
            self.current_capacity += 1
        else:
            # This will only be tiggered if cache is at capacity
            if self.current_capacity == self.maximum_capacity:
                self.delete_last_used()
            else:
                self.current_capacity += 1
            
            self.insert_at_start(node)
            
    def update_cache(self, node):
        # This method is only used if key exists
        if self.head and node.key == self.head.key:
            pass
        
        elif self.tail and node.key == self.tail.key:
            self.replace_tail()
            self.insert_at_start(node)
        
        else:
            self.move_from_middle(node)
        
    def put(self, key, value):
        # Could check to see if key exists in cache but it results in an extra lookup
        try:
            node = self.cache[str(key)]
            node.value = value
            node_exists = True
        except:
            node = Node(str(key), value)
            node_exists = False

        if node_exists:
            self.update_cache(node)
        else:
            self.add_to_cache(node)

    def get(self, key):
        try:
            node = self.cache[str(key)]
            node_exists = True
        except:
            node_exists = False
        
        if node_exists:
            if self.maximum_capacity != 1:
                self.update_cache(node)
            return node.value
        else:
            return -1

    def _traverse_cache(self, node):
        cache_list = list()
        cache_list.append({node.key: node.value})

        if node.next:
            cache_list += self._traverse_cache(node.next)
        
        return cache_list

    def _reverse_cache(self, node):
        cache_list = list()
        cache_list.append({node.key: node.value})

        if node.previous:
            cache_list += self._traverse_cache(node.previous)
        
        return cache_list

    def __repr__(self):
        if self.head:
            return str(self._traverse_cache(self.head))
        else:
            return str(list())