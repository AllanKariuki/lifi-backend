### Lifi dummy server.
## Introduction
This is a dummy server for lifi which aims at mimicing the transmission of sensor data from stm32 to the application.
The server is written in python and uses the flask library to create a web server.
The server is generates random values of sensor data and sends it to the application.
The server uses websocket connection to send this data.

## Installation
To install the server, you need to have python installed on your system.
You can install python from [here](https://www.python.org/downloads/).
Then clone the repository to your local machine.
```bash
  git clone https://github.com/AllanKariuki/lifi-backend.git
```
After cloning the repository, navigate to the project directory.
```bash
  cd lifi-backend
```

Create a virtual environment and activate it.
```bash
  python -m venv venv
  or virtualenv venv
  source venv/bin/activate
```

Install the required packages.
```bash
  pip install -r requirements.txt
```

## Running the server
To run the server, you need to run the following command.
```bash
  python server3.py
```

This sets up a wevsocket server on port 5000.
You can now connect to the server using the application.
```bash
    ws://localhost:5000/ws
```