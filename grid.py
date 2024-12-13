# TODO:
# Only one more error handling function to write but then I have to look at how
# passing no window names works
# - check the grid array is formatted correctly. This requires all designations
# of a window be touching eachother.
# - debug function when no window names are passed to it

# Take a 2d array as a grid where each object within the array represents
# the window id and create a window layout

import curses
from curses import wrapper
from typing import Optional, Dict, List


# Error Handling----------------------------------------------------------------
def error_check_for_name_duplication(window_names: Dict[int, str]):
    names_list = list(window_names.values())
    if len(names_list) != len(set(names_list)):
        raise ValueError("Window names cannot be duplicated")


def error_check_for_equal_array_lengths(window_layout: List[List[int]]):
    for rows in window_layout:
        if len(rows) != len(window_layout[0]):
            raise ValueError("All list lengths must be equal")


def error_check_for_correct_window_formatting(window_layout: List[List[int]]):
    window_points = {}
    for y, row in enumerate(window_layout):
        for x, window_id in enumerate(row):
            # print(f"ID at (y:{y}, x:{x}) {window_id}")
            if window_id not in window_points:
                window_points[window_id] = (y, x)


# Utility Functions-------------------------------------------------------------
def define_window_key_points():
    pass


def define_window_length_and_width():
    pass


# Main function-----------------------------------------------------------------
def grid(
    win: curses.window,
    window_layout: List[List[int]],
    window_names: Optional[Dict[int, str]] = None,
) -> Dict[str, curses.window]:
    if window_names:
        error_check_for_name_duplication(window_names)
    elif window_names is None:
        window_names = {}

    error_check_for_equal_array_lengths(window_layout)
    error_check_for_correct_window_formatting(window_layout)

    maxy, maxx = win.getmaxyx()
    grid_x = len(window_layout[0])
    grid_y = len(window_layout)
    grid_cell_size = (maxy // grid_y), (maxx // grid_x)
    value_coordinates = {}
    square_dimensions = {}
    windows = {}

    # Find the top left and bottom right points of each window on the grid
    # Itterates through the grid and stores the first point of a window
    # store the last point of the window
    # this is to calculate the shift between the points and structure a rectangle
    for y in range(len(window_layout)):
        for x in range(len(window_layout[y])):
            value = window_layout[y][x]
            if value not in value_coordinates:
                value_coordinates[value] = [(y, x), (y + 1, x + 1)]
            else:
                value_coordinates[value][1] = (y + 1, x + 1)

    # Calculate the shift between the first and last point of each rectangle and
    # store these values and the length and width of each window
    for key, value in value_coordinates.items():
        square_dimensions[key] = [value[1][0] - value[0][0], value[1][1] - value[0][1]]

    # Calculate the length and width of each grid cells in terminal cells
    # Define each window by the length and with of grid cells
    # Find the starting point to draw the windows
    for key in value_coordinates:
        val_coor = value_coordinates[key]
        sq_dim = square_dimensions[key]

        window_starting_location = (
            grid_cell_size[0] * val_coor[0][0],
            grid_cell_size[1] * val_coor[0][1],
        )

        window_height = grid_cell_size[0] * sq_dim[0]
        window_width = grid_cell_size[1] * sq_dim[1]

        new_window = curses.newwin(
            window_height,
            window_width,
            window_starting_location[0],
            window_starting_location[1],
        )
        new_window.box()
        title = f" {window_names[key]} "
        new_window.addstr(0, 1, title)
        windows[window_names[key]] = new_window

    return windows


# Configuration-----------------------------------------------------------------
screen = curses.initscr()
grid_layout = [
    [1, 2, 2],
    [1, 2, 2],
    [1, 2, 2],
    [3, 3, 3],
]

window_names = {
    1: "main",
    2: "side",
    3: "footer",
    4: "something",
}


# Main init---------------------------------------------------------------------
def main(screen):
    screen.clear()

    windows = grid(screen, grid_layout, window_names)

    for win in windows.values():
        win.refresh()

    # windows["side"].addstr(1, 1, "testing")
    # windows["side"].refresh()

    screen.getch()
    # curses.endwin()


wrapper(main)
