import matplotlib.pyplot as plt
import math
import matplotlib.collections as collections

K_CONSTANT = 9 * 10 ** 9
Q_CONSTANT = 1.602 * 10 ** (-19)
CHARGE_TO_RADIUS_FACTOR = 0.1 / Q_CONSTANT
STARTING_POINTS_PER_CHARGE = 14
SECTOR_LENGTH = 0.01
SIZE_OF_GRAPH = 5


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def get_angle(self):
        return math.atan2(self.y, self.x)

    def get_tuple(self):
        return self.x, self.y

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

    def subtract(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Charge:
    def __init__(self, is_positive, magnitude, position_vector):
        self.is_positive = is_positive
        self.magnitude = magnitude
        self.position_vector = position_vector

    def get_radius(self):
        return self.magnitude * CHARGE_TO_RADIUS_FACTOR

    def vector_is_inside(self, vector: Vector):
        return self.position_vector.subtract(vector).get_magnitude() < self.get_radius()


def draw_lines(lines_to_draw):
    line_collection = collections.LineCollection(lines_to_draw)
    axis = plt.gca()
    axis.add_collection(line_collection)


def create_vector(magnitude, angle):
    return Vector(magnitude * math.cos(angle), magnitude * math.sin(angle))


def calculate_field(charges, position):
    net_field = Vector(0, 0)

    for charge in charges:
        if charge.is_positive:
            vector = position.subtract(charge.position_vector)
        else:
            vector = charge.position_vector.subtract(position)
        magnitude = K_CONSTANT * charge.magnitude / (vector.get_magnitude() ** 2)
        angle = vector.get_angle()

        net_field = net_field.add(create_vector(magnitude, angle))

    return net_field


def draw_charges(charges):
    axis = plt.gca()
    for charge in charges:
        circle = plt.Circle(charge.position_vector.get_tuple(), charge.get_radius(),
                            color="g" if charge.is_positive else "r")

        axis.add_artist(circle)


def get_starting_vectors(charges):
    starting_vectors = []

    for charge in charges:
        if charge.is_positive:
            delta = 2 * math.pi / STARTING_POINTS_PER_CHARGE
            for counter in range(STARTING_POINTS_PER_CHARGE):
                angle = counter * delta
                starting_vectors.append(charge.position_vector.add(create_vector(charge.get_radius(), angle)))

    return starting_vectors


def setup_graph():
    axis = plt.gca()
    axis.set_xlim((-SIZE_OF_GRAPH, SIZE_OF_GRAPH))
    axis.set_ylim((-SIZE_OF_GRAPH, SIZE_OF_GRAPH))


def is_valid_end(end_vector, charges):
    for charge in charges:
        if charge.vector_is_inside(end_vector):
            return False

    return -SIZE_OF_GRAPH < end_vector.x < SIZE_OF_GRAPH and -SIZE_OF_GRAPH < end_vector.y < SIZE_OF_GRAPH


def draw_field(charges):
    setup_graph()
    draw_charges(charges)
    lines = []
    starting_points = get_starting_vectors(charges)
    if not starting_points:
        # Go reverse
        for charge in charges:
            charge.is_positive = not charge.is_positive

        starting_points = get_starting_vectors(charges)
    for start in starting_points:
        next_start = start
        for i in range(100000):
            field = calculate_field(charges, next_start)
            end = next_start.add(create_vector(SECTOR_LENGTH, field.get_angle()))

            if not is_valid_end(end, charges):
                break

            lines.append([next_start.get_tuple(), end.get_tuple()])
            next_start = end
    draw_lines(lines)
    plt.show()


if __name__ == '__main__':
    CHARGES = [
        Charge(True, Q_CONSTANT, Vector(0, 1)),
        Charge(False, Q_CONSTANT, Vector(-2, -2)),
        Charge(False, Q_CONSTANT, Vector(2, -2)),
        Charge(True, 3 * Q_CONSTANT, Vector(0, -2)),
        Charge(False, Q_CONSTANT, Vector(3, -2))
    ]

    draw_field(CHARGES)
