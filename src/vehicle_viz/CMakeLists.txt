cmake_minimum_required(VERSION 3.5)
project(vehicle_viz)

find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  vehicle_viz/vehicle_display.py
  vehicle_viz/unified_dashboard.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
