cmake_minimum_required(VERSION 2.8.3)
project(baxter_moveit_config)

find_package(catkin REQUIRED)

find_package(catkin REQUIRED genmsg actionlib_msgs actionlib message_generation geometry_msgs)
add_action_files(DIRECTORY action FILES baxter.action)

add_message_files(
   FILES
   
  poruka.msg
#   Message1.msg
#   Message2.msg
 )

generate_messages(DEPENDENCIES actionlib_msgs std_msgs geometry_msgs)

catkin_package(CATKIN_DEPENDS actionlib_msgs message_runtime)

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})


