from serial.tools import list_ports
from pydobot import Dobot
from unittest.mock import Mock

import pytest

USE_MOCKS = True


class TestPose:
    arm = None
    x_pos = None
    y_pos = None
    z_pos = None
    r_pos = None
    j1_pos = None
    j2_pos = None
    j3_pos = None
    j4_pos = None
    wait_mock = False

    @classmethod
    def mock_move_to(cls, x, y, z, r, wait=False):
        print("Inside mock_move_to")
        cls.x_pos = x
        cls.y_pos = y
        cls.z_pos = z
        cls.r_pos = r
        cls.j1_pos = 0
        cls.j2_pos = 0
        cls.j3_pos = 0
        cls.j4_pos = 0
        cls.wait_mock = wait

    @classmethod
    def get_mock_arm_position(cls):
        print("Inside get_mock_arm_position")
        return cls.x_pos, cls.y_pos, cls.z_pos, cls.r_pos, cls.j1_pos, cls.j2_pos, cls.j3_pos, cls.j4_pos

    @classmethod
    def setup_class(cls):
        if USE_MOCKS:
            cls.arm = Mock()
            cls.arm.move_to.side_effect = cls.mock_move_to
            cls.arm.pose.side_effect = cls.get_mock_arm_position
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
