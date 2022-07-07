#!/usr/bin/env python 
import rospy
import csv
from object_detection_msgs.msg import ObjectDetectionInfoArray
from tf2_geometry_msgs import do_transform_point
import tf2_ros
import rospy
import tf2_ros
import tf2_geometry_msgs

WORLD_FRAME = 'map'
CAMERA_FRAME = 'base_link'
# CAMERA_FRAME = 'base_link'

class myNode:

    def getObjectsCF(self,data):
        '''
            - This takes data from listener
            - Extracts objects from listener topic
        '''

        ObjectsArray = []

        for x in range(len(data.info)): 
            
            # object related
            obj = data.info[x]
            ID = obj.id 
            className = obj.class_id
            confidence = obj.confidence
            
            # Create Point Stamped Message for use with transform function ...
            point_camera = tf2_geometry_msgs.PointStamped()
            # point_camera.header.frame_id = data.header.frame_id
            point_camera.header.frame_id = CAMERA_FRAME

            # DEBUG
            point_camera.header.stamp = data.header.stamp
            # point_camera.header.stamp = rospy.Time.now()

            point_camera.point = obj.position

            ObjectsArray.append([ID, className, point_camera, confidence])
           
        
        return ObjectsArray
    
    def getObjectsWF(self, data):

        '''
            - This takes data as a array of form [ id , class name , pointStamped ]
            - converts the points from Camera to World
        '''

        ObjectsArray = []

        # WRITE TO CSV
        # create the csv writer
        f = open('/home/team8/catkin_ws/output_detections.csv', 'a')    
        self.writer = csv.writer(f)

        for x in range(len(data)): 
            
            # object related
            obj = data[x]

            ID          = obj[0] 
            className   = obj[1]
            pointCF     = obj[2]
            confidence  = obj[3]

            # pointWF = self.tf_buffer.transform(pointCF, WORLD_FRAME, rospy.Duration(1.0))
            transform = self.tf_buffer.lookup_transform(WORLD_FRAME, CAMERA_FRAME, rospy.Time(0) , rospy.Duration(2.0))
            pointWF = do_transform_point(pointCF, transform)

            # uncomment to write to csv
            row = [pointWF.point.x, pointWF.point.y, pointWF.point.z, className, confidence]
            self.writer.writerow(row)

            ObjectsArray.append([ID, className, pointWF, confidence])   
        # close csv file
        f.close()
        return ObjectsArray

    @staticmethod
    def valCheck(dataWF, dataCF):
        wx = dataWF[2].point.x
        wy = dataWF[2].point.y
        wz = dataWF[2].point.z

        cx = dataCF[2].point.x
        cy = dataCF[2].point.y
        cz = dataCF[2].point.z

        rospy.loginfo(f'C : {cx} , {cy} , {cz}' )
        rospy.loginfo(f'W : {wx} , {wy} , {wz}' )

        rospy.loginfo( ' -- val check finished -- ')
        



    def callback(self, data):

        self.tf_buffer = tf2_ros.Buffer()
        tf2_ros.TransformListener(self.tf_buffer)

        # Give the listener some time to accumulate transforms...
        rospy.sleep(0.5)

        rospy.loginfo(f'len of the objects deteceted {len(data.info)}')

        objectsCF = self.getObjectsCF(data);
        rospy.loginfo(' -- EXTRACTION : OK -- ')

        # objectsWF = self.getObjectsWF(objectsCF);
        # rospy.loginfo(' -- conversion CF to WF : OK -- ')
        

        # Now transform the point into the /odom frame...
        try:
            
            objectsWF = self.getObjectsWF(objectsCF);
            rospy.loginfo(' -- conversion CF to WF : OK -- ')
            
            # check for debugging
            # self.valCheck(objectsWF[0], objectsCF[0]);

        except tf2_ros.TransformException as e:
            rospy.loginfo(type(e))
            rospy.loginfo("-- conversion CF to WF : FAILED --")
                                      
   
    def listener(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber('/object_detector/detection_info', ObjectDetectionInfoArray, self.callback)
        rospy.spin()

if __name__ == '__main__':
    node = myNode()
    rospy.loginfo("[listener Node] OBJ Detection Listener has started")
    node.listener()





 


