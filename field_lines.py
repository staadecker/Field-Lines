from helper import *

STARTING_POINTS_PER_CHARGE = 8 / Q_CONSTANT
LINE_SEGMENT_LENGTH = 0.01
USE_COLORS = True
K_CONSTANT = 9 * 10 ** 9


def get_points_around_charge(charge):
    starting_vectors = []

    radius = charge.get_radius()

    step = 2 * math.pi / (charge.magnitude * STARTING_POINTS_PER_CHARGE)
    offset = step / 2
    angle = offset
    while angle < 2 * math.pi:
        starting_vectors.append(charge.position.add(Vector.create(radius, angle)))
        angle += step

    return starting_vectors


def calculate_field(charges, position):
    net_field = Vector(0, 0)

    for charge in charges:
        if charge.repels:
            vector = position.subtract(charge.position)
        else:
            vector = charge.position.subtract(position)
        magnitude = K_CONSTANT * charge.magnitude / (vector.get_magnitude() ** 2)
        angle = vector.get_angle()

        net_field = net_field.add(Vector.create(magnitude, angle))

    return net_field


def is_valid_end(end_vector, charges):
    for charge in charges:
        if charge.is_position_inside_item(end_vector):
            return False

    return True


def generate_lines_for_starting_point(starting_point, charges, reverse_follow=False):
    next_start = starting_point
    lines = []
    magnitudes = []
    for i in range(10000):
        field = calculate_field(charges, next_start)

        short_vector = Vector.create(LINE_SEGMENT_LENGTH, field.get_angle())

        if reverse_follow:
            end = next_start.subtract(short_vector)
        else:
            end = next_start.add(short_vector)

        if not is_valid_end(end, charges):
            break

        if Graph.is_within_borders(end):
            lines.append([next_start.get_tuple(), end.get_tuple()])
            magnitudes.append(field.get_magnitude())

        next_start = end

    return lines, magnitudes


def flip_items(charges):
    for charge in charges:
        charge.repels = not charge.repels


def get_field_lines(charges):
    lines = []
    magnitudes = []
    for index, charge in enumerate(charges):
        print(f"Charge ({index} of {len(charges)})...", end="")

        if charge.repels:
            for starting_point in get_points_around_charge(charge):
                (a, b) = generate_lines_for_starting_point(starting_point, charges)
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
        Item(True, 3 * Q_CONSTANT, Vector(0, 1)),
        Item(False, Q_CONSTANT, Vector(0, -1))
    ]

    main(ITEMS)
