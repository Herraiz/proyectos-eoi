Como miniproyecto para la parte de IOT, vamos a desarrollar una “luz domótica”, que funcione a través de MQTT.

A grandes rasgos, encenderemos o apagaremos el led según los mensajes MQTT que recibamos.

  

Los requisitos son los siguiente:

-   Un fichero de configuración “credenciales.py” donde le especifiquemos el nombre y password de nuestra wifi (este fichero no se entrega cuando enviemos el proyecto)
    
-   Un fichero de configuracion settings.py que contenga:
    

-   ID = xxx # donde xxx pondremos el numero que queramos que será el identificador de nuestro dispositivo
    

-   Las especificaciones de la comunicación:
    

-   El broker será ‘broker.hivemq.com’
    
-   El topic al que nos suscribimos será ‘proyectoEOI’
    
-   Por el topic de recibiremos mensajes en formato JSON del tipo {“id”: 123, “value”: 1} hay que actuar solo cuando el ID se corresponda con el nuestro (configurado en settings.py), y cuando value sea 1 encendemos el led, cuando sea 0 lo apagamos. El resto de mensajes que estén mal formados o cuyo ID no se corresponda con el nuestro, se descartan
    

Se valorará que el código esté bien estructurado, y comentado
