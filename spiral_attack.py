import time
import math
from pymavlink import mavutil

# The command used to start the ardupilot software opened two ports: 1 to connect to the apm planner
# and the other to connect into this script 

# We use mavutil.mavlink_connection to connect the script to the Drone on port 14551
print("--- Connecting to drone on port 14551 ---")
master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
master.wait_heartbeat()
print(f"--- TARGET ACQUIRED ---")

# Variables used for the spiral math
start_time = time.time()
radius = 0

# Main cycle of the script
while True:
    
    # We start by reading the drone's position to see if it is already at 10m of altitude
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    
    if msg:
        # Since the units that the message received are not meters, we need to do some calculations
        altitude = msg.relative_alt / 1000.0
        
        # Only attack above 10 meters
        if altitude > 10:
            # Calculate elapsed time
            t = time.time() - start_time
            
            # We make the radius grow larger over time to recreate the Spiral effect
            radius += 0.000005 
            
            # Using SIN and COS to create a circular offset
            # X changes with Sine, Y changes with Cosine
            glitch_lat = math.sin(t) * radius
            glitch_lon = math.cos(t) * radius

            # Print status on the same line to keep terminal clean and to make more visible of what the script is doing
            print(f"Alt: {altitude:.1f}m | Spiraling... Rad: {radius:.6f}", end="\r")
            
            # Sending the new fake GPS coordinates - Latitude Glitch (Y)
            master.mav.param_set_send(
                master.target_system, master.target_component,
                b'SIM_GPS_GLITCH_Y',
                glitch_lat, # The fake value
                mavutil.mavlink.MAV_PARAM_TYPE_REAL32
            )

            # Sending the new fake GPS coordinates - Longitude Glitch (X)
            master.mav.param_set_send(
                master.target_system, master.target_component,
                b'SIM_GPS_GLITCH_X',
                glitch_lon, # The fake value
                mavutil.mavlink.MAV_PARAM_TYPE_REAL32
            )
    
    # we run this loop 10 times per second to make it look real
    time.sleep(0.1)