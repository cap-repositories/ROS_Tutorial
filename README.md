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

## Iteraccion entre nodos
Conceptos basicos de la comunicacion en ROS:

* Nodos (node): un nodo es un ejecutable que utiliza ROS para comunicarse con otros nodos.
* Mensajes (messages): tipo de datos en ROS utilizado al suscribirse o publicar en un tema.
* Temas (topic): los nodos pueden publicar mensajes en un tema, así como suscribirse a un tema para recibir mensajes.
* Maestro (master): servicio encargado del registro de nombres en ROS (es decir, ayuda a los nodos a encontrarse)
* rosout: equivalente ROS de stdout / stderr (funciones de terminal de linux)
* roscore: Master + rosout + servidor de parámetros (el servidor de parámetros se presentará más adelante)

### Nodos
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

### Comunicacion por medio de topics
ROS permite dos tipos de comunicaciones entre nodos, *Topics* y *Services*, vamos a enfocarnos primero en los topics, los servicios los estudiatemos a continuacion.

Los *Topics* permiten una comunicacion tipo PUB/SUB (publicacion - suscripcion) en la cual un nodo crea un tema (topic) y otros nodos se suscriben a el, cada que el nodo creador publique un mensaje en el topic, todos los nodos suscritos pueden leerlo.



