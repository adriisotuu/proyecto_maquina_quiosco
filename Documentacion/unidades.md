
# ¿Qué son las _units_ o unidades?

_systemd_ se basa en la noción de unidades, compuestas de un nombre y una extensión que indica de qué tipo de unidad se trata. Cada unidad tiene su correspondiente fichero de configuración cuyo nombre es idéntico. Un ejemplo sería el servicio _httpd.service_ cuyo fichero de configuración sería _/usr/lib/systemd/system/httpd.service_.

Los archivos de configuración de las unidades se cargan desde dos ubicaciones. De menor a mayor precedencia son:

* _/usr/lib/systemd/system/_: unidades proporcionadas por paquetes instalados.

* _/etc/systemd/system/_: unidades instaladas por el administrador del sistema.


## Tipos de unidades

| Tipo | Descripción |
| :---: | ----------- |
| _.service_ | Describe cómo administrar un servicio o una aplicación en el servidor. Esto incluirá cómo iniciar, detener, reiniciar o recargar el servicio, en qué circunstancias debe iniciarse automáticamente, así como información de dependencia con otras unidades. |
| _.socket_ | Las unidades _socket_ son IPC (_sockets UNIX_), _sockets_ de red o _FIFO_. Esta unidad se utiliza para la activación basada en _socket_, es decir, cuando el socket recibe información, ejecuta un servicio. Debe haber un servicio con el mismo nombre o especificado por la directiva _Service =_. |
| _.target_ | Utilizada para la agrupación lógica de unidades. Hace referencia a otras unidades, que pueden ser controladas conjuntamente. También se pueden utilizar para llevar al sistema a un nuevo estado. |
| _.slice_ | Consiste en un conjunto jerárquico de _units_ organizadas para manejar un grupo de procesos del sistema. |
| _.mount_ | Contiene información sobre un punto de montaje del sistema de archivos controlado por _systemd_.
| _.automount_ | Configura un punto de montaje que se montará automáticamente. Éstos deben tener el nombre del punto de montaje al que se refieren y una unidad _.mount_ correspondiente para definir las especificaciones del montaje. |
| _.device_ | Contiene información de una unidad de dispositivo que requiere una gestión de _systemd_. No todos los dispositivos del sistema requieren una unidad de dispositivo _systemd_, solo aquellos marcados con la etiqueta _udev systemd_. |
| _.swap_ | Esta unidad describe el espacio de intercambio en el sistema. |
| _.path_ | Define una ruta o _path_ controlada por _systemd_. De forma predeterminada, se iniciará una unidad _.service_ del mismo nombre base que la unidad _.path_ cuando el estado de ésta cambie. |
| _.timer_ | Sirve para definir un temporizador que será administrado por _systemd_, similar a un trabajo _cron_ para la activación retardada o programada. |
| _.snapshot_ | Una unidad _.snapshot_ es creada automáticamente por el comando `systemctl snapshot`. Nos permite reconstruir el estado actual del sistema después de realizar cambios. Las instantáneas no sobreviven a través de las sesiones y se utilizan para revertir los estados temporales. |
| _.scope_ | Son creadas automáticamente por _systemd_ y se encargan de administrar conjuntos de procesos del sistema. Su objetivo es organizar y gestionar recursos para los procesos. A diferencia de las otras unidades, no están configuradas por ficheros de unidad. |


### Tipos de unidades _.service_

Existen distintos tipos de inicio a considerar cuando se escribe un archivo de servicio personalizado. Esto se configura con el parámetro _Type=_ en la sección _[Service]_:

