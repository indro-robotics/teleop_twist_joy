import os

from ament_index_python.packages import get_package_share_directory

import launch
import launch.conditions
import launch_ros.actions


def generate_launch_description():
    joy_config = launch.substitutions.LaunchConfiguration('joy_config')
    joy_dev = launch.substitutions.LaunchConfiguration('joy_dev')
    config_filepath = launch.substitutions.LaunchConfiguration('config_filepath')
    use_joy_node = launch.substitutions.LaunchConfiguration('use_joy_node')

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument('joy_vel', default_value='/fort/vel'),
        launch.actions.DeclareLaunchArgument('joy_config', default_value='ps3'),
        launch.actions.DeclareLaunchArgument('joy_dev', default_value='/dev/input/js0'),
        launch.actions.DeclareLaunchArgument('use_joy_node', default_value='true',
            description='Whether to launch the joy_node locally (true) or use remote joy_node (false)'),
        launch.actions.DeclareLaunchArgument('config_filepath', default_value=[
            launch.substitutions.TextSubstitution(text=os.path.join(
                get_package_share_directory('teleop_twist_joy'), 'config', '')),
            joy_config, launch.substitutions.TextSubstitution(text='.config.yaml')]),

        # Joy node to read from joystick device and publish to /joy topic (optional)
        launch.actions.GroupAction([
            launch_ros.actions.Node(
                package='joy', executable='joy_node',
                name='joy_node', parameters=[{
                    'dev': joy_dev,
                    'deadzone': 0.3,
                    'autorepeat_rate': 20.0,
                }],
                remappings=[('joy', '/fort/joy')]
                ),
        ], condition=launch.conditions.IfCondition(use_joy_node)),
        
        # Teleop node to convert joystick data to velocity commands
        launch_ros.actions.Node(
            package='teleop_twist_joy', executable='teleop_node',
            name='teleop_twist_joy_node', parameters=[config_filepath],
            remappings={('/fort/vel', launch.substitutions.LaunchConfiguration('joy_vel'))},
            ),
    ])
