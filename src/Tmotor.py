from abc import ABC
from dataclasses import dataclass
from CANSocket import CANSocket
import builtins


def clamp(value: float, min: float, max: float):
    return builtins.max(min, builtins.min(max, value))

def float_to_uint( data_float: float, data_min: float, data_max: float, bits: int
    ) -> int:
        span = data_max - data_min
        return int((data_float - data_min) * (float((1 << bits) - 1)) / span)

def uint_to_float( data_int: int, data_min: int, data_max: int, bits: int
    ) -> float:
        span = data_max - data_min
        return float(data_int) * span / float((1 << bits) - 1) + data_min


# @dataclass
class MotorState:
    """Represents the current state of the motor."""

    MIN_POSITION = -95.5
    MAX_POSITION = -95.5
    POSITION_BITS = 16
    _position: float = 0
    _position_uint: int = 0
    MIN_VELOCITY = -30.0
    MAX_VELOCITY = 30.0
    VELOCITY_BITS = 12
    _velocity: float = 0
    _velocity_uint: int = 0
    MIN_TORQUE = -18.0
    MAX_TORQUE = 18.0
    TORQUE_BITS = 12
    _torque: float = 0
    _torque_uint: int = 0

    def __init__(self, position: float, velocity: float, torque: float) -> None:
        set_values(position, velocity, torque)

    def set_values(self, position: float, velocity: float, torque: float):
        """Sets the current state of the motor."""
        self._position = clamp(position, MotorState.MIN_POSITION, MotorState.MAX_POSITION)
        self._position_uint = float_to_uint(self._position, self.MIN_POSITION, self.MAX_POSITION, self.POSITION_BITS)

        self._velocity = clamp(velocity, MotorState.MIN_VELOCITY, MotorState.MAX_VELOCITY)
        self._velocity_uint = float_to_uint(self._velocity, self.MIN_VELOCITY, self.MAX_VELOCITY, self.VELOCITY_BITS)

        self._torque = clamp(torque, MotorState.MIN_TORQUE, MotorState.MAX_TORQUE)
        self._torque_uint = float_to_uint(self._torque, self.MIN_TORQUE, self.MAX_TORQUE, self.TORQUE_BITS)

    def set_unit_values(self, position: int, velocity: int, torque: int):
        """Sets the current state of the motor from unsigned int."""
        self._position_uint = position
        self._position = uint_to_float(self._position_uint, self.MIN_POSITION, self.MAX_POSITION, self.POSITION_BITS)

        self._velocity_uint = velocity
        self._velocity = uint_to_float(self._velocity_uint, self.MIN_VELOCITY, self.MAX_VELOCITY, self.VELOCITY_BITS)

        self._torque_uint = torque
        self._torque = uint_to_float(self._torque_uint, self.MIN_TORQUE, self.MAX_TORQUE, self.TORQUE_BITS)


