## Gestor de Base de datos

Crear carpeta llamada database

Utiliza la siguiente sintaxis para realizar select,create,insert,delete and update.

*CREAR TABLA:
crear_tabla curso (id:int(10),nombre:var(30),programa:int)

*INSERTA UN ELEMENTO:
inserta curso (id,nombre,programa) (1,matematica,101)

*INSERTA VARIOS ELEMENTOS RANDOM:
inserta_rand curso (id,nombre,programa) (auto(1),str(1;curso),nrand(10;17)) 10

*SELECCIONAR CON WHERE Y SIN WHERE:
select curso 
select curso where nombre=curso_4

*EMILINAR ELEMENTO:
delete curso where id=7

*MODIFICAR UN ELEMENTO:
update curso set nombre=matematica where id=6

*ELIMINAR UNA TABLA Y SUS DATOS:
drop curso

*MOSTRAR ATRIBUTOS DE TABLA
show curso