| Tipo | Descripción |
| :---: | ----------- |
| _Type=simple_ (por defecto) | _systemd_ consedira que el servicio se iniciará de inmediato. El proceso iniciado con _ExecStart=_ es el proceso principal del servicio. |
| _Type=forking_ | El servicio se inicia una vez que el proceso se ha bifurcado (_fork_) y el proceso padre ha salido. El proceso iniciado con _ExecStart=_ genera un proceso hijo que se convierte en el proceso principal del servicio. Debemos especificar _PIDFile=_ para que _systemd_ pueda realizar un seguimiento del proceso principal. |
| _Type=oneshot_ | Este tipo es útil para _scripts_ que realizan un solo trabajo y luego salen. Podemos configurar _RemainAfterExit=yes_ para que _systemd_ todavía considere el servicio como activo después de que el proceso haya salido. |
| _Type=notify_ | Idéntico a _Type=simple_. En este caso, el _daemon_ enviará una señal a _systemd_ cuando esté listo, es decir, cuando haya terminado de iniciarse. |
| _Type=dbus_ | El servicio se considera listo cuando el _BusName=_ especificado aparece en el bus de sistema _DBus_. _D-Bus_ (_Desktop Bus_) es un sistema de comunicación entre procesos (_IPC_) para aplicaciones de software con el fin de comunicarse entre sí. |
| _Type=idle_ | _systemd_ retrasará el inicio del servicio hasta que se completen todos los trabajos. La documentación no se ajusta a la realidad, ya que los servicios de este tipo no tardarán más de cinco segundos en ser iniciados por _systemd_ de todas formas. Tiene un comportamiento muy parecido al de _Type=simple_. |


## Las unidades de plantilla (_template_)

Los archivos de unidades de plantilla permiten que _systemd_ direccione varias unidades desde un solo archivo de configuración. Es decir:

* _getty@.service_: unidad de plantilla

* _getty@tty1.service_, _getty@tty3.service_, etc: instancias de la unidad de plantilla

La cadena de carácteres entre el _@_ y el sufijo de la unidad recibe el nombre de identificador de instancia. Es un argumento que se le pasa a _systemd_ para usarlo en el fichero de la unidad de plantilla. Se puede utilizar para personalizar la forma en que _systemd_ trata con esa instancia específica de la unidad, de manera que pueden existir varias instancias de la misma unidad.

Se utilizan dos especificadores en el fichero de la unidad para pasar el argumento de instancia:

* _%i_ pasa el identificador de instancia literalmente sin escapar.
* _%I_ pasa el identificador de instancia a través de un simple _unescaping algorithm_.


## Los ficheros _drop-in_

Existen dos maneras seguras de modificar una unidad sin tocar el fichero original:

1. Crear un nuevo fichero de unidad que reemplace la unidad original. Podemos copiar el antiguo archivo de la unidad desde _/usr/lib/systemd/system/_ a _/etc/systemd/system/_ y realizar los cambios allí.

2. Crear fragmentos _drop-in_ que se aplican encima de la unidad original. Para crear ficheros _drop-in_ para un fichero de unidad proporcionado por un paquete, podemos crear un directorio llamado _/etc/systemd/system/unidad.d/_, por ejemplo _/etc/systemd/system/httpd.service.d/_ y colocar en su interior los ficheros _*.conf_ para reemplazar o añadir nuevas opciones. _systemd_ analizará estos archivos _*.conf_ y los aplicará antes que los de la unidad original.

La forma más sencilla de hacer lo anterior es ejecutar:

`# systemctl edit unidad`

Esto abre el fichero _/etc/systemd/system/unidad.d/override.conf_ en un editor de texto (creando el fichero y el directorio si es necesario) y vuelve a cargar automáticamente la unidad cuando hemos terminado de editar, sin necesidad de ejecutar `systemctl daemon-reload`.

Por ejemplo, si queremos agregar una dependencia adicional a una unidad, podemos crear el siguiente fichero _/etc/systemd/system/unidad.d/nueva\_dependencia.conf_:

```
[Unit]
Requires=dependencia nueva
After=dependencia nueva
```

Siguiendo con otro ejemplo, con el fin de reemplazar la directiva _ExecStart_ para una unidad que no es del tipo _oneshot_, crearemos el siguiente archivo _/etc/systemd/system/unidad.d/nuevo\_exec.conf_:

```
[Service]
ExecStart=
ExecStart=orden nueva
```

Otro último ejemplo, para reiniciar automáticamente un servicio:

```
/etc/systemd/system/unidad.d/restart.conf

[Service]
Restart=always
RestartSec=30
```

