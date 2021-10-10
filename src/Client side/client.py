from numpy.random import poisson
import streamlit as st
import numpy as np
import pandas as pd
import xmlrpc.client
from socket import gaierror
from ClientHandler import ClientHandler
from time import perf_counter

ch = None

st.set_page_config(
    page_title="T-motor Controller",
    page_icon="./Images/T-motor controller-logos.jpeg",
    layout="wide",
    menu_items={
        "Get Help": "https://github.com/SeifAbdElrhman/T-Motor-Controller/blob/main/README.md",
        "Report a Bug": "https://github.com/SeifAbdElrhman/T-Motor-Controller/issues",
        "About": "https://github.com/SeifAbdElrhman/T-Motor-Controller",
    },
)

serverColumn, portColumn, _ = st.columns([1, 1, 6])

with portColumn:
    port = st.text_input("Port Number")
with serverColumn:
    IP = st.text_input("Server IP")
    pressed = st.button("Connect", key="Server Connect")
    if pressed:
        try:
            ch = ClientHandler(IP, port)
            st.write(ch.ping())
        except ConnectionRefusedError:
            st.write("Server offline")
        except gaierror:
            st.write("Add IP and Port")

inputColumn, outputColumn = st.columns([1, 3])

with inputColumn:
    st.markdown("## T motor controller")
    selection = st.selectbox("Motor Port name", ["Can0", "Can1", "Can2"])
    pressed1 = st.button("Connect", key="Motor Connect")
    if pressed1:
        st.write("Motor Connected")
    st.number_input("Input")
    st.number_input("Kp")
    st.number_input("Kd")
    pressed2 = st.button("Send")
    if pressed2:
        st.write("Sending desired Position")
        st.write("Recieving reply...")

with outputColumn:
    placeholder_position_data = pd.DataFrame(
        0, index=np.arange(20), columns=["Position"]
    )
    placeholder_velocity_data = pd.DataFrame(
        0, index=np.arange(20), columns=["Velocity"]
    )
    placeholder_torque_data = pd.DataFrame(0, index=np.arange(20), columns=["Torque"])
    st.line_chart(placeholder_position_data, height=150)
    st.line_chart(placeholder_velocity_data, height=150)
    st.line_chart(placeholder_torque_data, height=150)
