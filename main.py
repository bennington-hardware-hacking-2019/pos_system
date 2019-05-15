# -*- coding: utf-8 -*-

from controller import Controller


if __name__== "__main__":
    controller = Controller()
    controller.setup()

    if controller.run() == False:
        print("error")
    else:
        print("success")
