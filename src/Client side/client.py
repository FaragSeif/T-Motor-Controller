import streamlit as st
import numpy as np
import pandas as pd
from ClientHandler import ClientHandler


st.markdown("# T motor controller")

ch = ClientHandler("127.0.0.1", 6969)

inputColumn, outputColumn = st.columns(2)

with inputColumn:
    selection = st.selectbox("Port name", ["Can0", "Can1", "Can2"])
    if st.button("Connect"):
        ch.ping()
    st.text_input("Input")
    st.text_input("Kp")
    st.text_input("Kd")
    if st.button("Send"):
        st.write(selection)
        # Add connection logic
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
