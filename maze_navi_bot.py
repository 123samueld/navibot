from robot_control_class import RobotControl

rc = RobotControl()

class maze_navigator:
    def __init__(self):
        pass
    

    def surrounding_check(self):
        left_quadrant = 0
        right_quadrant = 0
        sweep_left = 0
        sweep_right = 0
        
        while sweep_left < 6:
            rc.rotate(-10)
            result = rc.get_front_laser()
            left_quadrant = left_quadrant + result
            sweep_left = sweep_left + 1

        left_quadrant_mean = left_quadrant / 6
        rc.rotate(60)

        while sweep_right < 6:
            rc.rotate(10)
            result = rc.get_front_laser()
            right_quadrant = right_quadrant + result
            sweep_right = sweep_right + 1

        right_quadrant_mean = right_quadrant / 6
        rc.rotate(-60)

        if right_quadrant_mean > left_quadrant_mean:
            self.full_scan_right()
        else:
            self.full_scan_left()

    def full_scan_right(self):
        rc.rotate(90)
        full_laser_scan = rc.get_laser_full()
        iter_counter = 0
        max_range = 0
        for iteration in range(len(full_laser_scan)):
            current_scan_point = full_laser_scan[iter_counter]
            if current_scan_point > max_range:
                max_range = current_scan_point
                max_counter = iter_counter
            iter_counter = iter_counter + 1
        print(max_range)
        print(max_counter)
        rc.rotate(-90)
        new_vector = max_counter/2
        rc.rotate(new_vector)
        rc.move_straight_time("forward", 0.2, 1)
    
    def full_scan_left(self):
        rc.rotate(-90)
    
    def cautious_forward_move(self):
        sensor_front_feed = rc.get_front_laser()
        while sensor_front_feed > 1:
            rc.move_straight_time("forward", 0.1, 0.1)
            rc.move_straight_time("forward", 0.2, 0.2)
            rc.move_straight_time("forward", 0.3, 0.4)
            rc.move_straight_time("forward", 0.2, 0.2)
            rc.move_straight_time("forward", 0.1, 0.1)
            sensor_front_feed = rc.get_front_laser()
            print(sensor_front_feed)
        rc.stop_robot()
        self.surrounding_check()

            

    

nav1 = maze_navigator()
nav1.cautious_forward_move()