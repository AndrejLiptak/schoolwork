from typing import List, Tuple, Optional


class Person:
    def __init__(self, info):
        self.name = info[0]
        self.born_year = info[1]
        self.eye_color = info[2]
        self.parent = None
        self.children = []

    def validate_eye_color(self, color: str) -> bool:
        if self.eye_color != color:
            return False
        for child in self.children:
            if not child.validate_eye_color(color):
                return False
        return True

    def validate_children_min(self, color: str, count: int) -> bool:
        if color == self.eye_color:
            if len(self.children) < count:
                return False
            for child in self.children:
                if not child.validate_children_min(color, count):
                    return False
        return True

    def color_eyed_rec(self, color, my_list):
        if self.eye_color == color:
            my_list.append(self)
        for child in self.children:
            child.color_eyed_rec(color, my_list)

    def color_eyed_people(self, color: str) -> List['Person']:
        my_list = []
        self.color_eyed_rec(color, my_list)
        return my_list

    def aunt_eye_rec(self, color, result):
        if self.parent is not None:
            if self.parent.parent is not None:
                aunts = self.parent.parent.children.copy()
                aunts.remove(self.parent)
                for aunt in aunts:
                    if aunt.eye_color == color:
                        result.append(self)
        for child in self.children:
            child.aunt_eye_rec(color, result)

    def people_with_color_eyed_aunts(self, color: str) -> List['Person']:
        result = []
        self.aunt_eye_rec(color, result)
        return result

    def youngest_mother_rec(self, youngest, minimum):
        for child in self.children:
            if child.born_year - self.born_year < minimum:
                youngest = self
                minimum = child.born_year - self.born_year
        for child in self.children:
            youngest, minimum = child.youngest_mother_rec(youngest, minimum)
        return youngest, minimum

    def youngest_mother(self) -> Optional['Person']:
        if not self.children:
            return None
        youngest, minimum = self.youngest_mother_rec(
            self, self.children[0].born_year - self.born_year)
        return youngest

    def draw_tree_rec(self, depth):
        print('.' * (depth * 3) + self.name + ' (' + str(self.born_year) + ')')
        for child in sorted(self.children, key=lambda x: x.name):
            child.draw_tree_rec(depth + 1)

    def draw_family_tree(self) -> None:
        self.draw_tree_rec(0)

    def change_eye_color(self, old: str, new: str) -> None:
        if self.eye_color == old:
            self.eye_color = new
        for child in self.children:
            child.change_eye_color(old, new)

    def siblings_eye_color(self, parent):
        if len(parent.children) == 1:
            return True
        siblings = parent.children.copy()
        siblings.remove(self)
        color = siblings[0].eye_color
        for sibling in siblings:
            if sibling.eye_color != color:
                return False
        return True

    def change_born_year(self, increment: int) -> None:
        if self.parent is None or self.siblings_eye_color(self.parent):
            self.born_year += increment
        for child in self.children:
            child.change_born_year(increment)

    def count_offsprings(self, total):
        total += len(self.children)
        for child in self.children:
            total = child.count_offsprings(total)
        return total

    def cut_color_rec(self, color, total):
        if self.eye_color == color:
            if self.parent is not None:
                self.parent.children.remove(self)
            total = self.count_offsprings(total + 1)
            return total
        for child in self.children.copy():
            total = child.cut_color_rec(color, total)
        return total

    def cut_color_eyed(self, color: str) -> int:
        return self.cut_color_rec(color, 0)

    def check_years_interval(self, start, end):
        for child in self.children:
            if not child.check_years_interval(start, end):
                return False
            if not start <= child.born_year <= end:
                return False
        return True

    def cut_all(self):
        if self.parent is not None:
            self.parent.children.remove(self)
        for child in self.children.copy():
            child.cut_all()

    def cut_subtree_rec(self, start, end):
        if self.check_years_interval(start, end):
            self.cut_all()
        else:
            for child in self.children.copy():
                child.cut_subtree_rec(start, end)

    def cut_subtree_years(self, start: int, end: int) -> bool:
        if self.check_years_interval(start, end):
            remove_root = True
        else:
            remove_root = False
        self.cut_subtree_rec(start, end)
        return remove_root


def build_tree(persons: List[Tuple[str, int, str]],
               relations: List[Tuple[str, str]]) -> Optional['Person']:
    names = {}
    if not persons and not relations:
        return None
    for person in persons:
        names[person[0]] = Person(person)
    for relation in relations:
        names[relation[0]].children.append(names[relation[1]])
        names[relation[1]].parent = names[relation[0]]
    for person in names.values():
        if person.parent is None:
            return person
