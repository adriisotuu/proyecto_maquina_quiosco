
# _Targets_

_systemd_ utiliza _targets_ que sirven un propósito similar a los _runlevels_ o niveles de ejecución, pero que tienen un comportamiento un poco diferente. A cada _target_ se le asigna un nombre, en lugar de numerarse, y está destinado a servir a un propósito específico con la posibilidad de realizar más de una acción al mismo tiempo.

Algunos de ellos son activados heredando todos los servicios de otro _target_ e implementando servicios adicionales. Como hay _targets_ de _systemd_ que imitan los _runlevels_ de _SystemVinit_, es posible pasar de un _target_ a otro utilizando la orden `# telinit RUNLEVEL`.

Con el comando `systemctl list-units --type=target` podemos ver los _targets_ presentes en nuestro sistema.


## Tabla comparativa entre los _runlevels_ de _SysV_ y los _targets_ de _systemd_

| _Runlevel_ de _SysV_ | _Target_ de _systemd_ | _Descripción_ |
| :------------------: | --------------------- | ------------- |	
| 0 | _poweroff.target_, _runlevel0.target_ | Detiene el sistema. |
| 1, s, _single_ | _rescue.target_, _runlevel1.target_ | Modo de usuario único. |
| 2, 4 | _runlevel2.target_, _runlevel4.target_, _multi-user.target_ | Definidos por el usuario. Por defecto, idéntico a _multi-user.target_. |
| 3 | _multi-user.target_, _runlevel3.target_ | Multiusuario, no gráfica. Los usuarios, por lo general, pueden acceder a través de múltiples consolas o a través de la red. |
| 5 | _graphical.target_, _runlevel5.target_ | Multiusuario, gráfica. Es decir, _multi-user.target_ + inicio de sesión gráfica. |
| 6 | _reboot.target_, _runlevel6.target_ | Reinicia el sistema. |
| _emergency_ | _emergency.target_ | Consola de emergencia. |

Si queremos hacer uso de los niveles de ejecución 2 y 4, se sugiere dar un nuevo nombre al _target_ como _/etc/systemd/system/nombre.target_ y que tome como base uno de los _runlevels_ existentes. Crearemos el directorio _/etc/systemd/system/nombre.target.wants/_, así como un enlace a los servicios adicionales de _/usr/lib/systemd/system/_ que queramos habilitar.


## ¿Qué _default.target_ está utilizando nuestro sistema?

El proceso _systemd_ tiene un _target_ por defecto que utiliza al arrancar el sistema. Para saber cúal, ejecutamos:

`$ systemctl get-default`


## ¿Cómo cambiar el _target_ por defecto al arrancar el sistema?

Añadiremos el siguiente parámetro a nuestro gestor de arranque en la línea del _kernel_:

`systemd.unit=multi-user.target`

Con esta opción arrancaremos en modo multiusuario, pero no habremos modificado el _default.target_ de nuestro sistema.


## Modificar el _default.target_

```
# systemctl set-default multi-user.target
Removed /etc/systemd/system/default.target.
Created symlink /etc/systemd/system/default.target → /usr/lib/systemd/system/multi-user.target.
```

Como podemos observar, se ha vuelto a crear el enlace _/etc/systemd/system/default.target_ que ahora apunta a la unidad _/usr/lib/systemd/system/multi-user.target_ en vez de a _graphical.target_. Con lo cual, a partir de ahora nuestro sistema siempre arrancará en modo 3.


## Aislar _targets_ (_isolating_)

Es posible iniciar todas las unidades asociadas con un _target_ y detener todas las unidades que no forman parte del árbol de dependencias. El comando que necesitamos para hacer esto se llama _isolate_, es decir, aislar:

`# systemctl isolate multi-user.target`

Por ejemplo, si estamos trabajando en un entorno gráfico con _graphical.target_ activo, se puede apagar el sistema gráfico y poner el sistema en un estado de línea de comandos multiusuario mediante el aislamiento de _multi-user.target_. Dado que _graphical.target_ depende de _multi-user.target_ pero no al revés, todas las unidades gráficas se detendrán.

Esta orden solo cambiará el _target_ actual y no tendrá ningún efecto sobre el siguiente arranque. Es equivalente a las órdenes `telinit 3` o `telinit 5` en _Sysvinit_.