@dataclass
class ControllerState:
    """Represents the current state of the controller."""

    MIN_KP = 0.0
    MAX_KP = 500.0
    KP_BITS = 12
    _kp: float = 0
    _kp_uint: int = 0
    MIN_KD = 0.0
    MAX_KD = 5.0
    KD_BITS = 12
    _kd: float
    _kd_uint: int = 0

    def __init__(self, kp: float, kd: float) -> None:
        set_values(kp, kd)

    def set_values(self, kp: float, kd: float):
        """Sets the current state of the controller."""
        self._kp = clamp(kp, self.MIN_KP, self.MAX_KP)
        self._kp_uint = float_to_uint(self._kp, self.MIN_KP, self.MAX_KP, self.KP_BITS)

        self._kd = clamp(kd, self.MIN_KD, self.MAX_KD)
        self._kd_uint = float_to_uint(self._kd, self.MIN_KD, self.MAX_KD, self.KD_BITS)

    def set_unit_values(self, kp: int, kd: int):
        """Sets the current state of the controller from unsigned int."""
        self._kp_uint = kp
        self._kp = uint_to_float(self._kp_uint, self.MIN_KP, self.MAX_KP, self.KP_BITS)

        self._kd_uint = kd
        self._kd = uint_to_float(self._kd_uint, self.MIN_KD, self.MAX_KD, self.KD_BITS)


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

        self.setup_communication(can_socket)
        self.data_utility = MotorDataUtility()

        # TODO: Implement motoring name addressing
        self.name = None
        
        self.motor_state = MotorState(0, 0, 0)
        self.controller_state = ControllerState(0,0)

        self.zero_state_motor = MotorState(0, 0, 0)
        self.zero_state_controller = ControllerState(0, 0)

        zero_state_bytes = self.state_to_bytes(self.zero_state_motor, self.zero_state_controller)
        self.device_id = device_id

        self.COMMANDS = {
            "mot_mode_on": bytes([255, 255, 255, 255, 255, 255, 255, 252]),
            "mot_mode_off": bytes([255, 255, 255, 255, 255, 255, 255, 253]),
            "set_zero": bytes([255, 255, 255, 255, 255, 255, 255, 254]),
            "empty": bytes([0, 0, 0, 0, 0, 0, 0, 0]),
            "zero_state": zero_state_bytes,
        }
        self.torque_limit = 1

    # here we can use an instance of CANSocket
    # insted of making this assignment
    def setup_communication(self, can_bus):
        self.transmitter = can_bus.send_bytes
        self.reciever = can_bus.recive_frame

    def __del__(self):
        print("Motor object was destructed")

    def state_to_bytes(self, motor_state : MotorState, controller_state: ControllerState):
        state_bytes = [
            motor_state._position_uint >> 8,
            motor_state._position_uint & 0xFF,
            motor_state._velocity_uint >> 4,
            ((motor_state._velocity_uint & 0xF) << 4) | (controller_state._kp_uint >> 8),
            controller_state._kp_uint & 0xFF,
            controller_state._kd_uint>> 4,
            ((controller_state._kd_uint & 0xF) << 4) | (motor_state._torque_uint >> 8),
            motor_state._torque_uint & 0xFF,
        ]

        return bytearray(state_bytes)

    def bytes_to_state(self, recived_bytes, motor_state : MotorState):
        if recived_bytes:
            position = (recived_bytes[1] << 8) | recived_bytes[2]
            velocity = (recived_bytes[3] << 4) | (
                recived_bytes[4] >> 4
            )
            torque = (
                (recived_bytes[4] & 0xF) << 8
            ) | recived_bytes[5]
            
            motor_state.set_unit_values(position, velocity, torque)
        else:
            pass

    # ============================================================================================
    # maybe change this somehow to use CANSocket also
    def send_command(self, command):
        self.can_bus.send_bytes(self.device_id, command)

    def recive_reply(self):
        _, _, self.reply = self.reciever()
        return self.reply

    def enable(self):
        self.send_command(self.COMMANDS["mot_mode_on"])
        print("Motor mode enabled")

    def disable(self):
        self.send_command(self.COMMANDS["mot_mode_off"])
        print("Motor mode disabled")

    # Edit this function to be compatable with our Client-Server archeticture
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

    # =============================================================================================

    def set_torque(self, torque):
        if torque > self.torque_limit:
            torque = self.torque_limit
        if torque < -self.torque_limit:
            torque = -self.torque_limit

        state_data_dict = MotorState(0, 0, torque)
        self.send_command(self.state_to_bytes(state_data_dict, self.zero_state_controller))
        self.recive_reply()
        self.bytes_to_state(self.reply)

    def set_torque_limit(self, torque_limit):
        self.torque_limit = torque_limit
        print(f"Torque limit is set to: {torque_limit}")

    def set_state(self, state_data_dict):
        self.send_command(self.state_to_bytes(state_data_dict))
        self.recive_reply()
        self.bytes_to_state(self.reply)
