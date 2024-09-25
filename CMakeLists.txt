cmake_minimum_required(VERSION 3.8)
project(turtlebot4_setup)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(
  PROGRAMS ${PROJECT_NAME}/turtlebot4_setup
  DESTINATION lib/${PROJECT_NAME}
)

# disable XML linting; it consistently times out
# TODO (civerachb-cpr) -- figure out why it's timing out and re-enable
# hypothesis: it's related to the additional XML files in etc/turtlebot4
list(APPEND AMENT_LINT_AUTO_EXCLUDE
  ament_cmake_xmllint
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
