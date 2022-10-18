#!/usr/bin/env python3
import csv, sys
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler

rospy.init_node('init_pos')
pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 10)
rospy.sleep(3)
checkpoint = PoseWithCovarianceStamped()
filename = 'dataset.csv'
with open(filename, 'r') as f:
    reader = csv.reader(f)
    try:
        #print ("test:",reader[0])
        #for line in reader.readlines()
        for row in reader:
            if row[1]== "tmp/0.jpeg":
                x= float(row[2])
                y=float(row[3])
                z=float(row[4])
                x_o = float(row[5])
                y_o=float(row[6])
                z_o=float(row[7])
                w_o=float(row[8])
                print ("x=", x)
                print("y=", y)
                print("z=", z)
                print("x_o= ", x_o)
                print("y_o=",y_o)
                print("z_o=",z_o)
                print("w_o=",w_o)
                print(type(x_o))

                checkpoint.pose.pose.position.x = x
                checkpoint.pose.pose.position.y = y
                checkpoint.pose.pose.position.z = z

                #[x_o,y_o,z_o,w_o]=quaternion_from_euler(0,0,0,0)
                checkpoint.pose.pose.orientation.x = x_o
                checkpoint.pose.pose.orientation.y = y_o
                checkpoint.pose.pose.orientation.z = z_o
                checkpoint.pose.pose.orientation.w = w_o

                print (checkpoint)
                pub.publish(checkpoint)

    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))