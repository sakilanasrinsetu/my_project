import re
from django import forms
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from middlewares.middlewares import RequestMiddleware
from django.core.paginator import Paginator


"""
************************ Paginator Helper Functions ************************
"""

def get_paginated_object(request, queryset, paginate_by=8):
    """
    get_paginated_object() => Paginates object.
    params => queryset, paginate_by
    return => paginated queryset object
    """
    paginator = Paginator(queryset, paginate_by)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = queryset
    # return paginated object
    return page_obj

"""
************************ Get Dynamic Fields Helper Functions ************************
"""


def get_dynamic_fields(field=None, self=None):
    """
    get_dynamic_fields() => Gets model fields dynamically.
    params => field, self
    return => (field.name, value, field_type)
    """
    value = "-"
    if not field.value_from_object(self) == None and not field.value_from_object(self) == "":
        value = field.value_from_object(self)
    # print("***Fieldname***", field.name, "***FieldType***", field.get_internal_type())
    return (field.name, value, field.get_internal_type())


"""
************************ Validate Form Helper Functions ************************
"""


def validate_normal_form(field, field_qs, form, request):
    """
    validate_normal_form() => Validates form.
    params => field, field_qs, form, request
    return => int (0 or 1)
    """
    if not field_qs == None:
        if field_qs.exists():
            form.add_error(
                field, forms.ValidationError(
                    f"This {field} is already exists! Please try another one."
                )
            )
            return 0
    if 'update' in request.path or 'edit' in request.path:
        dynamic_msg = "Updated Successfully !!!"
    elif 'create' in request.path or 'add' in request.path:
        dynamic_msg = "Created Successfully !!!"
    else:
        dynamic_msg = "Manipulated Successfully !!!"
    messages.add_message(
        request, messages.SUCCESS,
        dynamic_msg
    )
    return 1


"""
************************ Retrieve Object Helper Functions ************************
"""

def get_simple_object(key='slug', model=None, self=None):
    """
    get_simple_object() => Retrieve object instance.
    params => key, model, self
    return => object (instane)
    """
    try:
        if key == 'id':
            id = self.kwargs['id']
            instance = model.objects.get(id=id)
        else:
            slug = self.kwargs['slug']
            instance = model.objects.get(slug=slug)
    except model.DoesNotExist:
        raise Http404('Not found!!!')
    except model.MultipleObjectsReturned:
        if key == 'id':
            id = self.kwargs['id']
            instance = model.objects.filter(id=id).first()
        else:
            slug = self.kwargs['slug']
            instance = model.objects.filter(slug=slug).first()
    except:
        raise Http404("Something went wrong !!!")
    return instance


"""
************************ Delete Object Helper Functions ************************
"""


def delete_simple_object(request, key, model, redirect_url):
    """
    delete_simple_object() => Deletes an object.
    params => request, key, model
    return => HttpResponseRedirect(url)
    """
    url = reverse('dashboard:home')
    if request.method == "POST":
        dynamic_identifier = request.POST.get("dynamic_identifier")
        if key == 'slug':
            qs = model.objects.filter(slug=dynamic_identifier)
        else:
            qs = model.objects.filter(id=dynamic_identifier)
        if qs.exists():
            qs.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Deleted successfully!")
            if redirect_url is not None:
                url = reverse(redirect_url)
            else:
                url = request.META.get('HTTP_REFERER', '/')
        else:
            messages.add_message(request, messages.WARNING,
                                 "Not found!")
    return HttpResponseRedirect(url)


"""
************************ Context Data Helper Functions ************************
"""

