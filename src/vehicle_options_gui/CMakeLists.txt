cmake_minimum_required(VERSION 3.16)
project(vehicle_options_gui)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  vehicle_options_gui/options_panel.py
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
