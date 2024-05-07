# RasPi View Glass Emulator

This repository contains the test plan, automated test cases, and source code for the RasPi View Glass Emulator project. The emulator simulates the behavior of View Glass by adjusting its tint based on the current weather, visibility, and temperature of the environment.

## Task Description

During the development of this project, the following tasks were undertaken:

1. **Studied the Code**: Thoroughly analyzed the provided source code (`weather.py`) to understand its functionality and business logic.
2. **Built a Test Plan**: Created a comprehensive test plan to validate the business logic of the emulator under different weather scenarios.
3. **Automated the Test Cases**: Developed automated test cases based on the test plan.
4. **Tested the Provided Test Kit based on RasPi**: Conducted testing on a RasPi test kit provided for the project, utilizing the provided source code. The emulator was tested according to the developed test plan, and the results were documented.

## Instructions

To execute the scripts and test the emulator, follow these instructions:

### Prerequisites:
- RasPi test kit
- Display cable, keyboard, and network cable

### Setup:
1. Plug in the RasPi test kit and ensure the network is up.
2. Boot up the RasPi and open the console.

### Execution:
1. Navigate to `/home/pi` or `/Downloads`.
2. Locate the `weather.py` file.
3. Run the script using the command: `python weather.py`.
4. Wait for 5 seconds for the LED array to light up, reflecting the current weather conditions.

### Test Plan Execution:
Refer to the provided test plan document for detailed instructions on executing the test cases.

## Repository Structure

- `weather.py`:  The provided source code for the RasPi View Glass emulator.
- `Test_plan.pdf`: Detailed test plan document outlining the test cases and procedures.
- `weather3.py`: Fixed bug in the source code and modified to allow feeding desired data for some test cases in the test plan.
- `Test scripts`: Additional scripts for automated testing.
