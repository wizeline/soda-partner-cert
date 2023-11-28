14/11

- Ya tenemos unas tablas que podemos usar para crear los queries.
- El archivo de taco.sql será nuestro script de carga.
- El objetivo será correr validaciones contr las tablas de `ev_charging_reports` y `ev_loads_per_user`
- Se comparará el resultado del query a `ev_loads_per_user` contra los resultados de los agregados en `hourly_ev_loads_aggregated`.
- Ya se pueden ejecutar los comandos de `scan`, solo falta ver la forma de cargar las variables de ambiente desde el `.env`

27/11

- Ya tenemos los checks casi a su totalidad
- Ya tenemos una base de proyecto estilo medallón
  - Las tablas tendrán una tabla previa.
    - Esto fue para poder tener cross reference checks...
  - Las tablas `raw_*` serán materializadas y se cargarán a su propio esquema
  - Las tablas `stg_*` serán vistas y se cargarán al esquema de main.
    - Esto sirve para generar los scans.
- Ya tenemos una base de proyecto de Dagster
  - Se llama Hermes <3 🏃‍♂️
- Ya tenemos una base de proyecto de DBT
  - Se llama Optimus <3 🤖
- Se renombró la base de datos para que se llame `Athena`
- Ya podemos utilizar poetry para el proyecto
- Los sql para carga y consulta ya no son necesarios.
- Se renombró el proyecto a solo soda-certification
