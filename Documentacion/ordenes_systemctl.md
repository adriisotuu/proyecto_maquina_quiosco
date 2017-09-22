
# Uso básico del comando _systemctl_

Es la principal orden para controlar _systemd_.


## Analizar el estado del sistema

| Función | Comando |
| ------- | ------- |
| Estado del sistema: | `$ systemctl status` |
| Listado de unidades activas: | `$ systemctl list-units` |
| Listado de todas las unidades: | `$ systemctl list-units --all` |
| Listado de todas las unidades inactivas: | `$ systemctl list-units --all --state=inactive` |
| Listado de unidades de servicio: | `$ systemctl list-units --type=service` |
| Listado de unidades que han tenido problemas: | `$ systemctl --failed` |
| Listado de todas las unidades instaladas: | `$ systemctl list-unit-files` | 

Los archivos de las unidades disponibles se pueden ver en _/usr/lib/systemd/system/_ y _/etc/systemd/system/_ (este último tiene prioridad).

El _output_ al ejecutar `$ systemctl list-units` contiene las siguientes columnas:

| Columna | Descripción |
| ------- | ----------- |
| UNIT | Nombre de la unidad. | 
| LOAD | Indica si la configuración de la unidad ha sido analizada por _systemd_. La configuración de las unidades cargadas se mantiene en memoria. |
| ACTIVE | Un estado de resumen indicando si la unidad está activa. Esto suele ser una forma bastante básica de saber si la unidad se ha iniciado correctamente o no. |
| SUB | Este es un estado de bajo nivel que proporciona información más detallada sobre la unidad. A menudo varía según el tipo de unidad, el estado y el método real en el que se ejecuta la unidad. |
| DESCRIPTION | Una breve descripción acerca de lo que la unidad es o hace. |


## Usar las unidades

| Función | Comando |
| ------- | ------- |
| Activar una unidad de inmediato: | `# systemctl start unidad` |
| Desactivar una unidad de inmediato: | `# systemctl stop unidad` |
| Reiniciar la unidad: | `# systemctl restart unidad` |
| Hacer que una unidad recargue su configuración: | `# systemctl reload unidad` |
| Mostrar el estado de una unidad, incluso si se está ejecutando o no: | `$ systemctl status unidad` |
| Comprobar si la unidad ya está habilitada o no: | `$ systemctl is-enabled unidad` |
| Activar el inicio automático en el arranque: | `# systemctl enable unidad` |
| Habilitar una unidad que se iniciará en el arranque e iniciar inmediatamente: | `# systemctl enable --now unidad` |
| Enmascarar una unidad para que sea imposible iniciarla: | `# systemctl mask unidad` |
| Desenmascarar una unidad: | `# systemctl unmask unidad` |
| Desactivar el inicio automático durante el arranque: | `# systemctl disable unidad` |
| Mostrar el fichero de unidad: | `$ systemctl cat unidad` |
| Listar el árbol de dependecias de una unidad: | `$ systemctl list-dependencies unidad` |
| Mostrar la página del manual asociada a una unidad: | `$ systemctl help unidad` |
| Recargar _systemd_, escaneando en busca de unidades nuevas o modificadas: | `# systemctl daemon-reload` |

