from matplotlib.pyplot import imshow
from numpy import *
from random import sample


def translate_point(point, translation):
    print(point, translation)
    return (point[0] + translation[0]), (point[1] + translation[1])

def generate_candidates(point, selector, n):
    candidates = set()
    while len(candidates) < n:
        # generate random points inside the selector's bounding box
        metacandidate = random.randint(0, selector.shape[0]),\
                        random.randint(0, selector.shape[1])
        # accept points covered by the selector
        if selector[metacandidate]:
            candidates.add(metacandidate)
    candidates = [translate_point(candidate, point) for candidate in candidates]
    return candidates

def distance_between_points(point_1, point_2):
    # Pythagorean theorem
    return sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

distance_between_points((1, 1), (5, 4))

def generate_annular_selector(r_o, r_i):
    size = int(ceil(2 * r_o + 1))
    center = (r_o, r_o)
    selector = zeros((size, size))  # bounding box
    for y in range(size):
        for x in range(size):
            distance = distance_between_points((x, y), center)
            if distance > r_i and distance < r_o + 1:
                selector[y][x] = 1
    return selector

def check_collisions(grid, candidate, collider):
    collider_t = [translate_point(point, candidate)
                  for point in grid_to_list(collider)]
    for point in collider_t:
        if grid[point]:
            return True
    return False


if __name__ == "__main__":
    r = 3.0
    sx = 15  # Physical grid size (external units, e.g. meters)
    sy = 15
    n_candidates = 30
    n = sx * sy
    cell_size_upper_bound = r / sqrt(n)
    cell_size = 10 ** (ceil(log10(cell_size_upper_bound)) - 1)

    s1 = int(sx / cell_size)  # Logical grid size (internal units for Bridson's algorithm)
    s2 = int(sy / cell_size)
    sr = r / cell_size  # Logical Poisson disc radius

    grid = zeros((s1, s2))
    grid = grid.astype(int)
    grid.fill(-1)
    start_point = random.randint(0, grid.shape[0]), random.randint(0, grid.shape[1])
    print(start_point)

    grid[start_point] = 0  # 0 is the first point index so can be hardcoded
    active_points = {start_point}  # Start the active points set

    while active_points:
        active_point = sample(active_points, 1)[0]
        print(active_point)
        annulus = generate_annular_selector(2 * r, r)
        collider = generate_annular_selector(r, 0)
        candidates = generate_candidates(active_point, annulus, n_candidates)
        succeeded = False
        for candidate in candidates:
            if not check_collisions(grid, candidate, collider):  # check if point can fit
                active_points.add(candidate)  # add point to active_points
                grid[int(candidate)] = len(active_points) - 1  # add index to grid
                succeeded = True
        if not succeeded:
            active_points.remove(active_point)

