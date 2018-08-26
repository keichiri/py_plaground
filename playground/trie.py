class _Node:
    __slots__ = 'item', 'value', '_first_child', '_next_sibling'

    def __init__(self, item=None, value=None, next_sibling=None):
        self.item = item
        self.value = value
        self._next_sibling = next_sibling
        self._first_child = None

    @property
    def has_children(self):
        return self._first_child is not None

    def get_child(self, item):
        if not self._first_child:
            return None

        child = self._first_child
        while child:
            if child.item == item:
                return child

            child = child._next_sibling

        return None

    def create_child(self, item):
        child = _Node(item)
        if not self._first_child:
            self._first_child = child
            return child

        existing_child = self._first_child
        while existing_child._next_sibling:
            existing_child = existing_child._next_sibling

        existing_child._next_sibling = child

        return child

    def set_value(self, value):
        self.value = value

    def remove_child(self, item):
        if not self._first_child:
            raise ValueError('No children')

        if self._first_child.item == item:
            self._first_child = self._first_child._next_sibling
            return

        node = self._first_child
        sibling = node._next_sibling

        while sibling:
            if sibling.item == item:
                node._next_sibling = sibling._next_sibling
                return

            node = sibling
            sibling = sibling._next_sibling

        raise ValueError(f'No such child')

    def get_children(self):
        children = []
        child = self._first_child

        while child:
            children.append(child)
            child = child._next_sibling

        return children

    def gen(self, prefix=None):
        if prefix is None:
            key = ''
        else:
            key = prefix + self.item

        if self.value:
            yield key, self.value

        child = self._first_child
        while child:
            yield from child.gen(key)
            child = child._next_sibling


class Trie:
    """
    API:
        * set(key, value)
        * get(key)
        * remove(key)
        * get_all()
    """

    def __init__(self, items=None):
        self._root = _Node()
        self._node_size = 0
        self._size = 0

        if items:
            for key, value in items.items():
                self.set(key, value)

    @property
    def size(self):
        return self._size

    def set(self, key, value):
        node = self._root

        for char in key:
            child = node.get_child(char)
            if not child:
                child = node.create_child(char)
                self._node_size += 1

            node = child

        assert not node.value
        node.set_value(value)
        self._size += 1

    def get(self, key):
        node = self._root

        for char in key:
            node = node.get_child(char)
            if not node:
                return None

        return node.value

    def remove(self, key):
        node = self._root
        nodes = [self._root]

        for char in key:
            node = node.get_child(char)
            if not node:
                raise ValueError(f'No such key {key}')

            nodes.append(node)

        value_node = nodes[-1]
        if not value_node.value:
            raise ValueError(f'Node has no value. Key: {key}')

        value_node.set_value(None)
        self._size -= 1
        if value_node.has_children:
            return

        parents = nodes[:-1]
        for parent, char in zip(reversed(parents), reversed(key)):
            parent.remove_child(char)
            self._node_size -= 1
            if parent.has_children or parent.value:
                break

    def __iter__(self):
        yield from self._root.gen()