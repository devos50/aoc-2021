class SnailfishNumberNode:

    def __init__(self, left, right, value, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    @staticmethod
    def from_str(raw_str):
        if raw_str.isdigit():
            return SnailfishNumberNode(None, None, int(raw_str))

        # Find the left part
        if raw_str[1] == '[':
            end_ind_left_part = parse_part(raw_str, 1)
        else:
            # Parse number until end
            end_ind_left_part = 1
            while raw_str[end_ind_left_part] in "0123456789":
                end_ind_left_part += 1
            end_ind_left_part -= 1

        # print("left: %s" % raw_str[1:end_ind_left_part + 1])
        # print("right: %s" % raw_str[end_ind_left_part + 2:len(raw_str) - 1])
        left_node = SnailfishNumberNode.from_str(raw_str[1:end_ind_left_part + 1])
        right_node = SnailfishNumberNode.from_str(raw_str[end_ind_left_part + 2:len(raw_str) - 1])
        parent = SnailfishNumberNode(left_node, right_node, None)
        left_node.parent = parent
        right_node.parent = parent
        return parent

    def get_root_node(self):
        """
        Return the root node
        """
        cur_node = self
        while cur_node.parent:
            cur_node = cur_node.parent
        return cur_node

    def get_depth(self):
        """
        Get the depth of this node.
        """
        depth = 0
        cur_node = self
        while cur_node.parent:
            cur_node = cur_node.parent
            depth += 1

        return depth

    def get_leaf_nodes(self):
        """
        Return a list of leaf nodes
        """
        if self.left is None and self.right is None:
            return [self]
        return self.left.get_leaf_nodes() + self.right.get_leaf_nodes()

    def is_leaf(self):
        return self.right is None and self.left is None

    def get_magnitude(self):
        """
        Get the magnitude of the number.
        """
        if self.left is None and self.right is None:
            return self.value
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()

    def explode(self):
        leaf_nodes = self.get_root_node().get_leaf_nodes()
        left_leaf_ind = leaf_nodes.index(self.left)
        if left_leaf_ind > 0:
            left_node_to_update = leaf_nodes[left_leaf_ind - 1]
            left_node_to_update.value += self.left.value

        right_leaf_ind = leaf_nodes.index(self.right)
        if right_leaf_ind != len(leaf_nodes) - 1:
            right_node_to_update = leaf_nodes[right_leaf_ind + 1]
            right_node_to_update.value += self.right.value

        parent = self.parent
        new_node = SnailfishNumberNode(None, None, 0, parent=parent)
        if parent.left == self:
            parent.left = new_node
        else:
            parent.right = new_node

    def split(self):
        parent = self.parent
        new_left_node = SnailfishNumberNode(None, None, self.value // 2)
        new_right_node = SnailfishNumberNode(None, None, self.value // 2 if self.value % 2 == 0 else self.value // 2 + 1)
        new_node = SnailfishNumberNode(new_left_node, new_right_node, None, parent=parent)
        new_left_node.parent = new_node
        new_right_node.parent = new_node
        if parent.left == self:
            parent.left = new_node
        else:
            parent.right = new_node

    def __str__(self):
        if not self.left and not self.right:
            return "%s" % self.value
        return "[%s,%s]" % (str(self.left), self.right)

    @staticmethod
    def reduce(root_number):
        for _ in range(500):
            did_operation = False

            # Check if we can explode
            queue = [(root_number, 0)]
            while queue:
                number, lvl = queue.pop(0)
                if lvl >= 4 and not number.is_leaf() and number.left.is_leaf() and number.right.is_leaf():
                    number.explode()
                    print("After explode %s: %s" % (str(number), str(number.get_root_node())))
                    did_operation = True
                    break

                # prepare next iteration
                if not number.is_leaf():
                    queue.insert(0, (number.left, lvl + 1))
                    queue.insert(1, (number.right, lvl + 1))

            if did_operation:
                continue

            # If we cannot explode, check if we can split
            queue = [(root_number, 0)]
            while queue:
                number, lvl = queue.pop(0)
                if number.is_leaf():
                    # Should I split?
                    if number.value >= 10:
                        number.split()
                        print("After split %d: %s" % (number.value, str(number.get_root_node())))
                        did_operation = True
                        break

                # prepare next iteration
                if not number.is_leaf():
                    queue.insert(0, (number.left, lvl + 1))
                    queue.insert(1, (number.right, lvl + 1))

            if not did_operation:
                print("DONE")
                break

    def __add__(self, other):
        new_node = SnailfishNumberNode(self, other, None)
        self.parent = new_node
        other.parent = new_node
        SnailfishNumberNode.reduce(new_node)
        print("after addition: %s" % str(new_node))
        return new_node


def parse_part(raw_str, start_ind):
    stack_size = 1
    char_ind = 1
    # Find matching closing bracket
    while stack_size:
        char_ind += 1
        if raw_str[char_ind] == "]":
            stack_size -= 1
        elif raw_str[char_ind] == "[":
            stack_size += 1

    return char_ind


with open("data/day18.txt") as in_file:
    cur_num = None
    for line in in_file.readlines():
        num = SnailfishNumberNode.from_str(line.strip())
        if not cur_num:
            cur_num = num
        else:
            print("Adding %s and %s" % (str(cur_num), str(num)))
            cur_num += num

    print("Reduced: %s" % str(cur_num))
    print(cur_num.get_magnitude())
