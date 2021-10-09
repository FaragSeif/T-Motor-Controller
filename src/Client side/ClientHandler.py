import xmlrpc.client


class ClientHandler:
    def __init__(self, ip, port):
        self.server = xmlrpc.client.ServerProxy(f"http://{ip}:{port}")

    def ping(self):
        self.server.ping()

    def connect_motor(self, motor_port):
        self.server.connect_to_motor(motor_port)

    def disconnect_motor(self):
        self.server.disconnect_motor()

    def set_motor_state(self, desired_position, kp, kd):
        self.server.set_motor_state(desired_position, kp, kd)

    def get_motor_feedback(self):
        return self.server.get_feedback()