def get_simple_context_data(request=None, app_namespace=None, model_namespace=None, display_name=None, model=None, list_template=None, fields_to_hide_in_table=[], **kwargs):
    """
    params: request, app_namespace (string), model_namespace (string), model (class), fields_to_hide_in_table (list), **kwargs

    return: object {
        "create_url": "example_app:create_example",
        "update_url": "example_app:update_example",
        "detail_url": "example_app:example_detail",
        "delete_url": "example_app:delete_example",
        "list_url": "example_app:create_example",
        "can_add_change": True,
        "can_add": True,
        "can_change": True,
        "can_view": True,
        "can_delete": True,
        "namespace": 'example',
        "list_objects": [],
        "list_template": "example.html",
        "fields_count": 7,
        "fields": {"field_name": "field_verbose_name"},
        "fields_to_hide_in_table": ["slug"],
        "kwargs_key": "kwargs_value"
    }

    Formats:
        URL Formats Required:
            => Create URL: "{app_namespace}:create_{model_namespace}",
            => Update URL: "{app_namespace}:update_{model_namespace}",
            => Detail URL: "{app_namespace}:{model_namespace}_detail",
            => Delete URL: "{app_namespace}:delete_{model_namespace}",
            => List URL: "{app_namespace}:create_{model_namespace}"
        Model Namespace:
            => ExampleModel -> example_model
        App Namespace:
            => example_app_name
        Fields To Hide in Table:
            => ["slug", "id"]
    """
    def get_permission_namespace(namespace):
        whitelist = set('abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        filtered_permission_namespace = ''.join(filter(whitelist.__contains__, namespace))
        return filtered_permission_namespace

    if request == None or model_namespace == None or model == None:
        raise ValueError(
            "request, model_namespace and model cannot be null! Please pass these arguments properly."
        )
    
    permission_namespace = get_permission_namespace(model_namespace)

    common_contexts = {}
    if not app_namespace == None:
        # URL Binding
        common_contexts["create_url"] = f"{app_namespace}:create_{model_namespace}"
        common_contexts["update_url"] = f"{app_namespace}:update_{model_namespace}"
        common_contexts["detail_url"] = f"{app_namespace}:{model_namespace}_detail"
        common_contexts["delete_url"] = f"{app_namespace}:delete_{model_namespace}"
        common_contexts["list_url"] = f"{app_namespace}:create_{model_namespace}"
        # Permission Binding
        common_contexts["can_add_change"] = True if request.user.has_perm(
            f'{app_namespace}.add_{permission_namespace}') or request.user.has_perm(f'{app_namespace}.change_{permission_namespace}') else False
        common_contexts["can_add"] = request.user.has_perm(
            f'{app_namespace}.add_{permission_namespace}')
        common_contexts["can_change"] = request.user.has_perm(
            f'{app_namespace}.change_{permission_namespace}')
        common_contexts["can_view"] = request.user.has_perm(
            f'{app_namespace}.view_{permission_namespace}')
        common_contexts["can_delete"] = request.user.has_perm(
            f'{app_namespace}.delete_{permission_namespace}')
    else:
        # URL Binding
        common_contexts["create_url"] = f"create_{model_namespace}"
        common_contexts["update_url"] = f"update_{model_namespace}"
        common_contexts["detail_url"] = f"{model_namespace}_detail"
        common_contexts["delete_url"] = f"delete_{model_namespace}"
        common_contexts["list_url"] = f"create_{model_namespace}"
        # Permission Binding
        common_contexts["can_add_change"] = True if request.user.has_perm(
            'add_{permission_namespace}') or request.user.has_perm('change_{permission_namespace}') else False
        common_contexts["can_add"] = request.user.has_perm(
            'add_{permission_namespace}')
        common_contexts["can_change"] = request.user.has_perm(
            'change_{permission_namespace}')
        common_contexts["can_view"] = request.user.has_perm(
            'view_{permission_namespace}')
        common_contexts["can_delete"] = request.user.has_perm(
            'delete_{permission_namespace}')

    common_contexts["namespace"] = model_namespace
    common_contexts["display_name"] = display_name
    common_contexts["list_objects"] = model.objects.all().order_by('-id')
    if not list_template == None:
        common_contexts["list_template"] = list_template
    common_contexts["fields_count"] = len(model._meta.get_fields()) + 1
    common_contexts["fields"] = dict([(f.name, f.verbose_name)
                                      for f in model._meta.fields + model._meta.many_to_many])
    if not fields_to_hide_in_table == None:
        common_contexts["fields_to_hide_in_table"] = fields_to_hide_in_table
    
    for key, value in kwargs.items():
        common_contexts[key] = value

    return common_contexts

"""
************************ Character Validate Helper Functions ************************
"""

def validate_chars(field_data, allowed_chars=None, max_length=50):
    """
    validate_chars() => Validates character field.
    params => field_data, allowed_chars, max_length
    return => field_data
    """
    if not field_data == None:
        pattern = allowed_chars
        characters_to_remove = '^[]+$'
        for character in characters_to_remove:
            pattern = pattern.replace(character, "")
        if not allowed_chars == None:
            allowed_chars = re.match(allowed_chars, field_data)
            if not allowed_chars:
                raise forms.ValidationError(
                    f"Only [{pattern}] these characters are allowed!"
                )
        length = len(field_data)
        if length > max_length:
            raise forms.ValidationError(
                f"Maximum {max_length} characters allowed. Currently using {length}!"
            )
    return field_data



"""
************************ Form Widget Helper Functions ************************
"""


def simple_form_widget(self=None, field=None, maxlength=50, step=None, pattern=None, placeholder=None):
    """
    simple_form_widget() => Generates form widget.
    params => self, field, maxlength, step, pattern, placeholder
    """
    field_name = ' '.join(field.split('_')).title()
    allowed_chars = pattern
    print(pattern)
    if not pattern == None:
        characters_to_remove = '^[]{1,}$'
        for character in characters_to_remove:
            allowed_chars = allowed_chars.replace(character, "")
    if not placeholder == None:
        placeholder = placeholder
    else:
        placeholder = f'Enter {field_name}...'
    self.fields[field].widget.attrs.update({
        'id': f'{field}_id',
        'placeholder': placeholder,
        'maxlength': maxlength,
        'step': step,
        'pattern': pattern
    })
    if not pattern == None:
        self.fields[field].help_text = f"Only [{allowed_chars}] these characters are allowed."


"""
************************ User Permission Checker Helper Functions ************************
"""


def user_has_permission(permission=None):
    """
    user_has_permission() => Checks if user has the required permissions to access the content.
    params => permission ('app_name.can_add_log_entry') => 'app_name.permission'
    """
    request = RequestMiddleware(get_response=None)
    request = request.thread_local.current_request
    if request.user.is_superuser == True or request.user.has_perm(permission) == True:
        return True
