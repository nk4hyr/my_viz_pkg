import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
import math

class CustomMarkerPublisher(Node):
    def __init__(self):
        super().__init__('custom_marker_publisher')
        
        # /visual_markers 토픽으로 MarkerArray를 발행하는 퍼블리셔 선언 (10Hz)
        self.pub_markers = self.create_publisher(MarkerArray, '/visual_markers', 10)
        self.timer = self.create_timer(0.1, self.publish_markers)
        
        # 미션 4 그라데이션 궤적 애니메이션을 위한 카운터 변수
        self.counter = 0
        
        self.get_logger().info("Custom Marker Publisher 노드가 시작되었습니다.")

    def publish_markers(self):
        self.counter += 1
        current_time = self.get_clock().now().to_msg()

        # -------------------------------------------------------------
        # 2단계 — 전방 가상 주행 경로선 (LINE_STRIP) 생성
        # -------------------------------------------------------------
        path_marker = Marker()
        path_marker.header.frame_id = "base_link"
        path_marker.header.stamp = current_time
        path_marker.ns = "trajectory"
        path_marker.id = 0
        path_marker.type = Marker.LINE_STRIP
        path_marker.action = Marker.ADD
        path_marker.scale.x = 0.08  # 선 두께 8cm
        path_marker.color.g = 1.0   # 초록색
        path_marker.color.a = 0.8   # 반투명 80%
        path_marker.lifetime = Duration(seconds=0.2).to_msg()

        # 전방 5m S자 곡선 40개 정점 생성
        for i in range(40):
            p = Point()
            p.x = i * 0.125  # 0m ~ 5m
            p.y = 0.4 * math.sin(i * 0.2)
            p.z = 0.0
            path_marker.points.append(p)

        # -------------------------------------------------------------
        # 3단계 — 3D 장애물 박스 (CUBE) 및 텍스트 마커 생성
        # -------------------------------------------------------------
        # 전방 3m 지점 가상 장애물 3D 바운딩 박스
        box = Marker()
        box.header.frame_id = "base_link"
        box.header.stamp = current_time
        box.ns = "obstacles"
        box.id = 1
        box.type = Marker.CUBE
        box.action = Marker.ADD
        box.pose.position.x = 3.0
        box.pose.position.y = 0.2
        box.pose.position.z = 0.4
        box.scale.x = 0.8
        box.scale.y = 0.8
        box.scale.z = 0.8
        box.color.r = 1.0
        box.color.g = 0.0
        box.color.b = 0.0
        box.color.a = 0.6  # 반투명 빨강
        box.lifetime = Duration(seconds=0.2).to_msg()

        # 장애물 상단 텍스트 라벨 (TEXT_VIEW_FACING)
        txt = Marker()
        txt.header.frame_id = "base_link"
        txt.header.stamp = current_time
        txt.ns = "labels"
        txt.id = 2
        txt.type = Marker.TEXT_VIEW_FACING
        txt.action = Marker.ADD
        txt.pose.position.x = 3.0
        txt.pose.position.y = 0.2
        txt.pose.position.z = 1.0
        txt.scale.z = 0.25  # 폰트 크기 25cm
        txt.text = "WARNING: OBSTACLE [3.0m]"
        txt.color.r = 1.0
        txt.color.g = 1.0
        txt.color.b = 1.0
        txt.color.a = 1.0
        txt.lifetime = Duration(seconds=0.2).to_msg()

        # -------------------------------------------------------------
        # 미션 4 (도전) — 이동 궤적 그라데이션 및 잔상 시각화 (SPHERE_LIST)
        # -------------------------------------------------------------
        grad_marker = Marker()
        grad_marker.header.frame_id = "base_link"
        grad_marker.header.stamp = current_time
        grad_marker.ns = "trajectory_gradient"
        grad_marker.id = 3
        grad_marker.type = Marker.SPHERE_LIST
        grad_marker.action = Marker.ADD
        grad_marker.scale.x = 0.12
        grad_marker.scale.y = 0.12
        grad_marker.scale.z = 0.12
        grad_marker.lifetime = Duration(seconds=0.2).to_msg()

        # 과거 궤적 포인트들을 생성하고 그라데이션 투명도 부여
        num_points = 25
        for i in range(num_points):
            t_offset = (self.counter * 0.05) - (i * 0.08)
            p = Point()
            p.x = 1.0 + (i * 0.08)
            p.y = 0.5 * math.sin(t_offset)
            p.z = 0.1
            grad_marker.points.append(p)

            # 최신 포인트일수록 진하고(alpha=1.0), 오래된 포인트일수록 투명해지는(alpha=0.1) 효과
            alpha = float(num_points - i) / num_points
            color = ColorRGBA()
            color.r = 0.0
            color.g = 0.8
            color.b = 1.0
            color.a = max(0.1, alpha)
            grad_marker.colors.append(color)

        # -------------------------------------------------------------
        # 4단계 — MarkerArray 래핑 및 10Hz 발행
        # -------------------------------------------------------------
        marker_array = MarkerArray()
        marker_array.markers.append(path_marker)
        marker_array.markers.append(box)
        marker_array.markers.append(txt)
        marker_array.markers.append(grad_marker)

        self.pub_markers.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = CustomMarkerPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()