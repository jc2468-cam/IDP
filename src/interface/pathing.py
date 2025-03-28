def reverse_turns_strip(path):
    """Inverts the turn instructions in a path, and removes all other instructions.#

    This allows the path from `B` to `A` to be constructed from the path from `A` to `B`, but non-turn instructions must be added manually
    (since they are not always symmetrical).

    Arguments:
        `path` (`list`): The instruction set to reverse.

    Returns:
        `list`: The turn instructions to path from the destination back to the origin.
    """
    started = False
    start_i, end_i = 0, 0
    for i in range(len(path)):
        if started:
            if path[i][0][0] != "t":
                end_i = i
        elif path[i][0][0] == "t":
            start_i = i
            started = True
    turns = [[(a[0][0], -a[0][1])] for a in path[start_i:end_i][::-1]]
    return turns


# forward and reverse times
front_house_times = [1.8, 3.5]
back_house_times = [2.5, 3.0]
factory_times = [2.5, 3.0]
warehouse_times = [2.0, 2.5]

end_time = 2


test_path = [[("p", 2.3)], [("p", 2.3)], [("p", 2.3)], [("p", 2.3)], [("p", 2.3)], [("p", 2.3)], [("p", 2.3)]]

# start
start_front_house_path = [[("t", 0)], [("t", 1)], [("t", -1), ("l", 0.5), ("a", 0), ("s", front_house_times[0])], [("p", 2.3)]]

# [0] drop red, [1] drop blue
front_house_drop_path = [[[("t", -1), ("h", 0.7)], [("t", 1)], [("d", 1.5)]], [[("t", 1)], [("t", 0), ("h", 1.0)], [("t", -1)], [("d", 1.5)]]]
back_house_drop_path = [[[("t", 1)], [("t", 0), ("h", 1.5)], [("t", 1)], [("t", 0)], [("d", 1.5)]], [[("t", -1), ("h", 0.7)], [("t", -1)], [("t", 0)], [("d", 1.5)]]]
factory_drop_path = [[[("t", -1)], [("t", -1), ("h", 0.5)], [("t", 1)], [("t", 0)], [("d", 1.5)]], [[("t", -1), ("h", 0.7)], [("t", 1)], [("t", 0), ("h", 0.7)], [("t", -1)], [("t", 0)], [("d", 1.5)]]]
warehouse_drop_path = [[[("t", 1)], [("t", 0), ("h", 1.5)], [("t", 1)], [("t", 0)], [("t", 0)], [("d", 1.5)]], [[("t", -1), ("h", 0.7)], [("t", -1)], [("t", 0)], [("t", 0)], [("d", 1.5)]]]
red_drop_blue_drop_path = [[("t", -1)], [("t", 0)], [("t", 0)], [("t", -1)], [("d", 1.5)]]
blue_drop_red_drop_path = [[("t", 1)], [("t", 0)], [("t", 0)], [("t", 1)], [("d", 1.5)]]

# return drop paths
red_drop_front_house_path = reverse_turns_strip(front_house_drop_path[0]) + [[("p", front_house_times[1])]]
red_drop_front_house_path[-2] += [("l", 0.5), ("a", 0), ("s", front_house_times[0])]
red_drop_back_house_path = reverse_turns_strip(back_house_drop_path[0]) + [[("p", back_house_times[1])]]
red_drop_back_house_path[-2] += [("l", 0.5), ("a", 0), ("s", back_house_times[0])]
red_drop_factory_path = reverse_turns_strip(factory_drop_path[0]) + [[("p", factory_times[1])]]
red_drop_factory_path[-2] += [("l", 0.5), ("a", 0), ("s", factory_times[0])]
red_drop_warehouse_path = reverse_turns_strip(warehouse_drop_path[0]) + [[("p", warehouse_times[1])]]
red_drop_warehouse_path[-2] += [("l", 0.5), ("a", 0), ("s", warehouse_times[0])]
red_drop_start_path = [[("t", -1)], [("t", 0)], [("t", -1)], [("l", end_time)]]


blue_drop_front_house_path = reverse_turns_strip(front_house_drop_path[1]) + [[("p", front_house_times[1])]]
blue_drop_front_house_path[-2] += [("l", 0.5), ("a", 0), ("s", front_house_times[0])]
blue_drop_back_house_path = reverse_turns_strip(back_house_drop_path[1]) + [[("p", back_house_times[1])]]
blue_drop_back_house_path[-2] += [("l", 0.5), ("a", 0), ("s", back_house_times[0])]
blue_drop_factory_path = reverse_turns_strip(factory_drop_path[1]) + [[("p", factory_times[1])]]
blue_drop_factory_path[-2] += [("l", 0.5), ("a", 0), ("s", factory_times[0])]
blue_drop_warehouse_path = reverse_turns_strip(warehouse_drop_path[1]) + [[("p", warehouse_times[1])]]
blue_drop_warehouse_path[-2] += [("l", 0.5), ("a", 0), ("s", warehouse_times[0])]
blue_drop_start_path = [[("t", 1)], [("t", 1)], [("l", end_time)]]


