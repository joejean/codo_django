from django import template

register = template.Library()

def grouped(l, n):
	# Yield successive n-sized chunks from l.
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

@register.filter
def group_by(value, arg):
	'''
	This filter can be used in a template to display n items per 
	row from a list of items.
	{% for group in objects|group_by:2 %}
	<div class="row">
		{% for obj in group %}
			<div class="span6">
				foo
			</div>
		{% endfor %}
	</div>
	{% endfor %}
	'''
	return grouped(value, arg)