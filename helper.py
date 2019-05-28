import math
import matplotlib.pyplot as plt
import matplotlib.collections as collections

K_CONSTANT = 9 * 10 ** 9
Q_CONSTANT = 1.602 * 10 ** (-19)
CHARGE_TO_RADIUS_FACTOR = 0.1 / Q_CONSTANT
SIZE_OF_GRAPH = 50


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

    @staticmethod
    def create(magnitude, angle):
        return Vector(magnitude * math.cos(angle), magnitude * math.sin(angle))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Item:
    def __init__(self, repels: bool, magnitude_of_charge, position: Vector):
        self.repels = repels
        self.magnitude = magnitude_of_charge
        self.position = position

    def get_radius(self):
        return self.magnitude * CHARGE_TO_RADIUS_FACTOR

    def is_coordinates_inside_radius(self, position: Vector) -> bool:
        return self.position.subtract(position).get_magnitude() < self.get_radius()


class Graph:
    @staticmethod
    def is_within_borders(end_vector: Vector):
        return -SIZE_OF_GRAPH < end_vector.x < SIZE_OF_GRAPH and -SIZE_OF_GRAPH < end_vector.y < SIZE_OF_GRAPH

    @staticmethod
    def setup():
        axis = plt.gca()
        axis.set_xlim((-SIZE_OF_GRAPH, SIZE_OF_GRAPH))
        axis.set_ylim((-SIZE_OF_GRAPH, SIZE_OF_GRAPH))

    @staticmethod
    def draw_lines(lines_to_draw, colors):
        line_collection = collections.LineCollection(lines_to_draw, colors=colors)
        axis = plt.gca()
        axis.add_collection(line_collection)

    @staticmethod
    def draw_charge(charge):
        axis = plt.gca()
        circle = plt.Circle(charge.position.get_tuple(), charge.get_radius(),
                            color="g" if charge.repels else "r")

        axis.add_artist(circle)

    @staticmethod
    def show_graph():
        plt.show()


def convert_magnitudes_to_colors(magnitudes):
    def magnitude_to_radius(magnitude_to_convert):
        return math.sqrt(1 / magnitude_to_convert)

    max_radius = magnitude_to_radius(min(magnitudes))
    min_radius = magnitude_to_radius(max(magnitudes))

    span = max_radius - min_radius
    target_span = 0.9
    minimum_value = 0.1

    colors = []

    for magnitude in magnitudes:
        ratio = -((magnitude_to_radius(magnitude) - min_radius) / span * target_span) + target_span + minimum_value
        colors.append((ratio, 0, 1-ratio, ratio))
    return colors
