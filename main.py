class Heap:
    def __init__(self):
        self.pages = {}
        self.current_page = None

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

    def get_object(self, address):
        return self.objects[address]


class Reference:
    def __init__(self, address):
        self.address = address
        self.finalizable = False
        self.marked0 = phase == 0
        self.marked1 = phase == 1
        self.remapped = phase == 2


class Object:
    def __init__(self, name):
        self.name = name
        self.references = list()


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
        new_address = copy(object)
        forwarding_table[old_address] = new_address


def copy(object):
    return None


def stw1():
    pass


def stw3():
    pass


def mark_barrier():
    pass


def load_barrier():
    pass


phase = 0
forwarding_table = {}
roots = []
heap = Heap()
