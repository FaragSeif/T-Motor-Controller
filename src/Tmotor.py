from CANSocket import CANDevice


class TMotorQDD:
    # TODO:
    # add tx_message dict
    # add rx_message dict
    def __init__(self, can_socket=None, device_id=0x001, rxtx_interface=None):

        # TODO: pass dict with reciver/transmitter functions from the specific bus
        if not can_socket:
            print("Provide can_bus as argument")
            self.__del__()

        self.setup_communication(can_socket)

        # TODO: Implement motoring name addressing
        self.name = None

        self.set_state_settings()

        self.bounds = dict(zip(self.state_send, self.state_bounds))
        self.device_id = device_id

        self.commands = {
            "mot_mode_on": b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFC",
            "mot_mode_off": b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFD",
            "set_zero": b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE",
            "empty": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "zero_state": self.zero_state_bytes,
        }

        self.t_data = self.commands["mot_mode_off"]
        self.r_data = self.commands["empty"]
        self.torque_limit = 1
        self.gear_ratio = 6
        self.torque_constant = 1
        self.message = {self.device_id: self.commands["zero_state"]}

    def set_state_settings(self):
        self.state_send = ["pos", "vel", "kp", "kd", "tor"]
        self.state_bounds = [
            [-95.5, 95.5],
            [-30.0, 30.0],
            [0.0, 500.0],
            [0.0, 5.0],
            [-18.0, 18.0],
        ]
        self.state_bits = dict(zip(self.state_send, [16, 12, 12, 12, 12]))
        self.des_state_int = dict(zip(self.state_send, [0, 0, 0, 0, 0]))
        self.zero_state = dict(zip(self.state_send, [0.0, 0.0, 0.0, 0.0, 0.0]))
        self.zero_state_bytes = self.state_to_bytes(self.zero_state)
        self.states_recv = ["pos", "vel", "tor"]
        self.state_recv_bytes = dict(zip(self.states_recv, [b"\x00", b"\x00", b"\x00"]))
        self.state_recv_ints = dict(zip(self.states_recv, [0, 0, 0]))
        self.state = dict(zip(self.states_recv, [0.0, 0.0, 0.0]))

    def setup_communication(self, can_bus):
        self.transmiter = can_bus.send_bytes
        self.reciver = can_bus.recive_frame

    def __del__(self):
        print("Motor object was destructed")

    def float_to_uint(self, data_float, data_min, data_max, bits):
        span = data_max - data_min
        offset = data_min
        return int((data_float - offset) * (float((1 << bits) - 1)) / span)

    def uint_to_float(self, data_int, data_min, data_max, bits):
        span = data_max - data_min
        offset = data_min
        return (float(data_int)) * span / (float((1 << bits) - 1)) + offset

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

            for state_label in self.states_recv:
                self.state[state_label] = self.uint_to_float(
                    self.state_recv_bytes[state_label],
                    self.bounds[state_label][0],
                    self.bounds[state_label][1],
                    self.state_bits[state_label],
                )
        else:
            pass

    def send_command(self, command):
        self.transmiter(self.device_id, command)

    def recive_reply(self):
        _, _, self.reply = self.reciver()
        return self.reply

    def enable(self):
        self.send_command(self.commands["mot_mode_on"])
        print("Motor mode enabled")

    def disable(self):
        self.send_command(self.commands["mot_mode_off"])
        print("Motor mode disabled")

    def set_zero(self):
        print(
            f'You are going to assign a new zero for motor with ID {self.device_id}, press "Y" to continue...\n'
        )
        user_input = input()
        if user_input == "Y" or user_input == "y":
            self.send_command(self.commands["set_zero"])
            print("New encoder zero is setted")
        else:
            print("Canceling...")

    def set_torque(self, torque):
        if torque > self.torque_limit:
            torque = self.torque_limit
        if torque < -self.torque_limit:
            torque = -self.torque_limit

        state_data_dict = self.zero_state
        state_data_dict["tor"] = torque
        self.send_command(self.state_to_bytes(state_data_dict))
        self.recive_reply()
        self.bytes_to_state(self.reply)

    def set_torque_limit(self, torque_limit):
        self.torque_limit = torque_limit
        print(f"Torque limit is seted to: {torque_limit}")

    def set_state(self, state_data_dict):
        self.send_command(self.state_to_bytes(state_data_dict))
        self.recive_reply()
        self.bytes_to_state(self.reply)
