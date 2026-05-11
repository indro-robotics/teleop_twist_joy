import asyncio
import websockets
from sensor_msgs.msg import Joy
import rclpy


pub = rclpy.Publisher('/joy', Joy, queue_size=10)
rclpy.init_node('websocket_vr_bridge')
rate = rclpy.Rate(10)

async def echo_handler(websocket):
    """
    Handles a single WebSocket connection.
    Echoes back any message received from the client.
    """
    prev_msg = "None"
    
    try:
        # Iterate over incoming messages asynchronously
        async for message in websocket:

            if isinstance(message, str):data

                if message != prev_msg:
                    print(f"{message}")
                    
                prev_msg = message
                msg_arr = message.split(',')

                # Lx, Ly, Rx, Ry, L_trig, LI_trig, R_trig, RI_trig

                JL_UpDown = float(msg_arr[1]) #float(L_Joystick.strip(')').strip('(').split(',')[1])
                JL_RightLeft = float(msg_arr[0]) #float(L_Joystick.strip(')').strip('(').split(',')[0])
                JR_RightLeft = float(msg_arr[2]) #float(R_Joystick.strip(')').strip('(').split(',')[0])
                JR_UpDown = flaot(msg_arr[3])
                
                L_trig = float(msg_arr[4])
                LI_trig = float(msg_arr[5])
                R_trig = float(msg_arr[6])
                RI_trig = float(msg_arr[7])

                joy_msg = Joy()
                joy_msg.header.stamp = rospy.Time.now()
                #joy_msg.header.frame_id = "joy"
                joy_msg.axes =  [JL_RightLeft, JL_UpDown, JR_RightLeft, JR_UpDown, L_trig, R_trig, LI_trig, RI_trig]
                joy_msg.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                pub.publish(joy_msg)

    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected gracefully")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    """
    Starts the WebSocket server on localhost, port 3000.
    """
    # The 'serve' function from the library associates the handler with a host and port
    async with websockets.serve(echo_handler, "0.0.0.0", 3000):
        print("WebSocket server started at ws://localhost:3000")
        # Run forever to keep the server alive
        await asyncio.Future()

if __name__ == "__main__":
    # Run the main asynchronous function
    asyncio.run(main())

