import sys

def parse_coordinates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    x1 = list(map(float, lines[0].split()))
    y1 = list(map(float, lines[1].split()))
    x2 = list(map(float, lines[2].split()))
    y2 = list(map(float, lines[3].split()))
    points1 = list(zip(x1, y1))
    points2 = list(zip(x2, y2))
    return points1, points2


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    # Sort the points primarily by x-coordinate, and by y-coordinate secondarily
    points = sorted(points, key=lambda p: (p[0], p[1]))
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def do_segments_intersect(p1, p2, q1, q2):
    def on_segment(p, q, r):
        if min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1]):
            return True
        return False

    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def check_intersection(hull1, hull2):
    for i in range(len(hull1)):
        for j in range(len(hull2)):
            if do_segments_intersect(hull1[i], hull1[(i + 1) % len(hull1)], hull2[j], hull2[(j + 1) % len(hull2)]):
                return True
    return False


def main(file_path):
    points1, points2 = parse_coordinates(file_path)
    union_hull = convex_hull(points1 + points2)
    x_coords = [p[0] for p in union_hull]
    y_coords = [p[1] for p in union_hull]
    intersect = check_intersection(points1, points2)
    print(' '.join(map(str, x_coords)))
    print(' '.join(map(str, y_coords)))
    print("TRUE" if intersect else "FALSE")


if __name__ == "__main__":
    main("testi/input-1.txt")
