import time
import math
from pymavlink import mavutil

# Connect to the simulator
print("--- Connecting to drone on port 14551 ---")
master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
master.wait_heartbeat()
print(f"--- TARGET ACQUIRED ---")

# Variables for the spiral math
start_time = time.time()
radius = 0

while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    
    if msg:
        altitude = msg.relative_alt / 1000.0
        
        # Only attack above 10 meters
        if altitude > 10:
            # Calculate elapsed time
            t = time.time() - start_time
            
            # --- THE MATH MAGIC ---
            # We make the radius grow larger over time (Spiral effect)
            radius += 0.000005 
            
            # Use SIN and COS to create a circular offset
            # X changes with Sine, Y changes with Cosine
            glitch_lat = math.sin(t) * radius
            glitch_lon = math.cos(t) * radius

            print(f"Alt: {altitude:.1f}m | Spiraling... Rad: {radius:.6f}", end="\r")
            
            # 1. Send Latitude Glitch (Y)
            master.mav.param_set_send(
                master.target_system, master.target_component,
                b'SIM_GPS_GLITCH_Y',
                glitch_lat,
                mavutil.mavlink.MAV_PARAM_TYPE_REAL32
            )

            # 2. Send Longitude Glitch (X) - We attack both axes now!
            master.mav.param_set_send(
                master.target_system, master.target_component,
                b'SIM_GPS_GLITCH_X',
                glitch_lon,
                mavutil.mavlink.MAV_PARAM_TYPE_REAL32
            )

    time.sleep(0.1)