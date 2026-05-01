cmake_minimum_required(VERSION 3.16)
project(rossim_core)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Python package setup
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  rossim_core/vehicle_model.py
  rossim_core/control_manager.py
  rossim_core/adas_manager.py
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
