
# Las secciones de los ficheros de unidad _systemd_

La estructura interna de los ficheros de unidad se organiza en secciones. Las secciones se indican con un par de corchetes _[ ]_ con el nombre de la sección encerrado dentro. Cada sección se extiende hasta el comienzo de la siguiente sección o hasta el final del archivo.

Todas las unidades pueden tener dos secciones estándar: _[Unit]_ e _[Install]_. Todo tipo de unidad también puede implementar sus propias secciones, como _[Service]_ en unidades de servicio o _[Socket]_ en unidades _socket_.


## La sección _[Unit]_

Es la primera sección que encontramos en la mayoría de ficheros de unidad. Se utiliza generalmente para definir _metadata_ para la unidad y configurar la relación de la unidad con otras unidades.

| Directiva | Descripción |
| :-------: | ----------- |
| _Description=_ | Describe el nombre y la funcionalidad básica de la unidad. |
| _Documentation=_ | Proporciona una ubicación para una lista de _URIs_ para documentación. Pueden ser páginas de manual disponibles internamente o _URLs_ accesibles por la web. |
| _Requires=_ | Lista de todas las unidades de las que depende esta unidad. Si la unidad actual está activada, las unidades de la lista también deben activarse con éxito, de lo contrario esta unidad fallará. Estas unidades se inician en paralelo con la unidad actual por defecto. |
| _Wants=_ | Similar a _Requires=_, pero menos estricta. Si las unidades de las lista no se encuentran o no pueden iniciarse, la unidad actual continuará funcionando. Implica activación paralela de las unidades. |
| _Before=_ | Las unidades listadas no se iniciarán hasta que la unidad actual esté marcada como iniciada si se activan al mismo tiempo. Esto no implica una relación de dependencia. |
| _After=_ | Las unidades listadas se iniciarán antes de iniciar la unidad actual. No implica una relación de dependencia. |
| _Conflicts=_ | Se puede usar para listar unidades que no se pueden ejecutar al mismo tiempo que la unidad actual. El arranque de una unidad con esta relación hará que se detengan las otras unidades. |
| _DefaultDependencies=_ | Para las unidades con _DefaultDependencies=yes_ (el valor por defecto) se establecen automáticamente varias dependencias de unidades. |
| _AllowIsolate=_ | _Boolean_ que permite el aislamiento de la unidad. |


## La sección _[Install]_

La última sección suele ser la sección _[Install]_. Esta sección es opcional y se utiliza para definir el comportamiento de una unidad si está habilitada o deshabilitada. Al habilitar una unidad se marca para que se inicie automáticamente al arrancar.

| Directiva | Descripción |
| :-------: | ----------- |
| _WantedBy=_ | Permite especificar una relación de dependencia de manera similar a la directiva _Wants=_ en la sección _[Unit]_. Cuando se habilite una unidad con esta directiva, se creará un directorio _/etc/systemd/system/unidad.tipo\_unidad.wants/_. Dentro se creará un enlace simbólico a la unidad actual, creando así la dependencia. |
| _RequiredBy=_ | Similar a la directiva _WantedBy=_, pero especifica una dependencia requerida que causará que falle la activación de la unidad si no se cumple. Cuando esté habilitada, se creará un enlace simbólico a la unidad actual en _/etc/systemd/system/unidad.tipo\_unidad.requires/_.
| _Alias=_ | Esta directiva permite habilitar la unidad bajo otro nombre. |
| _Also=_ | Permite habilitar o deshabilitar unidades como un conjunto. |
| _DefaultInstance=_ | Para las unidades de plantilla que pueden producir instancias de unidades con nombres impredecibles, esta directiva puede utilizarse como valor predeterminado para el nombre si no se proporciona un nombre apropiado. |


## La sección _[Service]_

Entre las dos secciones anteriores, podemos encontrar secciones específicas de cada tipo de unidad. 

La sección _[Service]_ se utiliza para proporcionar configuración que sólo es aplicable a los servicios (unidades _.service_). 

| Directiva | Descripción |
| :-------: | ----------- |
| _Type=_ | Explicada detalladamente en este [apartado](https://github.com). |
| _RemainAfterExit=_ | Se utiliza normalmente con el tipo _oneshot_. Indica que el servicio debe considerarse activo incluso después de la salida del proceso. |
| _PIDFile=_ | Si el tipo de servicio es _forking_, esta directiva se utiliza para establecer la ruta del fichero que debe contener el número de _ID_ de proceso del proceso hijo principal que se debe supervisar. |
| _BusName=_ | Nombre del bus _D-Bus_ que el servicio intentará adquirir al utilizar el tipo de servicio _dbus_. |
| _NotifyAccess=_ | Especifica el acceso al _socket_ que debe utilizarse para escuchar las notificaciones cuando se selecciona el tipo de servicio _notify_. El valor de esta directiva puede ser _none_, _main_ o _all_. Por defecto, _none_ ignora todos los mensajes de estado. La opción _main_ escuchará los mensajes del proceso principal y la opción _all_ hará que todos los miembros del grupo de control del servicio sean procesados. |
| _ExecStart=_ | Especifica la ruta completa y los argumentos del comando que se va a ejecutar para iniciar el proceso. Esto sólo se puede especificar una vez (excepto para los servicios _oneshot_). |
| _ExecStartPre=_ | Proporciona comandos adicionales que deben ejecutarse antes de que se inicie el proceso principal. Esto se puede utilizar varias veces. |
| _ExecStartPost=_ | Indica los comandos que se ejecutarán después de que se inicie el proceso principal. Puede utilitzarse varias veces. |
| _ExecReload=_ | Directiva opcional que indica el comando necesario para volver a cargar la configuración del servicio si está disponible. |
| _ExecStop=_ | Indica el comando necesario para detener el servicio. Sin esta directiva, el proceso se destruirá inmediatamente cuando el servicio se detenga. |
| _KillMode=_ | Especifica cómo se matarán los procesos de esta unidad. Si se establece en _control-group_, todos los procesos restantes en el grupo de control de esta unidad se matarán al pararla (_stop_). Con _process_, sólo el proceso principal en sí mismo es eliminado. _mixed_ hace que la señal _SIGTERM_ se envíe al proceso principal mientras que la señal _SIGKILL_ subsiguiente se envía a todos los procesos restantes del grupo de control de la unidad. Por último, si se establece en _none_ no se procesa ningún proceso. |
| _Restart=_ | Indica las circunstancias bajo las cuales _systemd_ intentará reiniciar automáticamente el servicio. Los posibles valores son _always_, _on-success_, _on-failure_, _on-abnormal_, _on-abort_ y _on-watchdog_. Esto activará un reinicio de acuerdo con la forma en la que se detuvo el servicio. |
| _RestartSec=_ | Si el reinicio automático del servicio está habilitado, esto especifica la cantidad de tiempo a esperar antes de intentar reiniciar el servicio. |

