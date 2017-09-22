
# Inicio de sesión automático en consolas virtuales

La configuración se basa en archivos _drop-in_ de _systemd_. Este tipo de ficheros son fragmentos que se aplican encima de la _unit_ original y sirven para reemplazar los parámetros predeterminados pasados ​​a _agetty_.

Existen pequeñas diferencias en la configuración de consolas virtuales y consolas seriales. Por ejemplo, el nombre de dispositivo de las consolas virtuales es _ttyN_, donde _N_ es un número. En cambio, los nombres de dispositivos de las consolas seriales son del tipo _ttySN_, donde _N_ también corresponde a un número.


## Ejemplo práctico

En este ejemplo queremos que en la _tty1_ se produzca de forma automática el inicio de sesión de _root_.

1. Simplemente tenemos que ejecutar el siguiente comando:

`# systemctl edit getty@tty1`

2. Este comando nos llevará a editar un nuevo fichero llamado _/etc/systemd/system/getty@tty1.service.d/override.conf, en el cual copiaremos lo siguiente:

```
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin root --noclear %I $TERM
```

A partir de ahora, cada vez que accedamos a la _tty1_ seremos _root_ automáticamente sin necesidad de escribir ningún tipo de contraseña.

También podríamos haber logrado esto creando de forma manual el directorio _/etc/systemd/system/getty@ttyN.service.d/_, donde N es el número de la _tty_ que queremos configurar, y en su interior, el fichero _drop-in_ llamado _override.conf_ con la configuración anterior.


## Inicio de sesión automático en modo gráfico

Siendo _root_ editamos el fichero _/etc/gdm/custom.conf_ y añadimos las siguientes directivas en la sección indicada a continuación:

```
[daemon]

AutomaticLoginEnable=True
AutomaticLogin=isx41012376
```

El valor de esta última corresponde al _login_ con el cual queremos iniciar la sesión automáticamente.


## ¿Cómo evitar que se borre la consola después del arranque?

Para evitar que _systemd_ borre la pantalla antes de iniciarla, crearemos el fichero _/etc/systemd/system/getty@tty1.service.d/noclear.conf_ con el siguiente contenido:

```
[Service]
TTYVTDisallocate=no
```

Esta configuración sólo reemplaza _TTYVTDisallocate_ para _agetty_ en la _tty1_ y deja intacto el fichero de servicio global _/usr/lib/systemd/system/getty@.service_.

