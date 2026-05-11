import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import asyncio
import websockets
import threading
import json


class JoyWebsocketPublisher(Node):
    def __init__(self):
        super().__init__('joy_websocket_publisher')
        # Publisher for /joy topic
        self.publisher_ = self.create_publisher(Joy, 'joy', 10)
        self.get_logger().info('Joy Publisher Node Started')

    def publish_joy(self, axes, buttons):
        msg = Joy()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'joy_link'
        msg.axes = axes
        msg.buttons = buttons
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published Joy: A:{axes} B:{buttons}')


rclpy.init()
node = JoyWebsocketPublisher()

# --- WebSocket Server Setup ---
async def websocket_handler(websocket):
    
    async for message in websocket:

        if isinstance(message, str):
            #if message != prev_msg:
            #    print(f"{message}")
                
            #prev_msg = message
            msg_arr = message.split(',')

            # Lx, Ly, Rx, Ry, L_trig, LI_trig, R_trig, RI_trig

            JL_UpDown = float(msg_arr[1]) #float(L_Joystick.strip(')').strip('(').split(',')[1])
            JL_RightLeft = float(msg_arr[0]) #float(L_Joystick.strip(')').strip('(').split(',')[0])
            JR_RightLeft = float(msg_arr[2]) #float(R_Joystick.strip(')').strip('(').split(',')[0])
            JR_UpDown = float(msg_arr[3])
            
            L_trig = float(msg_arr[4])
            LI_trig = float(msg_arr[5])
            R_trig = float(msg_arr[6])
            RI_trig = float(msg_arr[7])

            Ab = int(msg_arr[8].lower() == "true")
            Bb = int(msg_arr[9].lower() == "true")
            Xb = int(msg_arr[10].lower() == "true")
            Yb = int(msg_arr[11].lower() == "true")

            #joy_msg = Joy()
            #joy_msg.header.stamp = rospy.Time.now()
            #joy_msg.header.frame_id = "joy"
            axes =  [JL_RightLeft, -JL_UpDown, JR_RightLeft, -JR_UpDown]
            buttons = [Ab, Bb, Xb, Yb, int(L_trig), int(R_trig), int(LI_trig), int(RI_trig), 0, 0, 0]

            node.publish_joy(axes, buttons)

async def start_websocket_server(node):
    # asyncio.set_event_loop(asyncio.new_event_loop())
    # # Serve on localhost:3000
    # server = websockets.serve(
    #     lambda ws, path: websocket_handler(ws, path, node), 
    #     'localhost', 3000
    # )
    # asyncio.get_event_loop().run_until_complete(server)
    # asyncio.get_event_loop().run_forever()
    """
    Starts the WebSocket server on localhost, port 8765.
    """
    # The 'serve' function from the library associates the handler with a host and port
    async with websockets.serve(echo_handler, "0.0.0.0", 8765):
        print("WebSocket server started at ws://localhost:8765")
        # Run forever to keep the server alive
        await asyncio.Future()

# --- Main ---
async def main(args=None):

    # Start WebSocket server in a separate thread
    #ws_thread = threading.Thread(target=start_websocket_server, args=(node,), daemon=True)
    #ws_thread.start()
    """
    Starts the WebSocket server on localhost, port 8765.
    """
    # The 'serve' function from the library associates the handler with a host and port
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        print("WebSocket server started at ws://localhost:8765")
        # Run forever to keep the server alive
        await asyncio.Future()

    # Spin ROS 2 node
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
