14/11

- Ya tenemos unas tablas que podemos usar para crear los queries.
- El archivo de taco.sql será nuestro script de carga.
- El objetivo será correr validaciones contr las tablas de `ev_charging_reports` y `ev_loads_per_user`
- Se comparará el resultado del query a `ev_loads_per_user` contra los resultados de los agregados en `hourly_ev_loads_aggregated`.
- Ya se pueden ejecutar los comandos de `scan`, solo falta ver la forma de cargar las variables de ambiente desde el `.env`
