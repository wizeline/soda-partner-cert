{% macro strptime(col, format) %}
    {% if target.type == 'duckdb' %}
        strptime({{ col }}, '{{ format }}')
    {% elif target.type == 'bigquery' %}
        parse_timestamp('{{ format }}', {{ col }})
    {% else %}
        {{ exceptions.raise_compiler_error('Target is of an unregistered type.') }}
    {% endif %}
{% endmacro %}
