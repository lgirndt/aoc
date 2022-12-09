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


class Robe:
    def __init__(self, head=Point(0,0), tail=Point(0,0),matrix_size=5):
        self.head = head
        self.tail = tail
        self.tail_visits = {self.tail}
        self.matrix_size=matrix_size

    def follow_head(self):
        diff = self.head - self.tail
        if diff.abs().x <= 1 and diff.abs().y <= 1:
            return self
        self.move_tail(self.tail + diff.sign())
        return self

    def move_tail(self, new_position):
        self.tail_visits.add(new_position)
        self.tail = new_position

    def move_head(self, new_position):
        self.head = new_position
        self.follow_head()

    def apply_step_to_head(self, step):
        self.move_head(self.head + step)
        return self

    def count_tail_visits(self):
        return len(self.tail_visits)

    def print(self):
        for y in reversed(range(0,self.matrix_size)):
            for x in range(0,self.matrix_size):
                p = Point(x,y)
                c = '.'
                if p == Point(0,0):
                    c = 's'
                if p == self.tail:
                    c = 'T'
                if p == self.head:
                    c = 'H'
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

def run_on_file(file_name):
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
        steps = convert_to_steps(lines)
        robe = Robe()
        for step in steps:
            robe.apply_step_to_head(step)
            #robe.print()
        return robe.count_tail_visits()

if __name__ == '__main__':
    count = run_on_file("./dev09_input.txt")
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
    assert Robe(head=Point(1,0)).follow_head().tail == Point(0,0)
    assert Robe(head=Point(0, 1)).follow_head().tail == Point(0, 0)
    assert Robe(head=Point(-1,0)).follow_head().tail == Point(0,0)
    assert Robe(head=Point(0, -1)).follow_head().tail == Point(0, 0)

    assert Robe(head=Point(2,0)).follow_head().tail == Point(1,0)
    assert Robe(head=Point(0, 2)).follow_head().tail == Point(0, 1)
    assert Robe(head=Point(-2,0)).follow_head().tail == Point(-1,0)
    assert Robe(head=Point(0, -2)).follow_head().tail == Point(0, -1)

    assert Robe(head=Point(1, 1)).follow_head().tail == Point(0, 0)
    assert Robe(head=Point(2, 2)).follow_head().tail == Point(1, 1)
    assert Robe(head=Point(3, 5)).follow_head().tail == Point(1, 1)

    assert Robe(head=Point(3, 0)).follow_head().tail == Point(1, 0)
    assert Robe(head=Point(3, 0), tail=Point(1,0)).follow_head().tail == Point(2, 0)

def test_apply_step_to_head():
    assert Robe(head=Point(3,2)).apply_step_to_head(Point(1,0)).head == Point(4,2)


def test_Robe_init():
    r = Robe()
    assert r.count_tail_visits() == 1
    assert {Point()} == r.tail_visits


def test_convert_to_steps():
    assert convert_to_steps(["R 1"]) == [Point(1,0)]
    assert convert_to_steps(["L 1"]) == [Point(-1, 0)]
    assert convert_to_steps(["U 1"]) == [Point(0, 1)]
    assert convert_to_steps(["D 1"]) == [Point(0, -1)]

    assert convert_to_steps(["R 4"]) == [Point(1, 0),Point(1, 0),Point(1, 0),Point(1, 0)]

    assert convert_to_steps(["R 2","U 3"]) == [Point(1, 0), Point(1, 0), Point(0, 1), Point(0, 1), Point(0, 1)]


def assert_test_data():
    assert run_on_file("./dev09_input_test.txt") == 13