# Enchaîné - 128 points

On est face à une chaîne de caractères assez longue ressemblant à du Base64 sans padding, et comprenant 2 points `.` . On reconnaît un JWT (JSON Web Token). Celui-ci peut être décodé par un site comme [jwt.io](https://jwt.io/). On obtient une chaîne hexadécimale, qui décodée donne du Base64, qui donne enfin le flag chiffré par décalage (voir Guacamole).