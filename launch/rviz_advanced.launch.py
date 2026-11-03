import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 패키지 공유 디렉토리 경로 획득
    pkg_share = get_package_share_directory('my_viz_pkg')
    
    # rviz 설정 파일 경로 지정 (config 폴더 안의 integrated_view.rviz)
    rviz_config_path = os.path.join(pkg_share, 'config', 'integrated_view.rviz')

    return LaunchDescription([
        # 1. 커스텀 마커 퍼블리셔 노드 기동 (use_sim_time 추가)
        Node(
            package="my_viz_pkg",
            executable="custom_marker_publisher",
            name="marker_publisher",
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
        
        # 2. 사전 설정된 rviz 설정 파일 로드하며 Rviz2 기동 (use_sim_time 추가)
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config_path],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
    ])