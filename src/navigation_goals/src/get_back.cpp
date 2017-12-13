#include "ros/ros.h"
#include "std_msgs/String.h"
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <tf/transform_datatypes.h>

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  MoveBaseClient ac("move_base", true);

  //wait for the action server to come up
  while(!ac.waitForServer(ros::Duration(5.0))){
    ROS_INFO("Waiting for the move_base action server to come up");
  }

  move_base_msgs::MoveBaseGoal goal;

  //we'll send a goal to the robot to move 1 meter forward
  goal.target_pose.header.frame_id = "map";
  goal.target_pose.header.stamp = ros::Time::now();

  goal.target_pose.pose.position.x = 2.24151158333;
  goal.target_pose.pose.position.y = -2.27514123917;
  goal.target_pose.pose.position.z = 0;
  goal.target_pose.pose.orientation = tf::createQuaternionMsgFromYaw(-1.570796);

  ROS_INFO("Sending goal");
  ac.sendGoal(goal);

  ac.waitForResult();

  if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED){
    ROS_INFO("Hooray, the base moved 1 meter forward");
  }
  else
    ROS_INFO("The base failed to move forward 1 meter for some reason");
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "get_back");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("end", 1000, chatterCallback);

  ros::spin();

  return 0;
}