import itertools

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __repr__(self):
        return "Point({0},{1})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def sign(self):
        return Point(
            0 if self.x == 0 else abs(self.x)//self.x,
            0 if self.y == 0 else abs(self.y)//self.y)

    def abs(self):
        return Point(abs(self.x), abs(self.y))


class Rope:
    def __init__(self,n=2, head=Point(0,0),matrix_size=5):
        self.knots = [Point(0,0)]*n
        self.knots[0] = head
        self.tail_visits = {self.knots[-1]}
        self.matrix_size=matrix_size

    def _follow_knot(self, knot):
        head = self.knots[knot]
        tail = self.knots[knot+1]
        diff = head - tail
        if diff.abs().x <= 1 and diff.abs().y <= 1:
            return self
        self._set_knot(knot+1, tail + diff.sign())
        return self

    def _set_knot(self, knot, new_position):
        if knot == len(self.knots)-1:
            self.tail_visits.add(new_position)
        self.knots[knot] = new_position

    def _move_head(self, new_position):
        self.knots[0] = new_position
        for knot in range(0,len(self.knots)-1):
            self._follow_knot(knot)

    def apply_step_to_head(self, step):
        self._move_head(self.knots[0] + step)
        return self

    def count_tail_visits(self):
        return len(self.tail_visits)

    def print(self):
        min_x = min(0,min(p.x for p in self.knots))
        max_x = max(self.matrix_size,max(p.x for p in self.knots))
        min_y = min(0, min(p.y for p in self.knots))
        max_y = max(self.matrix_size, max(p.y for p in self.knots))
        for y in reversed(range(min_y, max_y)):
            for x in range(min_x,max_x):
                p = Point(x,y)
                c = '.'
                if p == Point(0,0):
                    c = 's'
                for i,k in enumerate(self.knots):
                    if p == k:
                        c = i
                print(c, end="")
            print()
        print()

def convert_to_steps(lines):

    dir_mapping = {
        "R": Point(1,0),
        "L": Point(-1,0),
        "U": Point(0,1),
        "D": Point(0,-1)
    }

    def _convert_line(line):
        direction, count = line.split(" ")
        return [dir_mapping[direction]]*int(count)

    return list(itertools.chain(*[_convert_line(line) for line in lines]))

def run_on_file(file_name, n=2):
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
        steps = convert_to_steps(lines)
        rope = Rope(n=n)
        for step in steps:
            rope.apply_step_to_head(step)
            # rope.print()
        return rope.count_tail_visits()

if __name__ == '__main__':
    count = run_on_file("./dev09_input.txt", n=10)
    print(count)

def test_point_eq():
    assert Point(0,0) == Point(0,0)
    assert Point(1,1) != Point(2,2)
    assert Point(23,42) == Point(23,42)


def test_point_add():
    assert Point(1,2) + Point(3,4) == Point(4,6)


def test_point_sub():
    assert Point(4,6) - Point(3,4) == Point(1,2)


def test_sign():
    assert Point(4,3).sign() == Point(1,1)
    assert Point(4, 0).sign() == Point(1, 0)
    assert Point(0, 3).sign() == Point(0, 1)

    assert Point(-4, -3).sign() == Point(-1, -1)
    assert Point(-4, 0).sign() == Point(-1, 0)
    assert Point(0, -3).sign() == Point(0, -1)


def test_follow_head():
    assert Rope(head=Point(1, 0))._follow_knot(0).knots[1] == Point(0, 0)
    assert Rope(head=Point(0, 1))._follow_knot(0).knots[1] == Point(0, 0)
    assert Rope(head=Point(-1, 0))._follow_knot(0).knots[1] == Point(0, 0)
    assert Rope(head=Point(0, -1))._follow_knot(0).knots[1] == Point(0, 0)

    assert Rope(head=Point(2, 0))._follow_knot(0).knots[1] == Point(1, 0)
    assert Rope(head=Point(0, 2))._follow_knot(0).knots[1] == Point(0, 1)
    assert Rope(head=Point(-2, 0))._follow_knot(0).knots[1] == Point(-1, 0)
    assert Rope(head=Point(0, -2))._follow_knot(0).knots[1] == Point(0, -1)

    assert Rope(head=Point(1, 1))._follow_knot(0).knots[1] == Point(0, 0)
    assert Rope(head=Point(2, 2))._follow_knot(0).knots[1] == Point(1, 1)
    assert Rope(head=Point(3, 5))._follow_knot(0).knots[1] == Point(1, 1)

    assert Rope(head=Point(3, 0))._follow_knot(0).knots[1] == Point(1, 0)
    r = Rope(head=Point(3, 0))
    r.knots[1] = Point(1, 0)
    assert r._follow_knot(0).knots[1] == Point(2, 0)

def test_apply_step_to_head():
    assert Rope(head=Point(3, 2)).apply_step_to_head(Point(1, 0)).knots[0] == Point(4, 2)


def test_rope_init():
    r = Rope()
    assert r.count_tail_visits() == 1
    assert {Point()} == r.tail_visits


def test_convert_to_steps():
    assert convert_to_steps(["R 1"]) == [Point(1,0)]
    assert convert_to_steps(["L 1"]) == [Point(-1, 0)]
    assert convert_to_steps(["U 1"]) == [Point(0, 1)]
    assert convert_to_steps(["D 1"]) == [Point(0, -1)]

    assert convert_to_steps(["R 4"]) == [Point(1, 0),Point(1, 0),Point(1, 0),Point(1, 0)]

    assert convert_to_steps(["R 2","U 3"]) == [Point(1, 0), Point(1, 0), Point(0, 1), Point(0, 1), Point(0, 1)]


def test_assert_test_data():
    assert run_on_file("./dev09_input_test.txt") == 13

def test_assert_test_data2():
    assert run_on_file("./dev_09_input_test2.txt", n=10) == 36