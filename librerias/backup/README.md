## Miniproyecto: Copia de seguridad semanal

Librerias que necesitas

- zipfile
- os
- statistics
- arrow o datetime

Hacer un programa que realize una copia de seguridad, almacenando todos los archivos
que pertenezcan a un determinado conjunto, que determinaremos por su extension (por
ejemplo, ficheros de tipo `.py`, `.md`, `.pynb` y `.rst`.
pero esta lista no es obligatoria, modificala segun tus preferencias) dentro de un fichero zip (usa la libreria
zipfile)

El programa creara un fichero .ZIP distinto para cada dia de la semana. Por ejemplo, los
lunes debería realizar la copia de seguridad en el archivo `lunes.zip`, los martes, en 
`martes.zip`. Si el archivo ya existe, sobreescribirlo o borrarlo previamente.

Al finalizar el programa deberia listar los nombres de todos los ficheros que ha incluido en
la copia de seguridad, y despues mostrara la siguiente informacion estadística:

- Numero y tamaño total de archivos resguardados
- Tamaño medio de los archivos
- Tiempo total (en segundos) que ha tomado realizar la copia
