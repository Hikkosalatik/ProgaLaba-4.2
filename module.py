class Node:
    def __init__(self, inf):
        self.inf = inf
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0


def EmptyList(l: LinkedList) -> bool:
    return l.head is None


def InitializeLinkedList():
    return LinkedList()


def ClearLinkedList(l: LinkedList) -> None:
    if EmptyList(l):
        return

    while l.head is not None:
        n = l.head
        l.head = n.next
        n.prev = None
        n.next = None

    l.tail = None
    l.count = 0


def DeleteNode(l: LinkedList, idx: int) -> None:
    if EmptyList(l):
        return

    if idx < 0 or idx >= l.count:
        return

    if idx == 0:
        n = l.head
        l.head = n.next
        if l.head is not None:
            l.head.prev = None
        else:
            l.tail = None
        l.count -= 1
        return

    if idx == l.count - 1:
        n = l.tail
        l.tail = n.prev
        if l.tail is not None:
            l.tail.next = None
        else:
            l.head = None
        l.count -= 1
        return

    n = l.head
    for _ in range(idx):
        n = n.next
    n.prev.next = n.next
    n.next.prev = n.prev
    l.count -= 1


def InsertNode(l: LinkedList, k: int, idx: int) -> None:
    if idx < 0 or idx > l.count:
        return

    n = Node(k)
    n.inf = k
    n.next = None
    n.prev = None

    if l.count == 0:
        l.head = n
        l.tail = n
        l.count = 1
        return

    if idx == 0:
        n.next = l.head
        l.head.prev = n
        l.head = n
        l.count += 1
        return

    if idx == l.count:
        n.prev = l.tail
        l.tail.next = n
        l.tail = n
        l.count += 1
        return

    m = l.head
    for _ in range(idx):
        m = m.next
    n.next = m
    n.prev = m.prev
    m.prev.next = n
    m.prev = n
    l.count += 1


def ReadAllElements(l: LinkedList) -> str:
    res = ""
    if EmptyList(l):
        res = "Список пуст, читать нечего"
        return res

    n = l.head
    while n is not None:
        res += str(n.inf) + " "
        n = n.next

    res = res + "Количество элементов: " + str(l.count)
    return res


def ReadOneElement(l: LinkedList, TargetIndex: int) -> int:
    if EmptyList(l) or TargetIndex < 0 or TargetIndex >= l.count:
        raise ValueError("Список пуст или индекс не корректен\n")

    n = l.head
    count = 0
    while count < TargetIndex:
        n = n.next
        count += 1
    return n.inf


def ReverseList(l: LinkedList) -> None:
    if EmptyList(l) or l.count == 1:
        return

    tw = LinkedList()

    while l.count != 0:
        k = ReadOneElement(l, l.count - 1)
        DeleteNode(l, l.count - 1)
        InsertNode(tw, k, tw.count)

    l.head = tw.head
    l.tail = tw.tail
    l.count = tw.count
