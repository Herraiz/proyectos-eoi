# Miniproyecto

## Descripción

La tarea consiste en preparar un playbook de Ansible que automatice los pasos necesarios para desplegar la aplicación de Shield en una máquina virtual Debian 10.

## A tener en cuenta

Al usuario no privilegiado de la máquina—por defecto `debian` y normalmente creado durante la instalación—se le debe añadir la capacidad de usar el comando `sudo` modificando los grupos a los que pertenece dicho usuario. En el playbook se tienen diversas opciones para lidiar con esto:

* Confeccionar el playbook asumiendo que el usuario `debian` ya existe y tiene correctamente configurados los permisos para ejecutar comandos con `sudo`, así como las claves ssh de la máquina host (desde la que se ejecuta Ansible). Es la opción más sencilla, aunque menos "meritoria" técnicamente.
* Crear el usuario (si no estuviese creado ya) y asignarle el grupo `sudo` usando el módulo [`user`](https://docs.ansible.com/ansible/latest/modules/user_module.html) (atención al parámetro `groups`); opcionalmente también se puede modificar la configuración del fichero `/etc/sudoers` desde Ansible como se explica [aquí](https://stackoverflow.com/a/55876857). Hay que tener en cuenta que esta parte tiene que ser ejecutada por `root` ya que el usuario no privilegiado aún no tiene permisos para usar `sudo`; se recomienda leer detenidamente la [documentación](https://docs.ansible.com/ansible/latest/user_guide/become.html) al respecto, con especial atención a `become_method` y evaluar la opción `su`.
* Gestionar toda la creación del usuario y su pertenencia al grupo `sudo` desde Vagrant, como paso previo a lanzar el playbook que partiría asumiendo la misma situación que en el primer punto.

## Criterios de evaluación

En orden de importancia, se evaluará la entrega acorde a los siguientes puntos:

1. **<ins>Funcionalidad</ins>**: Después de ser ejecutado, se probará la efectividad del playbook abriendo un navegador local y dirigiéndolo a la IP de la máquina virtual en el puerto 80 (por ejemplo, `192.168.122.10:80`). Si el portal de Shield se muestra con la base de datos cargada y todos los componentes funcionando adecuadamente, este punto se considerará completo.
2. **<ins>Eficiencia</ins>**: Se valorará el utilizar módulos específicos de Ansible allá donde sea posible, por encima de comandos _ad-hoc_ usando módulos como [shell](https://docs.ansible.com/ansible/latest/modules/shell_module.html) o [command](https://docs.ansible.com/ansible/latest/modules/command_module.html#command-module). Por ejemplo, si queremos instalar una librería con `pip install <librería>`, es mejor utilizar el módulo [pip](https://docs.ansible.com/ansible/latest/modules/pip_module.html) que invocar el comando correspondiente con los mencionados `shell` o `command`
3. **<ins>Limpieza</ins>**: Se debe intentar que las _tasks_ de Ansible sean claras, directas, eviten redundancias y tengan un campo `name` descriptivo. Asimismo, el/los ficheros YAML deben seguir las reglas del formato y mantener la consistencia en cuanto a espaciado, etc.
4. **<ins>Extra-mile</ins>**: Agregar funcionalidades de Ansible que no hayan sido vistas en clase, allá donde tengan sentido: handlers, variables, roles, etc.

## Tarea opcional

Crear un Vagrantfile que automatice también la creación e instalación de una máquina virtual Debian 10

## Fecha límite de entrega

La tarea deberá ser entregada, a más tardar, el **miércoles 17 de junio** a las **23:59 WEST**

## Forma de entrega

Se habilitará una tarea en nuestro Google Classroom a tal efecto para poder subir los ficheros finales.
