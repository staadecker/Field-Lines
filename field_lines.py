from helper import *

STARTING_POINTS_PER_CHARGE = 16 / Q_CONSTANT
LINE_SEGMENT_LENGTH = 0.01
USE_COLORS = True
K_CONSTANT = 9 * 10 ** 9


def get_points_around_item(item):
    starting_vectors = []

    radius = item.get_radius()

    step = 2 * math.pi / (item.magnitude * STARTING_POINTS_PER_CHARGE)
    offset = step / 2
    angle = offset
    while angle < 2 * math.pi:
        starting_vectors.append(item.position.add(Vector.create(radius, angle)))
        angle += step

    return starting_vectors


def calculate_field(items, position):
    net_field = Vector(0, 0)

    for item in items:
        if item.repels:
            vector = position.subtract(item.position)
        else:
            vector = item.position.subtract(position)
        magnitude = K_CONSTANT * item.magnitude / (vector.get_magnitude() ** 2)
        angle = vector.get_angle()

        net_field = net_field.add(Vector.create(magnitude, angle))

    return net_field


def is_valid_end(end_vector, items):
    for item in items:
        if item.is_position_inside_item(end_vector):
            return False

    return True


def generate_lines_for_starting_point(starting_point, items, reverse_follow=False):
    next_start = starting_point
    lines = []
    magnitudes = []
    for i in range(10000):
        field = calculate_field(items, next_start)

        short_vector = Vector.create(LINE_SEGMENT_LENGTH, field.get_angle())

        if reverse_follow:
            end = next_start.subtract(short_vector)
        else:
            end = next_start.add(short_vector)

        if not is_valid_end(end, items):
            break

        if Graph.is_within_borders(end):
            lines.append([next_start.get_tuple(), end.get_tuple()])
            magnitudes.append(field.get_magnitude())

        next_start = end

    return lines, magnitudes


def flip_items(items):
    for item in items:
        item.repels = not item.repels


def get_field_lines(items):
    lines = []
    magnitudes = []
    for index, item in enumerate(items):
        print(f"Calculating field for item ({index} of {len(items)})...", end="")

        if item.repels:
            for starting_point in get_points_around_item(item):
                (a, b) = generate_lines_for_starting_point(starting_point, items)
                lines += a
                magnitudes += b

        print("Done.")
    return lines, magnitudes


def main(items):
    Graph.setup()

    [Graph.draw_item(item) for item in items]

    # Check if at least one item repels. If not we need to flip all the items to get some starting points
    has_repels = False
    for item in items:
        if item.repels:
            has_repels = True
            break

    if not has_repels:
        flip_items(items)

    line_segments, magnitudes = get_field_lines(items)

    Graph.draw_lines(line_segments, convert_magnitudes_to_colors(magnitudes) if USE_COLORS else None)
    Graph.show_graph()


if __name__ == '__main__':
    ITEMS = [
        Item(True, Q_CONSTANT, Vector(0, 2)),
        Item(True, 2 * Q_CONSTANT, Vector(0, -2)),
        Item(False, Q_CONSTANT, Vector(-2, -2)),
        Item(False, Q_CONSTANT, Vector(2, -2))
    ]

    main(ITEMS)
