
# El modelo _getty@.service_

## ¿Qué es _getty_?

Es el nombre genérico (abreviatura de _"get tty"_) que recibe un programa que gestiona una línea de terminal y su terminal conectada.

Su función es la de proteger al sistema de accesos no autorizados. Generalmente, cada proceso _getty_ es iniciado por _systemd_ y gestiona una sola línea de terminal.

_agetty_ es el _getty_ por defecto en _Arch Linux_, como parte del paquete _util-linux_. Básicamente, lo que hace es abrir un puerto _tty_, solicitar un _login_ e invocar el comando `/bin/login`. También disponemos de varias alternativas como _mingetty_, _fbgetty_ o _mgetty_.


## Función de las unidades _getty@.service_ y _serial-getty@.service_

En _systemd_, dos unidades _template_ son responsables de generar un _login prompt_ en las consolas de texto:

1. _getty@.service_ es responsable de los _login prompts_ del terminal virtual, es decir, los de la pantalla VGA expuestos en _/dev/tty1_ y dispositivos similares.

2. _serial-getty@.service_ es responsable de todos los demás terminales, incluyendo puertos seriales como _/dev/ttyS0_. A diferencia de la unidad _getty@.service_, la variable de entorno _$TERM_ se establece en _vt102_ y no como _linux_, valor por defecto en las terminales virtuales.


### Terminales virtuales

Tradicionalmente, el sistema _init_ en máquinas _Linux_ estaba configurado para generar (_spawn_) un número fijo de _login prompts_ al arrancar. En la mayoría de los casos se generaban seis instancias del programa _getty_, en las seis primeras _TTVV_, de la _tty1_ a la _tty6_.

Con la llegada de _systemd_ se hizo de un modo más dinámico: los _login prompts_ se inician sólo bajo demanda a medida que el usuario cambia a terminales virtuales no utilizadas, es decir, los servicios _autovt_ se generan automáticamente y estos se instancian desde la unidad de plantilla _autovt@.service_ para el nombre correspondiente, como por ejemplo, _autovt@tty4.service_.

Por lo tanto, el servicio _getty_ se instancia a _getty@tty2.service_, _getty@tty5.service_ y así sucesivamente, ya que _autovt@.service_ es un enlace simbólico que apunta a _getty@.service_.

Ya que no tenemos que iniciar incondicionalmente los procesos _getty_, esto nos permite ahorrar un poco de recursos y hace que la puesta en marcha sea un poco más rápida. Este comportamiento es principalmente transparente para el usuario: si el usuario activa una _TV_, el _getty_ se inicia de forma inmediata, de modo que el usuario difícilmente notará que no estaba funcionando todo el tiempo.

Por defecto, este _spawning_ automático se realiza para las _TTVV_ hasta la _tty6_ sólamente (para estar cerca de la configuración predeterminada tradicional de los sistemas _Linux_). Hay que tener en cuenta que el _auto-spawning_ de _gettys_ sólo se intenta si ningún otro subsistema ha tomado posesión de las _TTVV_ todavía.


### Las terminales _tty1_ y _tty6_

Dos terminales virtuales son manejadas especialmente por la lógica del _auto-spawning_:

En primer lugar, la _tty1_ obtiene tratamiento especial: si arrancamos en modo gráfico el _display manager_ toma posesión de esta _TV_. Si arrancamos en el modo multiusuario (texto), se inicia un _getty_ en ella (incondicionalmente, sin ninguna lógica bajo demanda).

El hecho de iniciar bajo demanda o no el _getty_ en la _tty1_ apenas hace una diferencia, ya que es la terminal virtual activa predeterminada de todos modos, por lo que la demanda está allí de todos modos en el arranque del sistema. Como podemos observar en la unidad _getty@.service_, el valor de la directiva _DefaultInstance=_ es _tty1_.

En segundo lugar, la _tty6_ está especialmente reservada para la activación de_autovt@.service_, con lo cual no estará disponible para otros subsistemas. Esto se hace con el fin de garantizar que siempre hay una manera de obtener un inicio de sesión de texto, incluso si debido a la rápida conmutación de usuario, _X_ tomó posesión de más de 5 _TTVV_.

Podemos cambiar fácilmente esta _TV_ reservada modificando la opción _ReserveVT=_ en el fichero de configuración _/etc/systemd/logind.conf_.


### Terminales seriales

Para hacer uso de una consola serial, simplemente añadimos `console=ttyS0` en la línea de comandos del _kernel_ y _systemd_ iniciará automáticamente un _getty_ en ella.


## La unidad _getty@.service_

```
[Service]
ExecStart=-/sbin/agetty --noclear %I $TERM
```

Este servicio ejecuta el comando _agetty_, que lo que hace es abrir un puerto _tty_, solicitar un _login_ e invocar el comando `/bin/login`.

El carácter "-" antes del comando permite que un código de salida del comando normalmente considerado como fracaso (_failed_) sea ignorado y considerado un éxito (_success_).

La opción `--noclear` impide que se borre la pantalla antes de solicitar el _login prompt_. De todos modos, la pantalla se borra debido a la directiva _TTYVTDisallocate=_.

El especificador `%I` hace referencia al nombre de la instancia al cual se le ha aplicado un _unescaping algorithm_. Es la cadena de caràcteres que se encuentra entre el caràcter _@_ y el sufijo del nombre de la unidad, en este caso _.service_ (_tty1_).

Por último, el valor de la variable de entorno `$TERM` indica el tipo de terminal. El valor predeterminado es _vt100_ o _linux_ para _Linux_ en un terminal virtual.

`Type=idle`

Esta directiva retrasará el inicio del servicio hasta que se completen todos los trabajos (solicitudes de cambio de estado a las unidades) para evitar contaminar el _login prompt_ con mensajes de inicio del sistema.

