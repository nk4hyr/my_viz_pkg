# ROS 2 3D Marker & Gradient Trajectory Visualization Lab

## 1. 개요 (Overview)
- ROS 2 환경에서 `visualization_msgs/Marker`와 `MarkerArray`를 활용하여 3D 시각화 요소를 구현하고 RViz2로 검증하는 실습입니다.

## 2. 미션 수행 결과 및 실행 화면

### [미션 1] 3종 마커 통합 시각화 (LINE_STRIP, CUBE, TEXT_VIEW_FACING)
- 전방 S자 주행 경로선, 3D 장애물 박스, 상단 경고 텍스트가 RViz2 화면(`base_link` 기준)에 동시 표출된 화면입니다.
- ![Mission 1 Execution]
(./images/미션1-1.png)
(./images/미션1-2.png)

### [미션 2] `lifetime` 잔상 제거 실증
- 퍼블리셔 노드를 강제 종료(`Ctrl + C`)했을 때, `lifetime`(0.2초) 설정에 의해 화면 잔상이 깔끔하게 소멸하는 것을 확인했습니다.
- ![Mission 2 Execution]
(./images/미션2.png)

### [미션 3] 토픽 패킷 덤프 (`ros2 topic echo`)
- `/visual_markers` 토픽 데이터 구조 검증 로그
\`\`\`yaml
markers:
  - header:
      frame_id: base_link
    ns: "trajectory"
    type: 4 # LINE_STRIP
    lifetime: {sec: 0, nanosec: 200000000}
\`\`\`
(./images/미션3-1.png)
(./images/미션3-2.png)
(./images/미션3-3.png)
(./images/미션3-4.png)
(./images/미션3-5.png)
(./images/미션3-6.png)

### [미션 4] 도전 과제 — 이동 궤적 그라데이션 잔상 시각화 (`SPHERE_LIST`)
- 시간에 따른 차량 이동 궤적에 최신 위치는 진하고 과거 위치는 투명해지는 그라데이션 효과를 구현했습니다.
- ![Mission 4 Execution]
(./images/미션4-1.png)
(./images/미션4-2.png)