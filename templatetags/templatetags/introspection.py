from django import template

register = template.Library()

class Info(object):
    pass

def fixup(text):
    t = str(text)
    return t
    #if len(t) > 30:
    #    return str(t)[:27]+"..."
    #else:
    #    return t
    
def fixuplist(l):
    nl = []
    for i in range(0,len(l)):
        nl.append(fixup(l[i]))
    return nl

def inspect_model_instance(instance):
    mm = instance.__class__._meta
    model = instance.__class__.__name__
    fields = []
    for f in mm.fields + mm.many_to_many:
        field = Info()
        field.name = f.name
        field.type = f.__class__.__name__
        field.value = fixup(getattr(instance,f.name))
        fields.append(field)
    return {'model': model, 'fields': fields }

def inspect_form_instance(instance):
    fields = []
    bound = str(instance.is_bound)
    for f in instance.fields.keys():
        field = Info()
        field.name = f
        field.type = instance.fields[f].__class__.__name__
        field.widget = instance.fields[f].widget.__class__.__name__
        field.initial = fixup(instance.initial.get(f,''))
        field.bound = fixup(instance.data.get(f,''))
        field.errors = fixuplist(instance[f].errors)
        fields.append(field)
    return {'bound': bound, 'fields': fields }

def inspect_dict(instance):
    keys = []
    for k in instance.keys():
        key = Info()
        key.name = k
        key.type = instance[k].__class__.__name__
        key.value = fixup(instance[k])
        keys.append(key)
    return {'keys': keys }

def inspect_object(obj,name=""):
    dtype = 'basic'
    classname = obj.__class__.__name__
    meta = fixup(obj) 
    if getattr(obj,'__metaclass__',None):
        if obj.__metaclass__.__name__ == 'DeclarativeFieldsMetaclass': 
            dtype = 'form'
            meta = inspect_form_instance(obj)
        elif obj.__metaclass__.__name__ == 'ModelBase': 
            dtype = 'model'
            meta = inspect_model_instance(obj)
    elif classname == 'dict':
        dtype = 'dict'
        meta = inspect_dict(obj)
    elif classname == 'list':
        dtype = 'list'
        meta = fixuplist(obj)
        
    return {'classname': classname,'name': name, 'dtype': dtype, 'meta': meta}

register.inclusion_tag('inspect_object.html')(inspect_object)


