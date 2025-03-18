def reverse_turns_strip(path):
    started = False
    start_i, end_i = 0, 0
    for i in range(len(path)):
        if started:
            if path[i][0][0] != "t":
                end_i = i
        elif path[i][0][0] == "t":
            start_i = i
            started = True
    turns = [[(a[0][0], -a[0][-1])] for a in path[start_i:end_i][::-1]]
    return turns


front_house_time = 1.7
back_house_time = 1.5
factory_time = 1.7
warehouse_time = 1.5

end_time = 2


test_path = [[("p", 0)], [("p", 0)], [("p", 0)], [("p", 0)], [("p", 0)], [("p", 0)], [("p", 0)]]

# start
start_front_house_path = [[("t", 0)], [("t", 1)], [("t", -1), ("l", 0), ("a", 0), ("s", front_house_time)], [("p", 0)]]

# [0] drop red, [1] drop blue
back_house_drop_path = [[[("t", -1)], [("t", -1)], [("t", -1)], [("t", 0)], [("t", 0)], [("t", 1)], [("d", 0)]], [[("t", -1)], [("t", -1)], [("t", 0)], [("d", 0)]]]
front_house_drop_path = [[[("t", -1)], [("t", 1)], [("d", 0)]], [[("t", 1)], [("t", 0)], [("t", -1)], [("d", 0)]]]
warehouse_drop_path = [[[("t", 1)], [("t", 0)], [("t", 1)], [("t", 0)], [("t", 0)], [("d", 0)]], [[("t", -1)], [("t", -1)], [("t", 0)], [("t", 0)], [("d", 0)]]]
factory_drop_path = [[[("t", -1)], [("t", -1)], [("t", 1)], [("t", 0)], [("d", 0)]], [[("t", -1)], [("t", 1)], [("t", 0)], [("t", -1)], [("t", 0)], [("d", 0)]]]
red_drop_blue_drop_path = [[("t", -1)], [("t", 0)], [("t", 0)], [("t", -1)], [("d", 0)]]
blue_drop_red_drop_path = [[("t", 1)], [("t", 0)], [("t", 0)], [("t", 1)], [("d", 0)]]

# return drop paths
red_drop_front_house_path = reverse_turns_strip(front_house_drop_path[0]) + [[("p", 0)]]
red_drop_front_house_path[-2] += [("l", 0), ("a", 0), ("s", front_house_time)]
red_drop_back_house_path = reverse_turns_strip(back_house_drop_path[0]) + [[("p", 0)]]
red_drop_back_house_path[-2] += [("l", 0), ("a", 0), ("s", back_house_time)]
red_drop_factory_path = reverse_turns_strip(factory_drop_path[0]) + [[("p", 0)]]
red_drop_factory_path[-2] += [("l", 0), ("a", 0), ("s", factory_time)]
red_drop_warehouse_path = reverse_turns_strip(warehouse_drop_path[0]) + [[("p", 0)]]
red_drop_warehouse_path[-2] += [("l", 0), ("a", 0), ("s", warehouse_time)]
red_drop_start_path = [[("t", -1)], [("t", 0)], [("t", -1)], [("l", end_time)]]


blue_drop_front_house_path = reverse_turns_strip(front_house_drop_path[1]) + [[("p", 0)]]
blue_drop_front_house_path[-2] += [("l", 0), ("a", 0), ("s", front_house_time)]
blue_drop_back_house_path = reverse_turns_strip(back_house_drop_path[1]) + [[("p", 0)]]
blue_drop_back_house_path[-2] += [("l", 0), ("a", 0), ("s", back_house_time)]
blue_drop_factory_path = reverse_turns_strip(factory_drop_path[1]) + [[("p", 0)]]
blue_drop_factory_path[-2] += [("l", 0), ("a", 0), ("s", factory_time)]
blue_drop_warehouse_path = reverse_turns_strip(warehouse_drop_path[1]) + [[("p", 0)]]
blue_drop_warehouse_path[-2] += [("l", 0), ("a", 0), ("s", warehouse_time)]
blue_drop_start_path = [[("t", 1)], [("t", 1)], [("l", end_time)]]


# between
front_house_back_house_path = [[("t", -1)], [("t", -1)], [("t", -1)], [("t", 0)], [("t", 1), ("l", 0), ("a", 0), ("s", back_house_time)], [("p", 0)]]
front_house_factory_path = [[("t", -1)], [("t", -1)], [("t", -1)], [("t", 1)], [("t", 1), ("l", 0), ("a", 0), ("s", factory_time)], [("p", 0)]]
front_house_warehouse_path = [[("t", -1)], [("t", -1)], [("t", 0)], [("t", -1)], [("t", 0)], [("t", -1), ("l", 0), ("a", 0), ("s", warehouse_time)], [("p", 0)]]

back_house_front_house_path = reverse_turns_strip(front_house_back_house_path) + [[("p", 0)]]
back_house_front_house_path[-2] += [("l", 0), ("a", 0), ("s", front_house_time)]
back_house_factory_path = [[("t", 1)], [("t", -1)], [("t", 1), ("l", 0), ("a", 0), ("s", factory_time)], [("p", 0)]]
back_house_warehouse_path = [[("t", 1)], [("t", -1)], [("t", 0)], [("t", -1)], [("t", -1), ("l", 0), ("a", 0), ("s", factory_time)], [("p", 0)]]

factory_front_house_path = reverse_turns_strip(front_house_factory_path) + [[("p", 0)]]
factory_front_house_path[-2] += [("l", 0), ("a", 0), ("s", front_house_time)]
factory_back_house_path = reverse_turns_strip(back_house_factory_path) + [[("p", 0)]]
factory_back_house_path[-2] += [("l", 0), ("a", 0), ("s", back_house_time)]
factory_warehouse_path = [[("t", 1)], [("t", -1)], [("t", -1), ("l", 0), ("a", 0), ("s", warehouse_time)], [("p", 0)]]

warehouse_front_house_path = reverse_turns_strip(front_house_warehouse_path) + [[("p", 0)]]
warehouse_front_house_path[-2] += [("l", 0), ("a", 0), ("s", front_house_time)]
warehouse_back_house_path = reverse_turns_strip(back_house_warehouse_path) + [[("p", 0)]]
warehouse_back_house_path[-2] += [("l", 0), ("a", 0), ("s", back_house_time)]
warehouse_factory_path = reverse_turns_strip(factory_warehouse_path) + [[("p", 0)]]
warehouse_factory_path[-2] += [("l", 0), ("a", 0), ("s", factory_time)]


def get_path(location, next_location):
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
