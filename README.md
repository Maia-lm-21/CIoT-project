# CIoT-project - Setting up the environment
## To open the apm planner: 
1. Go to the directory `[your_path]/apm_planner-2.0.30`
2. Run `open ./release/apmplanner2.app`

## To start ardupilot:
1. Go to the directory `[your_path]/ardupilot`
2. Run `./Tools/autotest/sim_vehicle.py -v ArduCopter -L CMAC --out=udp:127.0.0.1:14550 --out=udp:127.0.0.1:14551`
3. Use the commands to start the flight:
    1. `mode guided`
    2. `arm throttle`
    3. `takeoff 20`

## To start the scripts:
1. Go to the scripts directory
2. Run `python3 attack.py` or `python3 spiral_attack.py`
