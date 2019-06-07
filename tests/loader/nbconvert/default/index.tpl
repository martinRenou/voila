{%- extends 'parent.tpl' -%}
{% block base %}
this is block base in nbconvert/default/index.tpl
{% block nested %}
this is block base:nested in nbconvert/default/index.tpl
{% endblock %}

{% block nested2 %}
this is block base:nested2 in nbconvert/default/index.tpl
{% endblock %}

{% endblock %}