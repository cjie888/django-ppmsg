# -*- coding: utf-8 -*-
from django import forms

from .widgets import (TextInput, HiddenInput, CheckboxInput, Select,
                      ClearableFileInput, SelectMultiple, DateInput,
                      DateTimeInput, TimeInput, NumberInput, PasswordInput,
                      EmailInput, NullBooleanSelect, IPAddressInput, MarkDownTextarea,
                      SplitDateTimeWidget, SplitHiddenDateTimeWidget)

__all__ = (
    'Field', 'CharField', 'IntegerField', 'DateField', 'TimeField',
    'DateTimeField', 'EmailField', 'FileField', 'ImageField', 'URLField',
    'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
    'FloatField', 'DecimalField', 'RegexField', 'IPAddressField',
    'GenericIPAddressField', 'TypedChoiceField', 'FilePathField',
    'TypedMultipleChoiceField', 'ComboField', 'MultiValueField',
    'SplitDateTimeField', 'SlugField', 'MarkdownField'
)


class Field(forms.Field):
    widget = TextInput
    hidden_widget = HiddenInput


class CharField(Field, forms.CharField):
    widget = TextInput
    def widget_attrs(self, widget):
        attrs = super(CharField, self).widget_attrs(widget)
        if self.max_length is not None and isinstance(widget, (TextInput, PasswordInput)):
            # The HTML attribute is maxlength, not max_length.
            attrs.update({'maxlength': str(self.max_length)})
        return attrs


class BooleanField(Field, forms.BooleanField):
    widget = CheckboxInput


class NullBooleanField(Field, forms.NullBooleanSelect):
    widget = NullBooleanSelect


class ChoiceField(Field, forms.ChoiceField):
    widget = Select


class TypedChoiceField(ChoiceField, forms.TypedChoiceField):
    widget = Select


class FilePathField(ChoiceField, forms.FilePathField):
    widget = Select


class FileField(Field, forms.FileField):
    widget = ClearableFileInput


class ImageField(Field, forms.ImageField):
    widget = ClearableFileInput


class MultipleChoiceField(Field, forms.MultipleChoiceField):
    widget = SelectMultiple


class TypedMultipleChoiceField(MultipleChoiceField, forms.TypedMultipleChoiceField):
    pass


class DateField(Field, forms.DateField):
    widget = DateInput


class DateTimeField(Field, forms.DateTimeField):
    widget = DateTimeInput


class TimeField(Field, forms.TimeField):
    widget = TimeInput


class DecimalField(Field, forms.DecimalField):
    widget = NumberInput


class FloatField(Field, forms.FloatField):
    widget = NumberInput


class IntegerField(Field, forms.IntegerField):
    widget = NumberInput

    def widget_attrs(self, widget):
        attrs = super(IntegerField, self).widget_attrs(widget) or {}
        if self.min_value is not None:
            attrs['min'] = self.min_value
        if self.max_value is not None:
            attrs['max'] = self.max_value
        return attrs


class EmailField(Field, forms.EmailField):
    widget = EmailInput


class URLField(Field, forms.URLField):
    pass


class RegexField(Field, forms.RegexField):
    widget = TextInput

    def __init__(self, regex, js_regex=None, max_length=None, min_length=None,
                 error_message=None, *args, **kwargs):
        self.js_regex = js_regex
        super(RegexField, self).__init__(regex, max_length, min_length,
                                         *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(RegexField, self).widget_attrs(widget) or {}
        if self.js_regex is not None:
            attrs['pattern'] = self.js_regex
        return attrs


class IPAddressField(Field, forms.IPAddressField):
    widget = IPAddressInput


class GenericIPAddressField(Field, forms.GenericIPAddressField):
    pass


class ComboField(Field, forms.ComboField):
    pass


class MultiValueField(Field, forms.MultiValueField):
    widget = SelectMultiple
    pass


class SplitDateTimeField(forms.SplitDateTimeField):
    pass


class SlugField(Field, forms.SlugField):
    pass


class MarkdownField(Field):
    widget = MarkDownTextarea
