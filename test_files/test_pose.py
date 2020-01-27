from serial.tools import list_ports
from pydobot import Dobot
from unittest.mock import Mock

import pytest

USE_MOCKS = True


class Dobot_Mock:
    def __init__(self):
        self.x_pos = None
        self.y_pos = None
        self.z_pos = None
        self.r_pos = None
        self.j1_pos = None
        self.j2_pos = None
        self.j3_pos = None
        self.j4_pos = None
        self.wait_mock = False

        self.arm = Mock()
        self.arm.move_to.side_effect = self.mock_move_to
        self.arm.pose.side_effect = self.get_mock_arm_position

    def mock_move_to(self, x, y, z, r, wait=False):
        print("Inside mock_move_to")
        self.x_pos = x
        self.y_pos = y
        self.z_pos = z
        self.r_pos = r
        self.j1_pos = 0
        self.j2_pos = 0
        self.j3_pos = 0
        self.j4_pos = 0
        self.wait_mock = wait

    def get_mock_arm_position(self):
        print("Inside get_mock_arm_position")
        return self.x_pos, self.y_pos, self.z_pos, self.r_pos, self.j1_pos, self.j2_pos, self.j3_pos, self.j4_pos

    def get_arm(self):
        return self.arm


class TestPose:
    arm = None

    @classmethod
    def setup_class(cls):
        if USE_MOCKS:
            cls.arm = Dobot_Mock().get_arm()
        else:
            try:
                port = list_ports.comports()[0].device
                cls.arm = Dobot(port=port, verbose=True)
            except Exception as e:
                print(f"Exception raised: {str(e)}")
                assert False
            finally:
                if cls.arm:
                    cls.arm.close()

    def test_one(self):
        try:
            TestPose.arm.move_to(202.0, 0.0, 0.0, 0.0, True)
            print("\nMoved arm in test")

            (x, y, z, r, j1, j2, j3, j4) = TestPose.arm.pose()
            assert pytest.approx(x) == 202.0
            print(f'\nx:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
        except Exception as e:
            print(f"Exception raised: {str(e)}")
            assert False
        finally:
            if TestPose.arm:
                TestPose.arm.close()
