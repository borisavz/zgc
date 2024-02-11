from enum import Enum
from uuid import uuid4


class GlobalPhase(Enum):
    MARKING = 0
    REMAPPING = 1


class MarkingPhase(Enum):
    MARKING0 = 0
    MARKING1 = 1

    def next_phase(self, current):
        if current == MarkingPhase.MARKING0:
            return MarkingPhase.MARKING1

        return MarkingPhase.MARKING0


phase = GlobalPhase.MARKING
mark_phase = MarkingPhase.MARKING0
forwarding_table = {}
roots = []
mark_stack = []


class Heap:
    def __init__(self):
        self.current_page_address = uuid4()
        self.pages = {
            self.current_page_address: Page()
        }

    def add_object(self, object):
        object_address = self.pages[self.current_page_address].add_object(object)

        return (self.current_page_address, object_address)

    def get_object(self, address):
        page_address = address[0]
        object_address = address[1]

        return self.pages[page_address].get_object(object_address)

    def remove_page(self, page_address):
        del self.pages[page_address]

    def get_evacuation_candidates(self):
        evacuation_candidates = []

        for p in self.pages.items():
            if p[1].evacuation_candidate:
                evacuation_candidates.append(p)

        return evacuation_candidates


class Page:
    def __init__(self):
        self.objects = {}
        self.evacuation_candidate = False
        self.relocatable = False

    def add_object(self, object):
        object_address = uuid4()
        self.objects[object_address] = object
        return object_address

    def get_object(self, address):
        return self.objects[address]


class Reference:
    def __init__(self, address):
        self.address = address
        self.finalizable = False
        self.marked0 = False
        self.marked1 = False
        self.remapped = False

        self.color()

    def color(self):
        global phase, mark_phase

        if phase == GlobalPhase.MARKING:
            self.marked0 = mark_phase == MarkingPhase.MARKING0
            self.marked1 = mark_phase == MarkingPhase.MARKING1
            self.remapped = False
        else:
            self.marked0 = False
            self.marked1 = False
            self.remapped = True


class Object:
    def __init__(self, name, references=None):
        if references is None:
            references = []

        self.name = name
        self.references = references

    def copy(self):
        return Object(self.name, self.references)


def marking_remapping():
    pass


def relocation():
    evacuation_candidates = heap.get_evacuation_candidates()

    for p in evacuation_candidates:
        for o in p[1].objects.items():
            relocate(o[0], o[1])

        heap.remove_page(p[0])


def relocate(old_address, object):
    if old_address not in forwarding_table:
        new_object = object.copy()
        new_address = heap.add_object(new_object)

        forwarding_table[old_address] = new_address


def stw1():
    global mark_phase

    for r in roots:
        r.color()

    mark_phase = mark_phase.next_phase(mark_phase)


def stw3():
    pass


def mark_barrier():
    pass


def load_barrier():
    pass


heap = Heap()

a = Object('a')
b = Object('b')
c = Object('c')

addr_a = heap.add_object(a)
addr_b = heap.add_object(b)
addr_c = heap.add_object(c)

roots.append(Reference(addr_a))
roots.append(Reference(addr_b))
roots.append(Reference(addr_c))
