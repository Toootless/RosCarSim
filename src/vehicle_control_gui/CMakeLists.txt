cmake_minimum_required(VERSION 3.16)
project(vehicle_control_gui)

find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  vehicle_control_gui/control_panel.py
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
