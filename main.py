import tello
from tello_control_ui import TelloUI


def main():

    drone = tello.Tello(local_ip=192.168.10.1, 8889)
    vplayer = TelloUI(drone, "./img/")

    # start the Tkinter mainloop
    vplayer.root.mainloop()

if __name__ == "__main__":
    main()
