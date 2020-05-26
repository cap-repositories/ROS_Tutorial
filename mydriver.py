#!/usr/bin/env python  
import rospy  #todo nodo de ROS en python debe importar rospy
from sensor_msgs.msg import LaserScan  #importa los tipos de mensaje
from geometry_msgs.msg import Twist
# le indicamos a rospy el nombre del nodo.
rospy.init_node('evadir1')  #con este nombre se registra en el rosmaster

#Creamos un objeto para publicar en el topic /cmd_vel, Twist es el tipo de mensaje
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) 

#rospy.rate() ndica la frecuencia en Hz con la que se va a repetir el loop de control.
rate = rospy.Rate(2)

#crea un objeto para guardar el mensaje de tipo Twist
vel = Twist()

#Se da un valor inicial a la velocidad del robot y la distancia del sensor
vel.linear.x = 0.3
vel.angular.z = 0
d = 0.1

#publica a velocidad (se envia al robot)
pub.publish(vel)

#creamos la funcion que haga girar el robot cuando detecte un objeto
def turn(msg): #el unico argumento es el arreglo de lecturas del laser
    d = msg.ranges[0] #optiene la lectura de laser en la primera posicion del arreglo
    # d es la distancia detectada por el laser junto en frente del robot en m
    if d < 0.7:  #se hay un bjeto muy cerca, gira
        vel.angular.z = 0.5
        vel.linear.x = 0
    else:  #si no, avanza
        vel.linear.x = 0.3
        vel.angular.z = 0
    pub.publish(vel) #actualiza la velocidad en el robot
"""
se crea una suscripcion al topic /scan (medidor laser de 360 grados.
el segundo argumento es el tipo de mensaje LaserScan (se importo)
el tercer argumento es la funcion que atiende el mensaje recibido "callback"
"""

rospy.Subscriber("/scan", LaserScan, turn)

#inicia la ejecucion periodica cada 0.5s segun se indique en rospy.rate
rospy.spin()