# between
front_house_back_house_path = [[("t", -1)], [("t", -1)], [("t", -1)], [("t", 0)], [("t", 1), ("l", 0.5), ("a", 0), ("s", back_house_times[0])], [("p", back_house_times[1])]]
front_house_factory_path = [[("t", -1), ("h", 1.5)], [("t", -1)], [("t", -1)], [("t", 1)], [("t", 1), ("l", 0.5), ("a", 0), ("s", factory_times[0])], [("p", factory_times[1])]]
front_house_warehouse_path = [[("t", -1)], [("t", -1)], [("t", 0)], [("t", -1)], [("t", 0)], [("t", -1), ("l", 0.5), ("a", 0), ("s", warehouse_times[0])], [("p", warehouse_times[1])]]

back_house_front_house_path = reverse_turns_strip(front_house_back_house_path) + [[("p", front_house_times[1])]]
back_house_front_house_path[-2] += [("l", 0.5), ("a", 0), ("s", front_house_times[0])]
back_house_factory_path = [[("t", 1)], [("t", -1)], [("t", 1), ("l", 0.5), ("a", 0), ("s", factory_times[0])], [("p", factory_times[1])]]
back_house_warehouse_path = [[("t", 1)], [("t", -1), ("h", 0.5)], [("t", 0)], [("t", -1)], [("t", -1), ("l", 0.5), ("a", 0), ("s", factory_times[0])], [("p", warehouse_times[1])]]

factory_front_house_path = reverse_turns_strip(front_house_factory_path) + [[("p", front_house_times[1])]]
factory_front_house_path[-2] += [("l", 0.5), ("a", 0), ("s", front_house_times[0])]
factory_back_house_path = reverse_turns_strip(back_house_factory_path) + [[("p", back_house_times[1])]]
factory_back_house_path[-2] += [("l", 0.5), ("a", 0), ("s", back_house_times[0])]
factory_warehouse_path = [[("t", 1)], [("t", -1)], [("t", -1), ("l", 0.5), ("a", 0), ("s", warehouse_times[0])], [("p", warehouse_times[1])]]

warehouse_front_house_path = reverse_turns_strip(front_house_warehouse_path) + [[("p", front_house_times[1])]]
warehouse_front_house_path[-2] += [("l", 0.5), ("a", 0), ("s", front_house_times[0])]
warehouse_back_house_path = reverse_turns_strip(back_house_warehouse_path) + [[("p", back_house_times[1])]]
warehouse_back_house_path[-2] += [("l", 0.5), ("a", 0), ("s", back_house_times[0])]
warehouse_factory_path = reverse_turns_strip(factory_warehouse_path) + [[("p", factory_times[1])]]
warehouse_factory_path[-2] += [("l", 0.5), ("a", 0), ("s", factory_times[0])]


def get_path(location, next_location):
    """Gets the instruction set to get from `location` to `next_location`, and perform the relevant action upon arriving (e.g. pick up / drop off block(s)).

    Arguments:
        `location` (`str`): The current location (to path from).
        `next_locaction`: The desired destination (to path to).

    Returns:
        `list`: Instructions to execute at each junction to get between locations and perform relevant actions.
    """
    if location == "start":
        return start_front_house_path

    if location == "front_house":
        if next_location == "back_house":
            return front_house_back_house_path
        elif next_location == "factory":
            return front_house_factory_path
        elif next_location == "warehouse":
            return front_house_warehouse_path
        elif next_location == "red_drop":
            return front_house_drop_path[0]
        elif next_location == "blue_drop":
            return front_house_drop_path[1]

    elif location == "back_house":
        if next_location == "front_house":
            return back_house_factory_path
        elif next_location == "factory":
            return back_house_factory_path
        elif next_location == "warehouse":
            return back_house_warehouse_path
        elif next_location == "red_drop":
            return back_house_drop_path[0]
        elif next_location == "blue_drop":
            return back_house_drop_path[1]

    elif location == "factory":
        if next_location == "front_house":
            return factory_front_house_path
        elif next_location == "back_house":
            return factory_back_house_path
        elif next_location == "warehouse":
            return factory_warehouse_path
        elif next_location == "red_drop":
            return factory_drop_path[0]
        elif next_location == "blue_drop":
            return factory_drop_path[1]

    elif location == "warehouse":
        if next_location == "front_house":
            return warehouse_front_house_path
        elif next_location == "back_house":
            return warehouse_back_house_path
        elif next_location == "factory":
            return warehouse_factory_path
        elif next_location == "red_drop":
            return warehouse_drop_path[0]
        elif next_location == "blue_drop":
            return warehouse_drop_path[1]

    elif location == "red_drop":
        if next_location == "front_house":
            return red_drop_front_house_path
        elif next_location == "back_house":
            return red_drop_back_house_path
        elif next_location == "factory":
            return red_drop_factory_path
        elif next_location == "warehouse":
            return red_drop_warehouse_path
        elif next_location == "blue_drop":
            return red_drop_blue_drop_path
        elif next_location == "start":
            return red_drop_start_path

    elif location == "blue_drop":
        if next_location == "front_house":
            return blue_drop_factory_path
        elif next_location == "back_house":
            return blue_drop_factory_path
        elif next_location == "factory":
            return blue_drop_factory_path
        elif next_location == "warehouse":
            return blue_drop_warehouse_path
        elif next_location == "red_drop":
            return blue_drop_red_drop_path
        elif next_location == "start":
            return blue_drop_start_path
