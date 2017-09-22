
# _systemd_

## ¿Qué es _systemd_?

Es un gestor del sistema y de los servicios para _Linux_ que se ejecuta como _PID_ 1 e inicia el resto del sistema. Soporta scripts de inicio _SysV_ y _LSB_, y funciona como un reemplazo para _sysvinit_.


### Características

* Ofrece una notable capacidad de paralelización usando _sockets_. Para acelerar el arranque completo del sistema e iniciar un mayor número de procesos en paralelo, _systemd_ en un primer paso crea los _sockets_ de escucha para todos los demonios en el sistema de inicio y, posteriormente, ejecuta e inicia a la vez todos los demonios.

* Utiliza la activación de _socket_ y _D-Bus_ para iniciar los servicios.

* Permite el inicio de los demonios bajo demanda.

* Realiza un seguimiento de los procesos utilizando los grupos de control de _Linux_, los cuales permiten agrupar los procesos en jerarquías.

* Mantiene los puntos de montaje y servicios de montaje automático.

* Implementa un elaborado sistema de gestión de dependencias entre las unidades.


## El cambio a _systemd_

Por muchos años, el _PID_ 1 de _Linux_ y _Unix_ ha sido el proceso _Init_. Este proceso era el responsable de la activación de otros servicios en el sistema. Normalmente, los demonios eran iniciados en el arranque por _System V_ y por los _scripts_ de _Init_. Menos frecuentes eran los demonios iniciados bajo demanda por otro servicio, como con _Inetd_ o _Xinetd_.

Por lo tanto, podemos decir que _systemd_ ha sido creado para ofrecer un inicio más rápido y flexible que _SysV_, permitiendo el arranque paralelo de servicios.

Algunas de las mejoras que ofrece son:

* El conjunto de características citadas en el apartado anterior.

* Se ha mejorado la velocidad de inicialización del sistema.

* Es modular, esto quiere decir que varios servicios pueden ser administrados de forma conjunta.

* Ha dejado de utilizar el fichero _/etc/inittab_.

