from abc import ABC
from dataclasses import dataclass
from CANSocket import CANSocket
import builtins


def clamp(value: float, min: float, max: float):
    return builtins.max(min, builtins.min(max, value))


# @dataclass
class MotorState:
    """Represents the current state of the motor."""

    MIN_POSITION = -95.5
    MAX_POSITION = -95.5
    _position: float = 0
    MIN_VELOCITY = -30.0
    MAX_VELOCITY = 30.0
    velocity: float = 0
    MIN_TORQUE = -18.0
    MAX_TORQUE = 18.0
    torque: float = 0

    def __init__(self, position: float, velocity: float, torque: float) -> None:
        set_values(position, velocity, torque)

    def set_values(self, position: float, velocity: float, torque: float):
        self._position = clamp(
            position, MotorState.MIN_POSITION, MotorState.MAX_POSITION
        )
        self.velocity = clamp(
            velocity, MotorState.MIN_VELOCITY, MotorState.MAX_VELOCITY
        )
        self.torque = clamp(
            torque, MotorState.MIN_TORQUE, MotorState.MAX_TORQUE
        )


@dataclass
class ControllerState:
    kp: float
    kd: float


class Frame:
    def __init__(self, state: MotorState, min_state: MotorState):
        self.state = state


class TMotor(ABC):
    pass


class MotorDataUtility:

    def float_to_uint(
        self, data_float: float, data_min: float, data_max: float, bits: int
    ) -> int:
        span = data_max - data_min
        return int((data_float - data_min) * (float((1 << bits) - 1)) / span)

    def uint_to_float(
        self, data_int: int, data_min: int, data_max: int, bits: int
    ) -> float:
        span = data_max - data_min
        return float(data_int) * span / float((1 << bits) - 1) + data_min


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

        self.state_send = ["pos", "vel", "kp", "kd", "tor"]
        state_bounds = [
            [-95.5, 95.5],
            [-30.0, 30.0],
            [0.0, 500.0],
            [0.0, 5.0],
            [-18.0, 18.0],
        ]
        self.state_bits = dict(zip(self.state_send, [16, 12, 12, 12, 12]))
        self.des_state_int = dict(zip(self.state_send, [0, 0, 0, 0, 0]))
        self.zero_state = dict(zip(self.state_send, [0.0, 0.0, 0.0, 0.0, 0.0]))
        self.states_recv = ["pos", "vel", "tor"]
        self.state_recv_bytes = dict(zip(self.states_recv, [b"\x00", b"\x00", b"\x00"]))
        self.state = dict(zip(self.states_recv, [0.0, 0.0, 0.0]))  # MotorState()

        self.bounds = dict(zip(self.state_send, state_bounds))
        zero_state_bytes = self.state_to_bytes(self.zero_state)
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

    def state_to_bytes(self, state_dict):
        for state_label in self.state_send:
            self.des_state_int[state_label] = self.float_to_uint(
                state_dict[state_label],
                self.bounds[state_label][0],
                self.bounds[state_label][1],
                self.state_bits[state_label],
            )

        state_bytes = [
            self.des_state_int["pos"] >> 8,
            self.des_state_int["pos"] & 0xFF,
            self.des_state_int["vel"] >> 4,
            ((self.des_state_int["vel"] & 0xF) << 4) | (self.des_state_int["kp"] >> 8),
            self.des_state_int["kp"] & 0xFF,
            self.des_state_int["kd"] >> 4,
            ((self.des_state_int["kd"] & 0xF) << 4) | (self.des_state_int["tor"] >> 8),
            self.des_state_int["tor"] & 0xFF,
        ]

        return bytearray(state_bytes)

    def bytes_to_state(self, recived_bytes):
        if recived_bytes:
            self.state_recv_bytes["pos"] = (recived_bytes[1] << 8) | recived_bytes[2]
            self.state_recv_bytes["vel"] = (recived_bytes[3] << 4) | (
                recived_bytes[4] >> 4
            )
            self.state_recv_bytes["tor"] = (
                (recived_bytes[4] & 0xF) << 8
            ) | recived_bytes[5]

            # self.state.position = self.uint_to_float(
            #     self.state_recv_bytes['position'],
            #     self.bounds['position'][0],
            #     self.bounds['position'][1],
            #     self.state_bits['position'],
            # )
            for state_label in self.states_recv:
                self.state[state_label] = self.uint_to_float(
                    self.state_recv_bytes[state_label],
                    self.bounds[state_label][0],
                    self.bounds[state_label][1],
                    self.state_bits[state_label],
                )
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

        state_data_dict = self.zero_state.copy()
        state_data_dict["tor"] = torque
        self.send_command(self.state_to_bytes(state_data_dict))
        self.recive_reply()
        self.bytes_to_state(self.reply)

    def set_torque_limit(self, torque_limit):
        self.torque_limit = torque_limit
        print(f"Torque limit is set to: {torque_limit}")

    def set_state(self, state_data_dict):
        self.send_command(self.state_to_bytes(state_data_dict))
        self.recive_reply()
        self.bytes_to_state(self.reply)
