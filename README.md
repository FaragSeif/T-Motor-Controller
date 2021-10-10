<div id="top"></div>

[![GitHub issues](https://img.shields.io/github/issues/SeifAbdElrhman/T-Motor-Controller)](https://gitHub.com/SeifAbdElrhman/T-Motor-Controller/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/SeifAbdElrhman/T-Motor-Controller)](https://gitHub.com/SeifAbdElrhman/T-Motor-Controller/pulls/)
[![GitHub stars](https://img.shields.io/github/stars/SeifAbdElrhman/T-Motor-Controller)](https://github.com/SeifAbdElrhman/T-Motor-Controller/stargazers)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/SeifAbdElrhman/T-Motor-Controller/blob/main/LICENSE)



<!-- PROJECT LOGO -->
<br />
<p align="center">
   <a href="https://github.com/\/T-Motor-Controller">
    <img src="Images/T-motor controller-logos.jpeg" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">T-Motor Controller</h3>

  <p align="center">
    A Fast, Easy, and User Friendly way to control Robotics Actuators. 
    <br />
    <br />
    <a href="https://github.com/SeifAbdElrhman/T-Motor-Controller">View Demo</a>
    ·
    <a href="https://github.com/SeifAbdElrhman/T-Motor-Controller/issues">Report Bug</a>
    ·
    <a href="https://github.com/SeifAbdElrhman/T-Motor-Controller/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#install-prerequisites">Install Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#server-initialization">Server Initialization</a></li>
        <li><a href="#gui-initialization">GUI</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This project provides an easy to use GUI to control the T-Motor brand Robotic Actuators (motors) with feedback Plotting and close to Real-time Control.
The Web app uses a Remote Procedure Call module (RPC). This module connects to a server running on your local or remote linux machine. That machine is connected to the motor over CAN bus. For more explanation on the technical terms please read the [Glossary](documentation/glossary.md) or view the [Documentation](documentation/) to understand more about the architecture of the software.
<br />
#### The GUI provides:
* Easy motor communication setup.
* Easily stop motor operation.
* Manual desired position input.
* An Easy way to Visualize Motor Angles, Velocities, and Torques.
* Visualize Desired values for Angles, Velocities, and Torques.
* Save session plots as PNG for further analysis.
* Set control parameters dynamically.
* CSV desired position input (planned for future).

#### Project Motivation
Working with hardware is usually a very daunting task and it involves debugging both your software and hardware simultaneously, Roboticists usually have to spend a ton of time just to get the actuators to work which sometimes even include writing their own libraries for the actuators instead of focusing on the research at hand AFTER the motor starts working. This is what sparked the idea for this project, for now we will be working with the T-motor brand of motors only since they are quite popular in robotics. Future plans will include expanding to other models/brands and motor types. The end goal is to help Roboticists focus on what matters in their research.



### Built With

* [Python]()
* [Streamlit](https://streamlit.io/)
* [xmlrpc](https://docs.python.org/3/library/xmlrpc.html)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

The Server side should be running on your desired remote (for example a raspberry pi) or local machine. and the client side can run from anywhere (even on windows).

#### Install Prerequisites
First you need to install Python 3.6 or higher, then you can install the requirements from the command below on both your remote and local machines.<br>
*the command should run in the same folder as the requirements.txt file, otherwise provide file path*
*(i.e. "path/to/file/requirements.txt")*<br/>
  ```sh
  pip install -r requirements.txt
  ```

#### Installation

Clone the repo from the terminal if you have git, or simply click the "download ZIP" from github.
   ```sh
   git clone https://github.com/SeifAbdElrhman/T-Motor-Controller.git
   ```
#### Server Initialization

Copy the Server side folder to your desired remote (or local) machine, and run the ServerHandler.py file using the following command.
   ```sh
   python ./ServerHandler.py <ip_address> <port#>
   ```
   Don't forget to substitue "<ip_address>" and "<port#>" with your actual IP and Port for the remote machine (for local machine you can use "127.0.0.1" without quotes as the IP)
   

#### GUI Initialization 
Now you can run the client.py file on your client machine (this machine doesn't have to be linux) with the following command.
```sh
streamlit run client.py
```
if your terminal is open on the full project folder please provide the path as "./src/Clien\ side/client.py".
if you have a different directory structure provide your own path to the client.py file.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Place Holder

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap
Currently we are working on multiple variants of a specific model of T-motors (the QDD AK80-6T, AK80-9T, AK45, and the AK30). Later we will expand to more models of T-motor. and Eventually fork to other brands.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated** and will boost the development of the Robotics community.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For any bugs, issues, additional features, please open an [issue](https://github.com/SeifAbdElrhman/T-Motor-Controller/issues) on github with a detailed description and a proper Tag. Or feel free to [contact](#contact) the developers of the project directly

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Seif Farag - [@FaragSeif](https://t.me/FaragSeif) - s.farag@innopolis.university
<br />
Nabila Adawy - [@NabilaAdawy](https://t.me/NabilaAdawy) - n.roshdy@innopolis.university
<br />
Sherif Nafee- [@Sh1co](https://t.me/Sh1co) - s.nafee@innopolis.university

Project Link: [https://github.com/SeifAbdElrhman/T-Motor-Controller](https://github.com/SeifAbdElrhman/T-Motor-Controller)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* Thanks to Simeon Nedelchev for his amazing control Library - [rPyControl](https://github.com/SimkaNed/rPyControl)

<p align="right">(<a href="#top">back to top</a>)</p>
