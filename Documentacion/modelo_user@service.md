
# El modelo _user@.service_

_Systemd_ ofrece a los usuarios la capacidad de gestionar los servicios bajo el control del usuario con una instancia _systemd_ por usuario, permitiéndoles de este modo iniciar, detener, habilitar y deshabilitar sus propias unidades, es decir, aquellas que se encuentran dentro de ciertos directorios cuando _systemd_ se ejecuta por el usuario.

Esto es conveniente para los demonios y otros servicios que normalmente se ejecutan como un usuario diferente a _root_, como por ejemplo mpd, o para realizar tareas automatizadas como la recuperación de correo.


## ¿Cómo funciona?

Según la configuración predeterminada en _/etc/pam.d/system-login_, el módulo _pam_systemd.so_ inicia automáticamente una instancia `systemd --user` cuando el usuario inicia sesión por primera vez, iniciando _user@.service_. Este proceso sobrevivirá mientras exista una sesión para ese usuario, y se matará tan pronto como se cierre la última sesión para el usuario.

Por lo tanto, la instancia `systemd --user` es un proceso por usuario y no por sesión. Esto significa que todos los servicios de usuario se ejecutan fuera de una sesión y, como consecuencia, los programas que necesiten ser ejecutados dentro de una sesión probablemente se romperán en los servicios de usuario.

Es importante saber que `systemd --user` se ejecuta como un proceso separado del proceso `systemd --system`. Las unidades de usuario no pueden referirse o depender de las unidades del sistema.

Cuando se habilita (_enabled_) el inicio automático de las instancias de usuario, la instancia se inicia en el arranque y no se eliminará. La instancia de usuario _systemd_ es responsable de administrar servicios de usuario, que pueden ser utilizados para ejecutar demonios o tareas automatizadas, con todos los beneficios de _systemd_, como activación de _socket_, temporizadores o _timers_, sistema de dependencia o control estricto de procesos a través de _cgroups_.

Con el comando `$ systemctl --user status` podemos asegurarnos de que la instancia de usuario se ha iniciado correctamente.

Las unidades de usuario se encuentran en los siguientes directorios (ordenados por precedencia ascendente):

1. _/usr/lib/systemd/user/_ donde pertenecen las unidades provistas por paquetes instalados.

2. _~/.local/share/systemd/user/_ donde pertenecen las unidades de paquetes que se han instalado en el directorio _/home/_ del usuario.

3. _/etc/systemd/user/_ donde el administrador del sistema coloca las unidades de usuario de todo el sistema (_system-wide_).

4. _~/.config/systemd/user/_ donde el usuario pone sus propias unidades.


## La unidad _user@.service_

```
[Unit]
Description=User Manager for UID %i
After=systemd-user-sessions.service

[Service]
User=%i
PAMName=systemd-user
Type=notify
ExecStart=-/usr/lib/systemd/systemd --user
Slice=user-%i.slice
KillMode=mixed
Delegate=yes
TasksMax=infinity
TimeoutStopSec=120s
```


## Configuración básica

Como he mencionado anteriormente, todos los servicios del usuario se colocarán en _~/.config/systemd/user/_. Para ejecutar servicios en el primer inicio de sesión, ejecutamos `systemctl --user enable servicio` para cualquier servicio que queramos iniciar de forma automática.


### Variables de entorno

La instancia de usuario de _systemd_ no hereda ninguna de las variables de entorno establecidas en lugares como _.bashrc_, etc. Hay varias maneras de establecer variables de entorno para la instancia de usuario _systemd_:

1. Para usuarios con un directorio `$HOME`, utilizamos la opción _DefaultEnvironment_ en _~/.config/systemd/user.conf_. Afecta sólo a la unidad de usuario de ese usuario.

2. Con la opción _DefaultEnvironment_ en el fichero _/etc/systemd/user.conf_. Afecta a todas las unidades de usuario.

3. Agregando un fichero de configuración _drop-in_ en _/etc/systemd/system/user@.service.d/_. Afecta a todas las unidades de usuario.
	
4. En cualquier momento, utilizar `systemctl --user set-environment` o `systemctl --user import-environment`. Afecta a todas las unidades de usuario iniciadas después de establecer las variables de entorno, pero no las unidades que ya estaban en ejecución.

Después de la configuración, se puede utilizar el comando `systemctl --user show-environment` para verificar que los valores son correctos.


#### Ejemplo de servicio

Creamos el directorio _/etc/systemd/system/user@.service.d/_ y en su interior generamos un fichero llamado _local.conf_:

```
[Service]
Environment="PATH=/usr/lib/ccache/bin:/usr/local/bin:/usr/bin:/bin"
Environment="EDITOR=nano -c"
Environment="BROWSER=firefox"
Environment="NO_AT_BRIDGE=1"
```


#### _DISPLAY_ y _XAUTHORITY_

_DISPLAY_ es utilizado por cualquier aplicación _X_ para saber qué pantalla utilizar y _XAUTHORITY_ para proporcionar una ruta al fichero _.Xauthority_ del usuario y, por tanto, la _cookie_ necesaria para acceder al servidor _X_.

Si queremos lanzar aplicaciones _X_ desde unidades _systemd_, estas variables deben establecerse. _Systemd_ proporciona un script en _/etc/X11/xinit/xinitrc.d/50-systemd-user.sh_ para importar esas variables en la sesión de usuario _systemd_ en el lanzamiento de _X_. Por lo tanto, a menos que iniciemos _X_ de un modo no estándar, los servicios de usuario deben tener en cuenta el _DISPLAY_ y _XAUTHORITY_.

`systemctl --user import-environment DISPLAY XAUTHORITY`


#### _PATH_

Si personalizamos nuestro _PATH_ y queremos lanzar aplicaciones que lo utilizan desde unidades _systemd_, deberíamos asegurarnos de que el _PATH_ modificado está configurado en el entorno _systemd_. Suponiendo que hemos establecido el _PATH_ en _.bash\_profile_, la mejor forma para que _systemd_ tenga conocimiento del _PATH_ modificado es añadiendo lo siguiente a _~/.bash\_profile_ después de que hayamos establecido la variable _PATH_:

`systemctl --user import-environment PATH`

Esto no afectará a los servicios _systemd_ iniciados antes de que se genere _~/.bash\_profile_.


### Inicio automático de instancias de usuario _systemd_

Sabemos que la instancia de usuario _systemd_ se inicia después del primer inicio de sesión de un usuario y se cancela después de que se cierre la última sesión del usuario. A veces puede sernos útil iniciarla justo después del arranque y mantenerla ejecutándose después de cerrar la última sesión, por ejemplo para que se ejecute algún proceso de usuario sin ninguna sesión abierta. Para conseguir esto usaremos el siguiente comando:

`# loginctl enable-linger username`


## Ejemplo de servicio de usuario

```
~/.config/systemd/user/mplayer.service

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

Iniciar el servicio: `$ systemctl --user start mplayer.service`

Detener el servicio: `$ systemctl --user stop mplayer.service`

Habilitar el servicio: `$ systemctl --user enable mplayer.service`

