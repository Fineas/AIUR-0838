import time 
import logging
import urx
import sys


class UR3_Robot:

    gr_0 = 0
    gr_1 = 0.017453 # radians
    gr_15 = gr_1 * 15
    gr_30 = gr_15 * 2
    gr_60 = gr_30 * 2
    gr_90 = gr_30 * 3 
    gr_180 = gr_90 * 2
    gr_360 = gr_180 * 2
    socket = 0

    def __init__(self):
        self.rob = urx.Robot("192.168.1.190")
        self.rob.set_tcp((0, 0, 0.1, 0, 0, 0))
        self.rob.set_payload(2, (0, 0, 0.1))
        self.socket = self.rob.secmon._s_secondary
        print(self.socket)

        time.sleep(0.2)  #leave some time to poop
        
        print("Initializing robot, moving to default position...")
        self.move_default()

        #1 = +back/-front, 2 = +right/-left, 3 = +up/-down
        # self.rob.movel((0,0,-0.01,0,0,0), relative=True)

        print("Done initialization")

        # Variables which keep track of the limits
        self.up_down = 0            # Should be between [16 and -25]
        self.front_back = 0         # Should be between [17 and -20]
        self.left_right = 0         # Should be between [22 and -47]

    def move_joints(self, j1, j2, j3, j4, j5, j6, a= '1.39', v='1.25'):
        self.rob.movej((j1, j2, j3, j4, j5, j6), a, v)
        time.sleep(2)

    def move_linear(self, x, y, z, rx, ry, rz, a= '1.39', v='.25'):
        self.rob.movel((x, y, z, rx, ry, rz), a, v, relative=True)
        time.sleep(0.5)

    def move_right(self):
        if self.left_right - 1 >= -16:
            self.move_linear(0,0.01,0,0,0,0)
            self.left_right -= 1
        else:
            print("Reached right-limit")

    def move_left(self):
        if self.left_right + 1 <= 20:
            self.move_linear(0,-0.01,0,0,0,0)
            self.left_right += 1
        else:
            print("Reached left-limit")

    def move_up(self):
        if self.up_down + 1 <= 16:
            self.move_linear(0,0,0.01,0,0,0)
            self.up_down += 1
            print(self.up_down)
        else:
            print("Reached up-limit")

    def move_down(self):
        if self.up_down - 1 >= -25:
            self.move_linear(0,0,-0.01,0,0,0)
            self.up_down -= 1
        else:
            print("Reached down-limit")

    def move_front(self):
        if self.front_back + 1 <= 16:
            self.move_linear(-0.01,0,0,0,0,0)
            self.front_back += 1
        else:
            print("Reached front limit")

    def move_back(self):
        if self.front_back - 1 >= -16:
            self.move_linear(0.01,0,0,0,0,0)
            self.front_back -= 1
        else:
            print("Reached back limit")

    def move_default(self):
        self.move_joints(0.0,-1.5708,1.5708,0.0,1.5708,0.0)

    def spin_left(self):
        pose2 = self.rob.getj()
        pose2[0] += self.gr_15
        self.move_joints(pose2[0], pose2[1], pose2[2], pose2[3], pose2[4], pose2[5])
        #self.update_tcp()

    def spin_right(self):
        pose2 = self.rob.getj()
        pose2[0] -= self.gr_15
        self.move_joints(pose2[0], pose2[1], pose2[2], pose2[3], pose2[4], pose2[5])
        #self.update_tcp()

    def update_tcp(self):
        self.rob.set_tcp((0, 0, 0.1, 0, 0, 0))

    def open_grip(self):
        pass
        time.sleep(3)

    def close_grip(self):
        pass
        time.sleep(3)

    def move_direction(self, direction):
        d = {'r' : self.move_right, 'l' : self.move_left, 'u' : self.move_up, 'd' : self.move_down, 'f' : self.move_front,
             'b' : self.move_back, 'def' : self.move_default, 'sl' : self.spin_left, 'sr' : self.spin_right, 'o' : self.open_grip,
             'c' : self.close_grip}

        d[direction]()

    def terminate(self):
        self.rob.close()

    def open_grip(self):
        print("Opening gripper")
        
        file_name = "grip_open.script"
        f = open (file_name, "rb")   #Robotiq Gripper
        l = f.read(1024)
        while (l):
            print ('AAA')
            self.socket.send(l)
            l = f.read(1024)
        print("Finished uploading script")
        time.sleep(5)

    def close_grip(self):
        print("Closing gripper")
        
        file_name = "grip_close.script"
        f = open (file_name, "rb")   #Robotiq Gripper
        l = f.read(1024)
        while (l):
            self.socket.send(l)
            l = f.read(1024)
        print("Finished uploading script")
        time.sleep(5)

    def interactive(self):
        while True:
            user_input = input('Enter command > ')
            
            if user_input == "exit":
                break

            robot.move_direction(user_input.strip())

if __name__ == "__main__":  
    try:
        robot = UR3_Robot()

        # for i in range(20):
        #     robot.move_direction('l')

        # for i in range(17):
        #     robot.move_direction('d')

        # robot.move_direction('c')

        # for i in range(17):
        #     robot.move_direction('u')

        # for i in range(20):
        #     robot.move_direction('r')

        # for i in range(16):
        #     robot.move_direction('f')

        # robot.move_direction('o')

        robot.interactive()
        robot.terminate()
        print("COX TONY MONTANA JOS")

        sys.exit(0)
    except:
        robot.terminate()
        sys.exit(1)