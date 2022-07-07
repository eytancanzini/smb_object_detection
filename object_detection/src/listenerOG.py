import rospy
from object_detection_msgs.msg import ObjectDetectionInfoArray
from tf import TransformListener
import numpy

class myNode:
    # def __init__(self, *args):
    #     self.tf_listener = TransformListener()

    # def example_function(self, cameraPoint):
    #     if self.tf_listener.frameExists("/map") and self.tf_listener.frameExists(self.frameID):

            

    #         TF = self.tf_listener.asMatrix('/map', self.hdr)
    #         CPt = numpy.asarray([cameraPoint.x,cameraPoint.y,cameraPoint.z]).T
    #         cameraPoint = numpy.matmul(TF, CPt)
    #         rospy.loginfo(' --- MEH: Check camera PT --- ')
    #         return cameraPoint
    #     else:
    #         rospy.loginfo(' --- Error: Unable to transform --- ')

    def callback(self, data):
    
        for x in range(len(data.info)): 
            # transformation related
            self.header = data.header

            # object related
            obj = data.info[x]
            ID = obj.id 
            classID = obj.class_id
            cameraPoint = obj.position
            # worldPoint = self.example_function(cameraPoint)
            worldPoint = cameraPoint
            # positionX = worldPoint[0]
            # positionY = worldPoint[1]
            # positionZ = worldPoint[2]
            rospy.loginfo(f'{self.header.frame_id}')                        
   
    def listener(self):

        
        rospy.init_node('listener', anonymous=True)

        rospy.Subscriber('/object_detector/detection_info', ObjectDetectionInfoArray, self.callback)
        rospy.spin()

if __name__ == '__main__':
    node = myNode()
    rospy.loginfo("[listener Node] OBJ Detection Listener has started")
    node.listener()