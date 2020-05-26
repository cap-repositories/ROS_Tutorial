# Tutorial ROS - Robotica - PUJC

Bienvenido al tutorial de ROS para el curso de robotica en la Pontificia Universidad Javeriana, para iniciar debe crear una cuenta en https://www.theconstructsim.com/rds-ros-development-studio/ y abrir un nuevo Rosject (project) con la configuracion basica.
Abrimos una nueva terminal en la pestaña Tools.

## Configurar el Workspace 

Cada aplicaion de ROS debe ejecutarse en su propio workspace para evitar conflictos entre versiones u otros proyectos.
Cuando abrimos el proyecto de ROS en el ROS Development Studio, un workspace de catkin esta preconfigurado y solo debemos verificar que este bien establecido.
En la terminal escribimos:
```
$ ls
```
Aparece la lista de carpetas y archivos, debe aparecer una carpera catkin_ws, entramos a ella con:
```
$ cd catkin_ws
$ ls
```
aparece la lista de carpetas que deben incluir:
* build
* devel
* src

Si estas carpetas no aparecen, se debe correr el comando ``` catkin_make ``` para crear el workspace.

Adicional se debe executar (source) el archivo devel/setup.bash para que el workspace quede activo y aplique los cambios.
```
$ source devel/setup.bash
```
Finalmente, verificamos que nuestro workspace apunte a la instalacion de ROS con el siguiente comando:
```
$ echo $ROS_PACKAGE_PATH
/home/user/catkin_ws/src:/home/user/simulation_ws/src:/home/simulations/public_sim_ws/src:/opt/ros/kinetic/share
```

## Actividad 1: Navegar por el sistema de archivos ROS


Los paquetes son la unidad de organización principales de ROS. Cada paquete puede contener bibliotecas, ejecutables, scripts u otros elementos. Los paquetes estan asociados a un manifiesto (package.xml) el cual contiene descripción del paquete y sirve para definir dependencias entre paquetes y para capturar metainformación sobre el paquete como versión, mantenedor, licencia, etc.

En un proyecto complejo se pueden usar muchos paquetes lo que hace que navegar usando comandos de consola como ```cd``` o ```ls``` sea muy dificil. Por esta razon, ROS tiene su propio sistema de navegacion basado en comandos pero enfocado a encontrar paquetes sin tener que conocer o especificar la ruta.

Intente los siguientes comando:
```
$ rospack find rospy
$ roscd roscpp
$ rosls rospy

```

El primer comando rospack find devuelve la ruta del paquete solo con su nombre.
El comando roscd permite entrar al directorio (carpeta) del paquete solo por su nombre. Tambien funciona con subcarpetas.
El comando rosls devuelve la lista de carpetas y archivos que contiene un paquete.

los paquete roscpp y rospy permiten correr funciones de ROS desde c++ y python respectivamente, se veran mas adelante.

cierre la terminal y abra una nueva para el siguiente paso.

## Autocompletado por medio de TAP
una funcion muy util de ROS para hacer mas rapido el uso de la terminal de comandos, es el autocompletado por medio de la tecla Tab, con esto, solo es encesario escribir las primeras letras de cada nombre y presionar Tab para que se complete el resto o se muestren las opciones cuando hay mas de una.

En la nueva terminal escriba los siguiente pero presionando Tab dos veces al final.
```
$ rosls rosc
```
Vera que se muestran todos los paquetes que empiezan por ```rosc```, ahora escriba lo siguente y presiones una vez Tab.
```
$ rosls roscpp_s
```
Vera que se completa ```rosls roscpp_serialization``` que es la unica opcion para completar.

De esta forma se pueden completar complicadas rutas de archivos para ejecutar los comandos correspondiente.

##Crear un paquete propio
Ahora veremos como crear nuestro propio paquete donde pondremos algo de codigo para nuestra aplicacion.

lo primero es ir al directorio src:
```
$ cd ~/catkin_ws/src
```

Ahora usamos la funcion catkin_create_pkg para crear una nuevo paquete, la sintaxis de la funciones es la siguiente:
```
# catkin_create_pkg <nombre> [depend1] [depend2] [depend3]
```
(lo anterior es un ejemplo, no intentes correrlo en la terminal)

