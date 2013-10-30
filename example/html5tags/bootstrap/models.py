# -*- coding: utf-8 -*-
from django.forms import models

from .fields import Field
from .widgets import Select, SelectMultiple
from .forms import BaseForm

__all__ = ('ModelForm', 'ModelChoiceField', 'ModelMultipleChoiceField')


class ModelForm(BaseForm, models.ModelForm):
    pass


class ModelChoiceField(Field, models.ModelChoiceField):
    widget = Select


class ModelMultipleChoiceField(Field, models.ModelMultipleChoiceField):
    widget = SelectMultiple
