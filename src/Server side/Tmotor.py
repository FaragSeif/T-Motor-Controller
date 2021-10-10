from abc import ABC
from dataclasses import dataclass
from CANSocket import CANSocket
import builtins


class FloatInt:
    def __init__(self, int_value, range_min, range_max, int_bits):
        self.int_value = int_value
        self.range_min = range_min
        self.range_max = range_max
        self.int_bits = int_bits
        self.float_value = self.toFloat()

    def set_by_float(self, float_value):
        self.float_value = float_value
        self.clamp()
        self.int_value = self.toUInt()

    def set_by_int(self, int_value):
        self.int_value = int_value
        self.float_value = self.toFloat()
        self.clamp()

    def toUInt(self):
        span = self.range_max - self.range_min
        return int(
            (self.float_value - self.range_min)
            * (float((1 << self.int_bits) - 1))
            / span
        )

    def toFloat(self):
        span = self.range_max - self.range_min
        return (
            float(self.int_value) * span / float((1 << self.int_bits) - 1)
            + self.range_min
        )

    def clamp(self):
        # TODO: check if ints should be clamped or not
        return builtins.max(
            self.range_min, builtins.min(self.range_max, self.float_value)
        )


class MotorState:
    _position: FloatInt(0, -95.5, 95.5, 16)
    _velocity: FloatInt(0, -30.0, 30.0, 12)
    _torque = FloatInt(0, -18.0, 18.0, 12)

    def __init__(self, position: float, velocity: float, torque: float) -> None:
        self.set_motor_state_values_by_floats(position, velocity, torque)

    def set_motor_state_values_by_floats(
        self, position: float, velocity: float, torque: float
    ):
        self._position.set_by_float(position)
        self._velocity.set_by_float(velocity)
        self._torque.set_by_float(torque)

    def set_motor_state_values_by_ints(self, position: int, velocity: int, torque: int):
        self._position.set_by_int(position)
        self._velocity.set_by_int(velocity)
        self._torque.set_by_int(torque)


@dataclass
class ControllerState:

    _kp = FloatInt(0, 0.0, 500.0, 12)
    _kd = FloatInt(0, 0.0, 5.0, 12)

    def __init__(self, kp: float, kd: float) -> None:
        self.set_controller_state_values_by_floats(kp, kd)

    def set_controller_state_values_by_floats(self, kp: float, kd: float):
        self._kp.set_by_float(kp)
        self._kd.set_by_float(kd)

    def set_controller_state_values_by_ints(self, kp: int, kd: int):
        self._kp.set_by_int(kp)
        self._kd.set_by_int(kd)


class Frame:
    def __init__(self, state: MotorState, min_state: MotorState):
        self.state = state


class TMotor(ABC):
    pass


class MotorDataUtility:
    pass


class TMotorQDD(TMotor):
    # TODO:
    # add tx_message dict
    # add rx_message dict
    def __init__(self, can_socket: CANSocket, device_id=0x001, rxtx_interface=None):

        # TODO: pass dict with reciver/transmitter functions from the specific bus
        if not isinstance(can_socket, CANSocket):
            raise TypeError("can_socket is not an instance of CANSocket")

        self.can_bus = can_socket
        self.data_utility = MotorDataUtility()

        # TODO: Implement motoring name addressing
        self.name = None

        self.motor_state = MotorState(0, 0, 0)
        self.controller_state = ControllerState(0, 0)

        self.zero_state_motor = MotorState(0, 0, 0)
        self.zero_state_controller = ControllerState(0, 0)

        zero_state_bytes = self.state_to_bytes(
            self.zero_state_motor, self.zero_state_controller
        )
        self.device_id = device_id

        self.COMMANDS = {
            "mot_mode_on": bytes([255, 255, 255, 255, 255, 255, 255, 252]),
            "mot_mode_off": bytes([255, 255, 255, 255, 255, 255, 255, 253]),
            "set_zero": bytes([255, 255, 255, 255, 255, 255, 255, 254]),
            "empty": bytes([0, 0, 0, 0, 0, 0, 0, 0]),
            "zero_state": zero_state_bytes,
        }
        self.torque_limit = 1

    def __del__(self):
        print("Motor object was destructed")

    def state_to_bytes(
        self, motor_state: MotorState, controller_state: ControllerState
    ):
        state_bytes = [
            motor_state._position.toUInt >> 8,
            motor_state._position.toUInt & 0xFF,
            motor_state._velocity.toUInt >> 4,
            ((motor_state._velocity.toUInt & 0xF) << 4)
            | (controller_state._kp.toUInt >> 8),
            controller_state._kp.toUInt & 0xFF,
            controller_state._kd.toUInt >> 4,
            ((controller_state._kp.toUInt & 0xF) << 4)
            | (motor_state._torque.toUInt >> 8),
            motor_state._torque.toUInt & 0xFF,
        ]

        return bytearray(state_bytes)

    def bytes_to_state(self, recived_bytes, motor_state: MotorState):
        if recived_bytes:
            position = (recived_bytes[1] << 8) | recived_bytes[2]
            velocity = (recived_bytes[3] << 4) | (recived_bytes[4] >> 4)
            torque = ((recived_bytes[4] & 0xF) << 8) | recived_bytes[5]

            motor_state.set_motor_state_values_by_ints(position, velocity, torque)
        else:
            pass

    def send_command(self, command):
        self.can_bus.send_bytes(self.device_id, command)

    def recive_reply(self):
        _, _, self.reply = self.can_bus.recive_frame()
        return self.reply

    def enable(self):
        self.send_command(self.COMMANDS["mot_mode_on"])
        print("Motor mode enabled")

    def disable(self):
        self.send_command(self.COMMANDS["mot_mode_off"])
        print("Motor mode disabled")

    def set_zero(self):
        print(
            f'You are going to assign a new zero for motor with ID {self.device_id}, press "Y" to continue...\n'
        )
        user_input = input()
        if user_input == "Y" or user_input == "y":
            self.send_command(self.COMMANDS["set_zero"])
            print("New encoder zero is setted")
        else:
            print("Canceling...")

    def set_torque(self, torque):
        if torque > self.torque_limit:
            torque = self.torque_limit
        if torque < -self.torque_limit:
            torque = -self.torque_limit

        state_data_dict = MotorState(0, 0, torque)
        self.send_command(
            self.state_to_bytes(state_data_dict, self.zero_state_controller)
        )
        self.recive_reply()
        self.bytes_to_state(self.reply, self.motor_state)

    def set_torque_limit(self, torque_limit):
        self.torque_limit = torque_limit
        print(f"Torque limit is set to: {torque_limit}")

    def set_state(self, state_data_dict):
        self.send_command(state_data_dict)
        self.recive_reply()
        self.bytes_to_state(self.reply, self.motor_state)