las dependencias son otros paquetes que nuestro paquete va a usar.

pruebe crear un paquete llamado rospuj con rospy como dependencia.

### aplicar cambios al workspace
cadaque se realiza un cambio en el paquete(o se crea un paquete) es necesario ejecutar los siguietnes comandos para que estos cambios sean tenidos en cuenta en la ejecucion del paquete. Esto es debido a que ROS no leer directamente los archivos sino que editamos sino sus correspondientes ejecutables.
```
$ cd ~/catkin_ws
$ catkin_make
$ . ~/catkin_ws/devel/setup.bash
$ source /opt/ros/kinetic/setup.bash  
```

## Nodos
Conceptos basicos de la comunicacion en ROS:

* Nodos (node): un nodo es un ejecutable que utiliza ROS para comunicarse con otros nodos.
* Mensajes (messages): tipo de datos en ROS utilizado al suscribirse o publicar en un tema.
* Temas (topic): los nodos pueden publicar mensajes en un tema, así como suscribirse a un tema para recibir mensajes.
* Maestro (master): servicio encargado del registro de nombres en ROS (es decir, ayuda a los nodos a encontrarse)
* rosout: equivalente ROS de stdout / stderr (funciones de terminal de linux)
* roscore: Master + rosout + servidor de parámetros (el servidor de parámetros se presentará más adelante)

Un nodo es un archivo ejecutable dentro de un paquete ROS. Los nodos ROS utilizan **rospy** o **roscpp** para comunicarse con otros nodos. Los nodos pueden publicar o suscribirse a un tema. Los nodos también pueden proporcionar o usar un Servicio.

### roscore
Para utilizar la infraestructura de comunicacion de ROS es necesario que roscore este ejecutandose, esto implica tener una terminal dedicada donde se ejecuta el siguiente comando:
```
$ roscore
```
Esta terminal no se debe cerrar por lo que debe abrir otras terminales para ejecutar otros comandos.

### rosnode
Rosnode es una funcion de ROS que permite obtener informacion de los nodos que estan registrados en rosmaster. Roscore debe estar corriendo para poder usar rosnode.

veamos que puede hacer rosnode, ejecuta en una nueva terminal:

```
rosnode list
```
esto devuelve todos los nodos que esten corriendo, en nuestro caso solo deberia mostrar ```/rosout``` que es un nodo que siempre se esta ejecutando para manejar la comunicacion.

Otro comando es *rosnode info* el cual responde con la informacion del nodo solicitado. esta informacion debe ser escrita por el desarrollador.

ejecute:
```
rosnode info /rosout
```

ahora veremos como activar mas nodos manualmente, pero primero vamos a iniciar la simulacion de un robot para analizar la comunicacion entre nodos.

Siga los siguientes pasos:
1. En el ROS DE abra la pestaña *Simulations*
2. En la opcion "world" seleccione "Empty + Wall"
3. En la opcion "robot" seleccione "Rosbot"
4. De click en "Start Simulation"

la simulacion puede tardar varios segundos o minutos en iniciar. Una ves cargado todo el ambiente de simulacion, ejecute nuevamente ```rosnode list``` para ver todos los nodos que ahora se estan ejecutando.
Aparecen los siguentes nodos.
```
/gazebo
/gmapping_node
/joint_state_controller_spawner
/move_base
/robot_state_publisher
/rosout
/rviz
```
Estos nodos iniciaron automaticamente, pero otros nodos se pueden inciar desde la terminal usando ```rosrun```, veremos mas adelante como usar este comando con los nodos que creamos.

## Comunicacion por medio de topics
ROS permite dos tipos de comunicaciones entre nodos, *Topics* y *Services*, vamos a enfocarnos primero en los topics, los servicios los estudiatemos a continuacion.

Los *Topics* permiten una comunicacion tipo PUB/SUB (publicacion - suscripcion) en la cual un nodo crea un tema (topic) y otros nodos se suscriben a el, cada que se publique un mensaje en el topic, todos los nodos suscritos pueden leerlo.

El comando base para trabajar con *Topics* es **rostopic**. Un primer uso de este comando es la funcion de ayuda para leer otras funciones y comandos, en una nueva terminal escriba lo siguiente:
```
$ rostopic -h
```
veremos con detalle algunos de estos comandos.

