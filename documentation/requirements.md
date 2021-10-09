# Functional Requirements 
# 
ID |  User Story Title |  Priority | Any Other Label
------------ | ------------- | ------------- | ------------- 
1 | CAN-Bus Connection | Must | Mandatory / Verifiable
2 | Send Input Angle | Must | Doable
3 | Feedback Plotting | Must | Mandatory / Doable
4 | Set Control Parameters | Must | Relievant
5 | CMD line reporting |Must |Good to have
6 | Save plots as PNG | Should | Good to have

# Use-Cases
#
Title  |  Use Case
------------ | -------------
CAN-Bus Connection | As a Web User I want to Connect to my Motor Through CAN-Bus so that I can communicate with my motor.
||As a Web User I want  to choose my COM port so that I can establish the communication to the right port.
||As a Web User I want to Disconnect from the CAN-Bus so that i can stop the Motor.
Send Input angle | As a Web User I want to type the desired angle so that it can be sent and executed by the motor.
Feedback Plots | As a Web User I want to get feedback plots of motor position so that i can monitor motor performance.
||As a Web User I want to get feedback plots of motor velocity so that i can monitor motor performance
||As a Web User I want to get feedback plots of motor torque so that i can monitor motor performance
||As a Web User I want to get plots of Desired position so that i can compare it to motor performance
||As a Web User I want to get plots of Desired velocity so that i can compare it to motor performance
||As a Web User I want to get plots of Desired torque so that i can compare it to motor performance
Set Control Parameters | As a Web User I want to change control parameters so that i can adjust the motor response.
CMD line reporting | As a Web User I want to have Command Line reporting So that I see connection status.
||As a Web User I want to have Command Line reporting So that I see Error reports
Save Plots as PNG | As a Web User I want to save the current session plots as PNG so that I can reuse it later for analsys.

# Non-Functional Requirement 
# 
NFR | How will you achieve it
------------ | -------------
Client-Server Latency | Latency to/from client-server should not exceed 25 millisecond , this can be done by using a lightweight webserver such as [socket.IO](https://python-socketio.readthedocs.io/en/latest/intro.html#what-is-socket-io) or a simple [xmlrpc](https://docs.python.org/3/library/xmlrpc.html)
Server-Hardware Latency | Latency between server and hardware should not exceed 5 millisecond, this is already achieved through fast communication protocol and optimized code
Installation | The app should have minimum installation steps (maximum of 5 steps)
User Interface | The app should have a very intuitive user interface that requires minimum to no previous knowledge of the app. This can be done through an aesthetic design and descriptive tooltips for each block of the interface.
Single Tab Interface | The App should have a single tab interface to lessen the intimidation of the multi-tab apps, this can be done by a good design and layout of the user interface to strike a balance between having a single tab and not having a cluttered interface.

