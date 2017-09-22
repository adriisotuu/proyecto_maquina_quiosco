
# Análisis del arranque y apagado del sistema con _systemd_

## Inicio del sistema

En el arranque del sistema intervienen varios componentes distintos. Inmediatamente después de encender el ordenador, la _BIOS_ del sistema lleva a cabo una inicialización mínima del _hardware_. A continuación, el _boot loader_ invoca el _kernel_ del S.O. desde el disco (o la red) y, este, extrae y ejecuta una imagen de disco _RAM_ inicial (_initrd_).

Después de que el sistema de ficheros raíz se encuentra y se monta, _initrd_ entrega el control a _systemd_, almacenado en la imagen del sistema operativo, y se encarga de probar todo el _hardware_ restante, montar todos los sistemas de ficheros necesarios e iniciar todos los servicios configurados.


### Funcionamiento de _systemd_ en el arranque

El administrador del sistema es el responsable de inicializar los sistemas de ficheros, servicios y controladores necesarios para el correcto funcionamiento del sistema. Este proceso, altamente paralelizado, se divide en varios pasos que están expuestos como unidades _.target_.

Cuando _systemd_ inicie el sistema, activará todas las unidades que son dependencias de _default.target_ (así como recursivamente todas las dependencias de estas dependencias). Por lo general, _default.target_ es simplemente un alias de _graphical.target_ o _multi-user.target_.

![arranque_sistema](/Imagenes/inicio.png "systemd en el arranque del sistema")

La tabla anterior es una descripción estructural de los _targets_ y su posición en la lógica de arranque. Las flechas describen qué unidades se extraen y se ordenan antes de qué otras unidades.


### Descripción de los _targets_

| _Target_ | Descripción |
| :------: | ----------- |
| _local-fs-pre.target_ | Este _target_ se ordena automáticamente antes de todos los puntos de montaje locales marcados con _auto_. Se puede utilizar para ejecutar ciertas unidades antes de todas las monturas locales. |
| _local-fs.target_ | _systemd-fstab-generator_ agrega automáticamente dependencias de tipo _Before=_ a todas las unidades de montaje que se refieren a puntos de montaje locales para este _target_. Además, agrega dependencias de tipo _Wants=_ a esta unidad _.target_ para aquellos montajes enumerados en _/etc/fstab_ que tienen el conjunto de opciones de montaje automático. |
| _swap.target_ | Similar a _local-fs.target_, pero para particiones _swap_ y ficheros _swap_. |
| _cryptsetup.target_ | Agrupa servicios de configuración para todos los dispositivos de bloque cifrados. |
| _sysinit.target_ | _systemd_ agrega automáticamente dependencias de los tipos _Requires=_ y _After=_ para este _target_ a todos los servicios (excepto para aquellos con _DefaultDependencies=no_). Este _target_ extrae los servicios necesarios para la inicialización del sistema. Estos servicios deben configurarse con _DefaultDependencies=no_ y especificar todas sus dependencias manualmente. |
| _timers.target_ | Configura todas las unidades de temporizador (_.timer_) que deben estar activas después del arranque del sistema. |
| _paths.target_ | Configura todas las unidades de ruta (_.path_) que deben estar activas después del arranque. |
| _sockets.target_ | Configura todas las unidades _.socket_ que tienen que estar activas después del arranque. |
| _basic.target_ | Cubre el arranque básico. _systemd_ agrega automáticamente la dependencia del tipo _After=_ para esta unidad _.target_ a todos los servicios (excepto para aquellos con _DefaultDependencies=no_). |
| _multi-user.target_ | Consiste en un sistema multiusuario, no gráfico. De esta unidad depende _graphical.target_. |
| _graphical.target_ | Consiste en una pantalla de inicio de sesión gráfica, es decir, un sistema multiusuario gráfico. Depende de _multi-user.target_. |
| _rescue.target_ | Extrae el sistema base (incluyendo los montajes del sistema) y genera un _shell_ de rescate. Aislamos este _target_ con el fin de administrar el sistema en modo de usuario único con todos los sistemas de ficheros montados, pero sin servicios en ejecución, excepto los más básicos. |
| _emergency.target_ | Inicia un _shell_ de emergencia en la consola principal. No extrae ningún servicio o montaje. Es la versión más mínima de arrancar el sistema para adquirir un _shell_ interactivo; los únicos procesos en ejecución normalmente son sólo el gestor del sistema (_PID_ 1) y el proceso _shell_. También se utiliza cuando falla una comprobación del sistema de ficheros en un sistema de ficheros requerido y el arranque no puede continuar. |


## Apagado del sistema

En el apagado, _systemd_ detiene todos los servicios, desmonta todos los sistemas de ficheros y luego (opcionalmente) salta de nuevo al código _initrd_ que desmonta/desacopla el sistema de ficheros raíz y el almacenamiento en el que reside. Como último paso, el sistema se apaga.


### Funcionamiento de _systemd_ en el apagado

Del mismo modo que sucede en el arranque, consiste en varias unidades _.target_ con una mínima estructura de orden aplicada:

![apagado_sistema](/Imagenes/apagado.png "systemd en el apagado del sistema")


### Descripción de los _targets_

| _Target_ | Descripción |
| :------: | ----------- |
| _shutdown.target_ | Termina los servicios en el apagado del sistema. Los servicios que se terminen en el apagado deben añadir las dependencias _Conflicts=_ y _Before=_ a esta unidad para su unidad de servicio, lo que se hace implícitamente cuando se establece _DefaultDependencies=yes_ (el valor por defecto). |
| _umount.target_ | Desmonta todos los puntos de montaje y de montaje automático en el apagado del sistema. Los puntos de montaje que se desmontarán al cerrar el sistema agregarán dependencias _Conflicts=_ a esta unidad para su unidad _.mount_ (_DefaultDependencies=yes_). |
| _final.target_ | Se utiliza durante la lógica de apagado y se puede utilizar para extraer los servicios finales después de que todos los servicios normales ya estén terminados y todos los puntos de montaje desmontados. |
| _reboot.target_ | Se utiliza para apagar y reiniciar el sistema. |
| _poweroff.target_ | Cierra y apaga el sistema. |
| _halt.target_ | Unidad _.target_ que sirve para detener el sistema. |

