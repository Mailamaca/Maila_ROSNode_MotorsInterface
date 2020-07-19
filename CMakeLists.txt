cmake_minimum_required(VERSION 2.8.3)
project(hardware_interface)


## Compile as C++11, supported in ROS Kinetic and newer


find_library(wiringPi_LIB wiringPi)

if(NOT wiringPi_LIB)
  add_compile_options(-std=c++11 -DIS_PC)  
else()
  add_compile_options(-std=c++11)  
endif()

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  custom_msgs
)

## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)


###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
  INCLUDE_DIRS include
#  LIBRARIES hardware_interface
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

## Declare a C++ executable
## With catkin_make all packages are built within a single CMake context
## The recommended prefix ensures that target names across packages don't collide

if(NOT wiringPi_LIB)
  add_executable(${PROJECT_NAME}_node 
  	src/hardware_interface_node.cpp  	
  )
else()
  add_executable(${PROJECT_NAME}_node 
    src/hardware_interface_node.cpp
    src/pca9685/pca9685.c
  )
endif()
 

## Rename C++ executable without prefix
## The above recommended prefix causes long target names, the following renames the
## target back to the shorter version for ease of user use
## e.g. "rosrun someones_pkg node" instead of "rosrun someones_pkg someones_pkg_node"
# set_target_properties(${PROJECT_NAME}_node PROPERTIES OUTPUT_NAME node PREFIX "")

## Add cmake target dependencies of the executable
## same as for the library above
add_dependencies(${PROJECT_NAME}_node 
	${${PROJECT_NAME}_EXPORTED_TARGETS} 
	${catkin_EXPORTED_TARGETS}
)

## Specify libraries to link a library or executable target against
if(NOT wiringPi_LIB)
target_link_libraries(${PROJECT_NAME}_node
 ${catkin_LIBRARIES} 
)
else()
target_link_libraries(${PROJECT_NAME}_node
 ${catkin_LIBRARIES}
 ${wiringPi_LIB}
)
endif()

# INSTALL PKG
install(TARGETS ${PROJECT_NAME}_node
        RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
  PATTERN ".svn" EXCLUDE)

install(DIRECTORY config/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/config
  PATTERN ".svn" EXCLUDE)