### rostopic echo
```rostopic echo``` permite ver en la terminal los mensajes publicados en un tema.

Para conocer los temas que estan abiertos podemos escribir el siguiente comando:
```
$ rostopic list
```
Esto desplega una lista de los temas abiertos, ahora vamos a leer el tema */scan* el cual es usado por el robot para publicar constantemente los valores leidos por el sensor laser de 360 grados.

```
$ rostopic echo /scan
```
No te alarmes!, apareceran muchas lineas de informacion, es normal solo tienes que presionar *Ctrl + Z* para dejar de leer.

Esto nos muestra un ejemplo de un mensaje publicado constantemente en un tema. Para usar esa informacion es necesario crear una suscripcion, eso lo haremos mas adelante.

### Tipos de mensaje
los temas transmiten mesajes, un mensaje tiene una estructura de datos compleja que puede ir desde un valor unico hasta un conjunto de datos de diferentes tipos uncluidos areglos y listas.

Es necesario conocer el tipo de mensaje asociado a un tema para poder usarlo, ya sea para interpretar los datos y usarlos en una aplicacion o para poder enviar un mensaje con la estructura correcta.

Para conocer el tipo de mensaje asociado a un tema, se usa el comando ```rostopic type [topic]```. Podemos usarlo con el tema ```/scan``` asi:

```
$ rostopic type /scan
# sensor_msgs/LaserScan
```
Ahora podemos usar ```rosmsg show [message topic]``` para conocer la estructura detallada del mensaje asi:
```
$ rosmsg show sensor_msgs/LaserScan
```
Respuesta:
```
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
float32 angle_min
float32 angle_max
float32 angle_increment
float32 time_increment
float32 scan_time
float32 range_min
float32 range_max
float32[] ranges
float32[] intensities
```
Estos muestra que hay varios datos de los cuales nos puede interesar que el dato ```ranges``` es un arreglo de datos tipo float32, este dato contiene los valores leidos por el sensor desde *angle_min* a *angle_max aumentando* lo indicado en *angle_increment*.

Como otro ejemplo, podemos revisar la estructura del tema */cmd_vel*, este tema es usado para enviar mensajes de movimiento al robot.
```
$ rostopic type /cmd_vel
```
respuesta:
```
geometry_msgs/Twist
```
Ahora buscamos la estructura del mensaje:
```
$ rosmsg show geometry_msgs/Twist
```
Respuesta:
```
geometry_msgs/Vector3 linear
  float64 x
  float64 y
  float64 z
geometry_msgs/Vector3 angular
  float64 x
  float64 y
  float64 z
```
Esto corresponde a un mensaje del tipo: '[x, y, z]' '[x, y, z]' donde el primer vector es la velocidad y el segundo la rotacion.

### rostopic pub
el comando ```rostopic pub``` permite escribir un mensaje en un tema desde la terminal.

La sintaxis del comando es:
```
rostopic pub [topic] [msg_type] [args]
```
donde.
* [topic] es el nombre del tema tal como aparece al usar ```rostopic list```
* [msg_type] es el tipo de mensaje tal como aparece al usar ```rostopic type```
* [args] es el contenido del mesaje que debe tener la misma estructura mostra al usar ```rosmsg show```

ahora usemos este comando para mover el robot. en la terminal escribe:
```
rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[0.6, 0.0, 0.0]' '[0.0, 0.0, 2.0]'
```

El atributo ```-1``` indica que envia un solo mensaje y termina la comunicacion.

En el simulador podra ver como el robot inicia su movimiento donde '[0.6, 0.0, 0.0]' indica una velocidad lineal en X y '[0.0, 0.0, 2.0]' una velocidad de rotacion en Z. Ahora tome un tiempo para jugar un poco con el robot cambiando estos valores.

Ahora podemos introducir la comunicacion por servicios en ROS con un servicio que permite reiniciar la simulacion, si el robot se perdio y se estrello, intente reiniciar con alguno de estos comandos:
```
$ rosservice call /gazebo/reset_world
$ rosservice call /gazebo/reset_simulation
```


