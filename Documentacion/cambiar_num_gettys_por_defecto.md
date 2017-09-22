
# ¿Cómo cambiar el número de _gettys_ ejecutados por defecto?

Actualmente, sólo un _getty_ se inicia de forma predeterminada. Si cambiamos a otra _tty_, un nuevo _getty_ se lanzará allí (_socket-activation style_). En otras palabras, `Ctl + Alt + F2` lanzará un nuevo _getty_ en la _tty2_.


## Método 1: Editando el fichero _/etc/systemd/logind.conf_ (activación bajo demanda)

Por defecto, el número de terminales virtuales activadas bajo demanda al arrancar el sistema se limita a seis. Para cambiar este comportamiento, editamos el fichero _/etc/systemd/logind.conf_ y cambiamos el valor de _NAutoVTs_. Si queremos que todas las teclas _[Fx]_ inicien un _getty_, simplemente hay que aumentar el valor de _NAutoVTs_ a 12.

Este fichero contiene entradas comentadas que muestran los valores predeterminados como una guía para el administrador. Se puede editar para llevar a cabo modificaciones locales.


## Método 2: Creando enlaces simbólicos en _/etc/systemd/system/getty.target.wants/_

Con este método podemos añadir _gettys_ preactivados, los cuales serán ejecutados y estarán funcionando desde el arranque. Para ello, tenemos que colocar otro enlace simbólico para crear instancias a otro _getty_ en el directorio _/etc/systemd/system/getty.target.wants/_:

```
# systemctl enable getty@tty8.service getty@tty9.service
# systemctl start getty@tty8.service getty@tty9.service
```

En este caso, si el valor de _NAutoVTs_ de _/etc/systemd/logind.conf_ fuera equivalente a 6, a partir de ahora contaríamos con un total de ocho terminales virtuales después de iniciar el sistema: seis bajo demanda (_tty1-6_) y dos terminales ya preactivadas (_tty8-9_).

En cambio, si lo que queremos es eliminar un _getty_, basta sólamente con eliminar el enlace simbólico del _getty_ que queramos del directorio _/etc/systemd/system/getty.target.wants/_:

```
# systemctl disable getty@tty8.service getty@tty9.service
# systemctl stop getty@tty8.service getty@tty9.service
```


## ¿Cómo iniciar terminales virtuales temporales?

Para iniciar una terminal virtual de forma temporal, podemos iniciar un servicio _getty_ en la _tty_ deseada escribiendo:

`# systemctl start getty@ttyN.service`

