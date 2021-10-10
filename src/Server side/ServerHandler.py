import sys
from xmlrpc.server import SimpleXMLRPCServer
from CANSocket import CANSocket
from Tmotor import TMotorQDD, MotorState, ControllerState

if not len(sys.argv) == 3:
    print("Usage example: python ./ServerHandler.py <ip address> <port number>")
    exit()

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

tmotor = None


def connect_to_motor(motor_port, device_id):
    global tmotor

    socket = CANSocket(motor_port)
    tmotor = TMotorQDD(socket, device_id)
    return 1


def set_motor_state(desired_position, kp, kd):
    if tmotor == None:
        return "No motor connected"
    ms = MotorState(desired_position, 0, 0)
    cs = ControllerState(kp, kd)
    command_bytes = tmotor.state_to_bytes(ms, cs)
    tmotor.set_state(command_bytes)
    return get_feedback()


def disconnect_motor():
    global tmotor

    tmotor = None
    return 0


def get_feedback():
    if tmotor == None:
        return "No motor connected"
    ms = MotorState(0, 0, 0)
    reply = tmotor.recive_reply()
    tmotor.bytes_to_state(reply, ms)
    return ms._position.toFloat(), ms._velocity.toFloat(), ms._torque.toFloat()


def ping():
    return "Server pinged successfuly"


def setup_server_functions(xmlrpc_server):
    xmlrpc_server.register_function(connect_to_motor, "connect_to_motor")
    xmlrpc_server.register_function(set_motor_state, "set_motor_state")
    xmlrpc_server.register_function(disconnect_motor, "disconnect_motor")
    xmlrpc_server.register_function(get_feedback, "get_feedback")
    xmlrpc_server.register_function(ping, "ping")


def run_server(server):
    print(f"The server started at {server_ip}:{server_port}")
    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, server quitting")
        exit()


server = SimpleXMLRPCServer((server_ip, int(server_port)), logRequests=False)

setup_server_functions(server)

run_server(server)
