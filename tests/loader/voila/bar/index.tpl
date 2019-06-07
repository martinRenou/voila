{%- extends 'default/index.tpl' -%}
{% block base %}
this is block base in voila/bar/index.tpl
{{ super() }}
{% block nested %}
{{ super() }}
{% endblock %}
{% endblock %}