from serial.tools import list_ports
from pydobot import Dobot
import pytest


class TestPose:

    def test_one(self):
        port = list_ports.comports()[0].device
        device = Dobot(port=port, verbose=True)
        device.move_to(202.0, 0.0, -0.0, 0.0, True)
        print("\nMoved")

        (x, y, z, r, j1, j2, j3, j4) = device.pose()
        print(f'\nx:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
        device.close()
