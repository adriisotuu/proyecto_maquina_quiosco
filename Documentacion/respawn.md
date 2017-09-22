
# _Respawn_ de los servicios en sistemas _Unix_

## El fichero _/etc/inittab_

Antes de la llegada de _systemd_, el _PID_ 1 de _Linux_ y _Unix_ era el proceso _Init_. Este proceso se encargaba de la activación de otros servicios en el sistema.

Al iniciar el sistema o cambiar los niveles de ejecución con el comando _init_ o _shutdown_, el daemon _init_ iniciaba los procesos mediante la lectura de la información del fichero _/etc/inittab_. Este archivo definía los siguientes puntos importantes para el proceso _init_:

* Que el proceso _init_ se tenía que reiniciar.

* Qué procesos se debían iniciar, supervisar o reiniciar si se terminaban.

* Qué acciones se debían realizar cuando el sistema ingresaba a un nuevo nivel de ejecución.

Cada entrada en el fichero _/etc/inittab_ tenía los siguientes campos:

`id:rstate:action:process`


### Descripción de los campos de _/etc/inittab_

| Campo | Descripción |
| :---: | ----------- |
| _id_ | Es un identificador único para la entrada. |
| _rstate_ | Muestra los niveles de ejecución a los que se le aplica esta entrada. |
| _action_ | Identifica el modo en que el proceso que está especificado en el campo del proceso se ejecutará. Los valores posibles incluyen: _sysinit_, _boot_, _bootwait_, _wait_ y _respawn_. |
| _process_ | Define el comando o la secuencia de comandos a ejecutar. |


## ¿Cómo restaurar (_respawn_) procesos en _Linux_ con _init_?

El comando _respawn_ básicamente servía para restaurar procesos en _Linux_. Imaginemos que queremos tener un proceso que se esté ejecutando siempre en nuestro sistema, pero como todos sabemos, a veces ese proceso muere o es eliminado. Con _respawn_, ese proceso se volverá a ejecutar y será monitorizado para que siempre exista una instancia del mismo en ejecución.

Como he comentado anteriormente, estos procesos a restaurar eran especificados en el fichero _/etc/inittab_. Un ejemplo sería:

`prueba:234:respawn:/bin/mplayer.sh`

Con este ejemplo siempre tendríamos una instancia del proceso _mplayer.sh_ (porque _respawn_ se encargaría de reiniciarlo si se apagara) identificado en _/etc/inittab_ por el nombre "prueba", que se encuentra en el directorio _/bin/_, en los niveles de ejecución 2, 3 y 4.


## _Respawn_ de los procesos en _Linux_ con _systemd_

_systemd_ no utiliza el fichero _/etc/inittab_. Simplemente tenemos que añadir en el fichero de la unidad de servicio la directiva _Restart=_ y, opcionalmente, _RestartSec=_. Estas directivas se encuentran explicadas con mayor detalle en este [apartado](https://github.com/).


### Ejemplo de un servicio _respawn_ (_mplayer.service_)

```
[Unit]
Description=mplayer streaming con respawn automático
#Documentation=
After=network.target

[Service]
Type=simple
ExecStart=/bin/mplayer.sh
ExecStop=/usr/bin/kill -TERM $MAINPID
Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

