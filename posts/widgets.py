#http://djangosnippets.org/snippets/583/

from django.forms.widgets import Input

class MultiFileInput(Input):
    input_type = 'file'
    needs_multipart_form = True

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        if attrs.has_key('class'):
            attrs['class'] += ' multi'
        else:
            attrs['class'] = 'multi'

        #name += '[]'

        return super(MultiFileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        return files.get(name, None)

