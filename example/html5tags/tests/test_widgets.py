import datetime
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.template import Context, Template
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.dates import MONTHS
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

import html5tags.bootstrap as forms
from example_app.models import SomeModel

from .base import InvalidVariable


@python_2_unicode_compatible
# class SomeModel(models.Model):
#     some_field = models.CharField(max_length=255)
# 
#     def __str__(self):
#         return u'%s' % self.some_field


class WidgetRenderingTest(TestCase):
    """Testing the rendering of the different widgets."""
    maxDiff = None

    def test_text_input(self):
        """<input type="text">"""
        class TextForm(forms.Form):
            text = forms.CharField(label='My text field')

        rendered = TextForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">My text field:</label>
            <input class=" form-control" type="text" name="text" id="id_text" />
        </p>""")

        form = TextForm(data={'text': ''})
        self.assertFalse(form.is_valid())

        form = TextForm(data={'text': 'some text'})
        self.assertTrue(form.is_valid())

        class TextFormNotRequire(forms.Form):
            text = forms.CharField(required=False)

        rendered = TextFormNotRequire().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <input class=" form-control" type="text" name="text" id="id_text">
        </p>""")

        class TextFormAttr(forms.Form):
            text = forms.CharField(
                widget=forms.TextInput(attrs={'placeholder': 'Heheheh'})
            )

        rendered = TextFormAttr(initial={'text': 'some initial text'}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <input class=" form-control" type="text" name="text" id="id_text" value="some initial text" placeholder="Heheheh" >
        </p>""")

        invalid = lambda: forms.CharField(max_length=5).clean('foo bar')
        self.assertRaises(forms.ValidationError, invalid)

        class TextFormMax(forms.Form):
            text = forms.CharField(max_length=2)
 
        self.assertFalse(TextFormMax(data={'text': 'foo'}).is_valid())
 
        rendered = TextFormMax(data={'text': 0}).as_p()
 
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <input class=" form-control" type="text" name="text" id="id_text" value="0" maxlength="2">
        </p>""")

    def test_password(self):
        """<input type="password">"""
        class PwForm(forms.Form):
            pw = forms.CharField(widget=forms.PasswordInput)
 
        rendered = PwForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_pw">Pw:</label>
            <input class=" form-control" type="password" name="pw" id="id_pw" >
        </p>""")

        class PwFormWidget(forms.Form):
            text = forms.CharField()
            pw = forms.CharField(widget=forms.PasswordInput)
 
        form = PwFormWidget(data={'pw': 'some-pwd'})
        self.assertFalse(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li><small><font color="#ff0000">This field is required.</font></small></li>
        </ul>
        <p>
            <label for="id_text">Text:</label>
            <input class=" form-control" type="text" name="text" id="id_text" >
        </p>
        <p>
            <label for="id_pw">Pw:</label>
            <input class=" form-control" type="password" name="pw" id="id_pw" value="some-pwd" >
        </p>""")

        class PwFormData(forms.Form):
            text = forms.CharField()
            pw = forms.CharField(
                widget=forms.PasswordInput(render_value=True)
            )
 
        form = PwFormData(data={'pw': 'some-pwd'})
        self.assertFalse(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li><small><font color="#ff0000">This field is required.</font></small></li>
        </ul>
        <p>
            <label for="id_text">Text:</label>
            <input class=" form-control" type="text" name="text" id="id_text" >
        </p>
        <p>
            <label for="id_pw">Pw:</label>
            <input class=" form-control" type="password" name="pw" id="id_pw" value="some-pwd">
        </p>""")

    def test_hidden(self):
        """<input type="hidden">"""
        class HiddenForm(forms.Form):
            hide = forms.CharField(widget=forms.HiddenInput())

        rendered = HiddenForm().as_p()
        self.assertHTMLEqual(rendered, """
        <input class=" form-control" type="hidden" name="hide" id="id_hide" >
        """)

        form = HiddenForm(data={'hide': 'what for?'})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <input class=" form-control" type="hidden" name="hide" id="id_hide" value="what for?">
        """)

    def test_textarea(self):
        """<textarea>"""

        class TextForm(forms.Form):
            text = forms.CharField(widget=forms.Textarea)

        rendered = TextForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <textarea class=" form-control" name="text" id="id_text" cols="40" rows="10" ></textarea>
        </p>
        """)

        class TextFormAttrs(forms.Form):
            text = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 42, 'cols': 55})
            )
 
        rendered = TextFormAttrs().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <textarea class=" form-control" name="text" id="id_text" rows="42" cols="55" ></textarea>
        </p>
        """)

    def test_file(self):
        """"<input type="file">"""
        class FileForm(forms.Form):
            file_ = forms.FileField()

        rendered = FileForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label>
            <input type="file" name="file_" id="id_file_" >
        </p>
        """)

        class FileFormNotrequire(forms.Form):
            file_ = forms.FileField(required=False)
 
        rendered = FileForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label>
            <input type="file" name="file_" id="id_file_">
        </p>
        """)

    def test_date(self):
        """<input type="date">"""
        class DateForm(forms.Form):
            date = forms.DateField()

        rendered = DateForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p><label for="id_date">Date:</label> 
        <input data-date-language="en" name="date" data-bootstrap-widget="datepicker" 
        data-date-format="yyyy-mm-dd" type="None" id="id_date" class="form-control form-control" />
            <script>$("#id_date").datetimepicker({
                keyboardNavigation: true,
                todayBtn: true,
                todayHighlight: true,
                startView: 1}, "update");
            </script>
        </p>
        """)

    def test_datetime(self):
        """<input type="datetime">"""
        class DateTimeForm(forms.Form):
            date = forms.DateTimeField()

        rendered = DateTimeForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p><label for="id_date">Date:</label> <input data-date-language="en" name="date" data-bootstrap-widget="datepicker" 
        data-date-format="yyyy-mm-dd hh:ii:ss" type="text" id="id_date" class="form-control" />
            <script>$("#id_date").datetimepicker({
                keyboardNavigation: true,
                todayBtn: true,
                todayHighlight: true,
                startView: 1}, "update");
            </script>
        </p>
        """)

    def test_time(self):
        """<input type="time">"""
        class TimeForm(forms.Form):
            date = forms.TimeField()

        rendered = TimeForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p><label for="id_date">Date:</label> <input data-date-language="en" name="date" data-bootstrap-widget="datepicker" 
        data-date-format="hh:ii:ss" type="text" id="id_date" class="form-control" />
            <script>$("#id_date").datetimepicker({
                keyboardNavigation: true,
                todayBtn: true,
                todayHighlight: true,
                startView: 1}, "update");
            </script>
        </p>
        """)

    def test_search(self):
        """<input type="search">"""
        class SearchForm(forms.Form):
            query = forms.CharField(widget=forms.SearchInput)

        rendered = SearchForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_query">Query:</label>
            <input class=" form-control" type="search" name="query" id="id_query" >
        </p>
        """)

    def test_email(self):
        """<input type="email">"""
        class EmailForm(forms.Form):
            email = forms.EmailField()

        rendered = EmailForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_email">Email:</label>
            <input class=" form-control" type="email" name="email" id="id_email" >
        </p>
        """)

        form = EmailForm(data={'email': 'foo@bar.com'})
        self.assertTrue(form.is_valid())
        form = EmailForm(data={'email': 'lol'})
        self.assertFalse(form.is_valid())

    def test_url(self):
        """<input type="url">"""
        class URLForm(forms.Form):
            url = forms.URLField()

        rendered = URLForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_url">Url:</label>
            <input class=" form-control" type="text" name="url" id="id_url" >
        </p>
        """)

        form = URLForm(data={'url': 'http://example.com'})
        self.assertTrue(form.is_valid())
        form = URLForm(data={'url': 'com'})
        self.assertFalse(form.is_valid())


    def test_number(self):
        """<input type="number">"""
        class NumberForm(forms.Form):
            num = forms.DecimalField()

        rendered = NumberForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input class=" form-control" type="number" name="num" id="id_num" >
        </p>
        """)

        form = NumberForm(data={'num': 10})
        self.assertTrue(form.is_valid())
        form = NumberForm(data={'num': 'meh'})
        self.assertFalse(form.is_valid())

        class NumberFormAttrs(forms.Form):
            num = forms.DecimalField(
                widget=forms.NumberInput(attrs={'min': 5, 'max': 10})
            )
 
        rendered = NumberFormAttrs().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input class=" form-control" type="number" name="num" id="id_num" min="5" max="10">
        </p>
        """)

        class NumInput(forms.NumberInput):
            min = 9
            max = 99
            step = 10

        class NumberFormWidget(forms.Form):
            num = forms.DecimalField(widget=NumInput)
 
        rendered = NumberFormWidget().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input class=" form-control" type="number" name="num" id="id_num" min="9" max="99" step="10">
        </p>
        """)
 
        class NumberFormWidAttrs(forms.Form):
            num = forms.DecimalField(widget=NumInput(attrs={'step': 12}))
        rendered = NumberFormWidAttrs().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input class=" form-control" type="number" name="num" id="id_num" min="9" max="99" step="12">
        </p>
        """)


    def test_checkbox(self):
        """<input type="checkbox">"""
        class CBForm(forms.Form):
            cb = forms.BooleanField()

        rendered = CBForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" >
        </p>
        """)

        form = CBForm(data={'cb': False})
        self.assertFalse(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li><small><font color="#ff0000">This field is required.</font></small></li>
        </ul>
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" >
        </p>
        """)

        form = CBForm(data={'cb': 1})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" checked="checked" value="1">
        </p>
        """)

        form = CBForm(data={'cb': True})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" checked>
        </p>
        """)

        form = CBForm(data={'cb': 'foo'})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" checked value="foo">
        </p>
        """)

    def test_select(self):
        """<select>"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
        )

        class SelectForm(forms.Form):
            select = forms.ChoiceField(choices=CHOICES)

        rendered = SelectForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_select">Select:</label>
            <select class="form-control" name="select" id="id_select" >
                <option value="en">English</option>
                <option value="de">Deutsch</option>
            </select>
        </p>
        """)

        rendered = SelectForm(initial={'select': 'en'}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_select">Select:</label>
            <select class="form-control" name="select" id="id_select" >
                <option value="en" selected="selected">English</option>
                <option value="de">Deutsch</option>
            </select>
        </p>
        """)

    def test_nbselect(self):
        """NullBooleanSelect"""
        class NBForm(forms.Form):
            nb = forms.NullBooleanField()

        rendered = NBForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_nb">Nb:</label>
            <select class="form-control" name="nb" id="id_nb" >
                <option value="1" selected>Unknown</option>
                <option value="2">Yes</option>
                <option value="3">No</option>
            </select>
        </p>
        """)

        rendered = NBForm(data={'nb': True}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_nb">Nb:</label>
            <select name="nb" id="id_nb" class="form-control">
                <option value="1">Unknown</option>
                <option value="2" selected="selected">Yes</option>
                <option value="3">No</option>
            </select>
        </p>
        """)

    def test_select_multiple(self):
        """<select multiple>"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
            ('fr', 'Francais'),
        )

        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(choices=CHOICES)

        rendered = MultiForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <select class="form-control" multiple="multiple" name="multi" id="id_multi" >
                <option value="en">English</option>
                <option value="de">Deutsch</option>
                <option value="fr">Francais</option>
            </select>
        </p>
        """)

        rendered = MultiForm(data={'multi': ['fr', 'en']}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <select class="form-control" name="multi" id="id_multi"  multiple="multiple" >
                <option value="en" selected="selected">English</option>
                <option value="de">Deutsch</option>
                <option value="fr" selected="selected">Francais</option>
            </select>
        </p>
        """)

    def test_select_multiple_values(self):
        """<select multiple>"""
        CHOICES = (
            ('1', 'English'),
            ('12', 'Deutsch'),
            ('123', 'Francais'),
        )

        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(choices=CHOICES)

        rendered = MultiForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <select name="multi"  class="form-control" id="id_multi" multiple="multiple">
                <option value="1">English</option>
                <option value="12">Deutsch</option>
                <option value="123">Francais</option>
            </select>
        </p>
        """)

        rendered = MultiForm(data={'multi': ['123']}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <select name="multi"  class="form-control" id="id_multi" multiple="multiple">
                <option value="1">English</option>
                <option value="12">Deutsch</option>
                <option value="123" selected="selected">Francais</option>
            </select>
        </p>
        """)

    def test_optgroup(self):
        """<optgroup> in select widgets"""
        CHOICES = (
            (None, (
                ('en', 'English'),
                ('de', 'Deutsch'),
                ('fr', 'Francais'),
            )),
            ("Asian", (
                ('jp', 'Japanese'),
                ('bn', 'Bengali'),
            )),
        )

        class LangForm(forms.Form):
            lang = forms.ChoiceField(choices=CHOICES)

        rendered = LangForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_lang">Lang:</label> 
            <select class="form-control" name="lang" id="id_lang">
            <optgroup label="None">
                <option value="en">English</option>
                <option value="de">Deutsch</option>
                <option value="fr">Francais</option>
            </optgroup>
            <optgroup label="Asian">
                <option value="jp">Japanese</option>
                <option value="bn">Bengali</option>
            </optgroup>
            </select>
        </p>""")

        rendered = LangForm(data={'lang': 'jp'}).as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_lang">Lang:</label> 
            <select class="form-control" name="lang" id="id_lang">
                <optgroup label="None">
                    <option value="en">English</option>
                    <option value="de">Deutsch</option>
                    <option value="fr">Francais</option>
                </optgroup>
                <optgroup label="Asian">
                    <option value="jp" selected="selected">Japanese</option>
                    <option value="bn">Bengali</option>
                </optgroup>
            </select>
        </p>""")

    def test_cb_multiple(self):
        """CheckboxSelectMultiple"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
            ('fr', 'Francais'),
        )
 
        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(
                choices=CHOICES,
                widget=forms.CheckboxSelectMultiple,
            )
 
        rendered = MultiForm().as_p()
 
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi_0">Multi:</label>
            <ul class="list-inline">
                <li><label class="checkbox-inline" for="id_multi_0"><input type="checkbox" id="id_multi_0" name="multi" value="en">English</label></li>
                <li><label class="checkbox-inline" for="id_multi_1"><input type="checkbox" id="id_multi_1" name="multi" value="de">Deutsch</label></li>
                <li><label class="checkbox-inline" for="id_multi_2"><input type="checkbox" id="id_multi_2" name="multi" value="fr">Francais</label></li>
            </ul>
        </p>
        """)
        rendered = MultiForm(data={'multi': ['fr', 'en']}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi_0">Multi:</label>
            <ul class="list-inline">
                <li><label class="checkbox-inline" for="id_multi_0"><input type="checkbox" id="id_multi_0" name="multi" value="en" checked="checked">English</label></li>
                <li><label class="checkbox-inline" for="id_multi_1"><input type="checkbox" id="id_multi_1" name="multi" value="de">Deutsch</label></li>
                <li><label class="checkbox-inline" for="id_multi_2"><input type="checkbox" id="id_multi_2" name="multi" value="fr" checked>Francais</label></li>
            </ul>
        </p>
        """)

    def test_checkbox_select_multiple_with_iterable_initial(self):
        """Passing iterable objects to initial data, not only lists or tuples.
        This is useful for ValuesQuerySet for instance."""
        choices = (
            ('en', 'En'),
            ('fr', 'Fr'),
            ('de', 'De'),
        )
 
        class iterable_choices(object):
            def __init__(self, choices):
                self.choices = choices
 
            def __iter__(self):
                for choice in self.choices:
                    yield choice
 
            def __len__(self):
                return len(self.choices)
 
        class Form(forms.Form):
            key = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                choices=choices,
            )
 
        form = Form(initial={'key': iterable_choices(['fr', 'en'])})
        self.assertHTMLEqual(form.as_p(), """
            <p><label for="id_key_0">Key:</label>
            <ul class="list-inline">
                <li><label class="checkbox-inline" for="id_key_0"><input id="id_key_0" name="key" type="checkbox" value="en" checked="checked">En</label></li>
                <li><label class="checkbox-inline" for="id_key_1"><input id="id_key_1" name="key" type="checkbox" value="fr" checked="checked">Fr</label></li>
                <li><label class="checkbox-inline" for="id_key_2"><input id="id_key_2" name="key" type="checkbox" value="de">De</label></li>
            </ul></p>
        """)

    def test_radio_select(self):
        """<input type="radio">"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
            ('fr', 'Francais'),
        )

        class RadioForm(forms.Form):
            radio = forms.ChoiceField(
                choices=CHOICES,
                widget=forms.RadioSelect,
            )

        rendered = RadioForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_radio_0">Radio:</label>
            <ul class="list-inline">
                <li><label class="radio-inline" for="id_radio_0"><input type="radio" name="radio" id="id_radio_0" value="en" >English</label></li>
                <li><label class="radio-inline" for="id_radio_1"><input type="radio" name="radio" id="id_radio_1" value="de" >Deutsch</label></li>
                <li><label class="radio-inline" for="id_radio_2"><input type="radio" name="radio" id="id_radio_2" value="fr" >Francais</label></li>
            </ul>
        </p>""")

        rendered = RadioForm(data={'radio': 'fr'}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_radio_0">Radio:</label>
            <ul class="list-inline">
                <li><label class="radio-inline" for="id_radio_0"><input type="radio" name="radio" id="id_radio_0" value="en" >English</label></li>
                <li><label class="radio-inline" for="id_radio_1"><input type="radio" name="radio" id="id_radio_1" value="de" >Deutsch</label></li>
                <li><label class="radio-inline" for="id_radio_2"><input type="radio" name="radio" id="id_radio_2" value="fr" checked>Francais</label></li>
            </ul>
        </p>""")

    def test_slug(self):
        """<input type="text" pattern="[-\w]+">"""
        class SlugForm(forms.Form):
            slug = forms.SlugField()

        rendered = SlugForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_slug">Slug:</label>
            <input  class=" form-control" type="text" name="slug" id="id_slug" >
        </p>""")
        self.assertFalse(SlugForm(data={'slug': '123 foo'}).is_valid())
        self.assertTrue(SlugForm(data={'slug': '123-foo'}).is_valid())

    def test_regex(self):
        """<input type="text" pattern="...">"""
        class RegexForm(forms.Form):
            re_field = forms.RegexField(r'^\d{3}-[a-z]+$',
                                        '\d{3}-[a-z]+')
            re_field_ = forms.RegexField(r'^[a-z]{2}$')

        rendered = RegexForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_re_field">Re field:</label>
            <input class=" form-control" type="text" name="re_field" id="id_re_field" pattern="\d{3}-[a-z]+" >
        </p><p>
            <label for="id_re_field_">Re field :</label>
            <input class=" form-control" type="text" name="re_field_" id="id_re_field_" >
        </p>""")

        self.assertFalse(RegexForm(data={'re_field': 'meh',
                                         're_field_': 'fr'}).is_valid())
        self.assertTrue(RegexForm(data={'re_field': '123-python',
                                        're_field_': 'fr'}).is_valid())

    def test_ip_address(self):
        """<input pattern="<IPv4 re>">"""
        class IPv4Form(forms.Form):
            ip = forms.IPAddressField()

        rendered = IPv4Form().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_ip">Ip:</label>
            <input class=" form-control" type="text" name="ip" pattern="%s" id="id_ip" >
        </p>""" % forms.IPAddressInput.ip_pattern)

        self.assertFalse(IPv4Form(data={'ip': '500.500.1.1'}).is_valid())
        self.assertTrue(IPv4Form(data={'ip': '250.100.1.8'}).is_valid())

    def test_generic_ip_address(self):
        """<input type=text>"""
        class GenericIPForm(forms.Form):
            ip = forms.GenericIPAddressField()

        rendered = GenericIPForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_ip">Ip:</label>
            <input class=" form-control" type="text" name="ip" id="id_ip" >
        </p>""")

    def test_typed_choice_field(self):
        """foo = forms.TypedChoiceField()"""
        TYPE_CHOICES = (
            (0, 'Some value'),
            (1, 'Other value'),
            (2, 'A third one'),
        )
        my_coerce = lambda val: bool(int(val))

        class TypedForm(forms.Form):
            typed = forms.TypedChoiceField(coerce=my_coerce,
                                           choices=TYPE_CHOICES)

        rendered = TypedForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_typed">Typed:</label>
            <select class="form-control" name="typed" id="id_typed" >
                <option value="0">Some value</option>
                <option value="1">Other value</option>
                <option value="2">A third one</option>
            </select>
        </p>""")

        form = TypedForm(data={'typed': '0'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['typed'], False)

    def test_file_path_field(self):
        """foo = forms.FilePathField()"""
        parent = os.path.join(os.path.dirname(__file__), '..')

        class PathForm(forms.Form):
            path = forms.FilePathField(path=parent, recursive=True)

        rendered = PathForm().as_p()
        self.assertTrue('<select ' in rendered, rendered)
        self.assertTrue(len(PathForm().fields['path'].choices) > 10)

    def test_typed_multiple_choice(self):
        """foo = forms.TypedMultipleChoiceField()"""
        TYPE_CHOICES = (
            (0, 'Some value'),
            (1, 'Other value'),
            (2, 'A third one'),
        )
        my_coerce = lambda val: bool(int(val))

        class TypedMultiForm(forms.Form):
            thing = forms.TypedMultipleChoiceField(coerce=my_coerce,
                                                   choices=TYPE_CHOICES)

        rendered = TypedMultiForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_thing">Thing:</label>
            <select class="form-control" name="thing" id="id_thing" multiple="multiple">
                <option value="0">Some value</option>
                <option value="1">Other value</option>
                <option value="2">A third one</option>
            </select>
        </p>""")

    def test_model_choice_field(self):
        """ModelChoiceField and ModelMultipleChoiceField"""
        SomeModel.objects.create(some_field='Meh')
        SomeModel.objects.create(some_field='Bah')

        class ModelChoiceForm(forms.Form):
            mod = forms.ModelChoiceField(queryset=SomeModel.objects.all())

        rendered = ModelChoiceForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_mod">Mod:</label>
            <select class="form-control" name="mod" id="id_mod" >
                <option selected="selected" value="">---------</option>
                <option value="1">Meh</option>
                <option value="2">Bah</option>
            </select>
        </p>""")

        rendered = ModelChoiceForm(data={'mod': 1}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_mod">Mod:</label>
            <select class="form-control" name="mod" id="id_mod" >
                <option value="">---------</option>
                <option value="1" selected="selected">Meh</option>
                <option value="2">Bah</option>
            </select>
        </p>""")

        class MultiModelForm(forms.Form):
            mods = forms.ModelMultipleChoiceField(queryset=SomeModel.objects.all())

        rendered = MultiModelForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_mods">Mods:</label>
            <select class="form-control" name="mods" id="id_mods" multiple>
                <option value="1">Meh</option>
                <option value="2">Bah</option>
            </select>
        </p>""")
        rendered = MultiModelForm(data={'mods': [1]}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_mods">Mods:</label>
            <select class="form-control" name="mods" id="id_mods" multiple="multiple">
                <option value="1" selected="selected">Meh</option>
                <option value="2">Bah</option>
            </select>
        </p>""")

    def test_combo_field(self):
        """Combo field"""
        class ComboForm(forms.Form):
            combo = forms.ComboField(fields=[forms.EmailField(),
                                             forms.CharField(max_length=10)])

        rendered = ComboForm().as_p()
        self.assertFalse(ComboForm(data={'combo': 'bob@exmpl.com'}).is_valid())
        self.assertTrue(ComboForm(data={'combo': 'bob@ex.com'}).is_valid())

    def test_split_datetime(self):
        """Split date time widget"""
        class SplitForm(forms.Form):
            split = forms.SplitDateTimeField()

        rendered = SplitForm().as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_split_0">Split:</label>
            <input type="text" name="split_0" id="id_split_0" />
            <input type="text" name="split_1" id="id_split_1" />
        </p>""")

        class SplitFormNotRequire(forms.Form):
            split = forms.SplitDateTimeField(required=False)
 
        rendered = SplitFormNotRequire().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_split_0">Split:</label>
            <input type="text" name="split_0" id="id_split_0" />
            <input type="text" name="split_1" id="id_split_1" />
        </p>""")
 
        valid = {'split_0': '2011-02-06', 'split_1': '12:12'}
        self.assertTrue(SplitForm(data=valid).is_valid())
 
        invalid = {'split_0': '2011-02-06', 'split_1': ''}
        self.assertFalse(SplitForm(data=invalid).is_valid())
 
        class SplitFormWidget(forms.Form):
            split = forms.SplitDateTimeField(
                widget=forms.SplitHiddenDateTimeWidget,
            )

        rendered = SplitFormWidget().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_split_0">Split:</label>
            <input type="text" name="split_0" id="id_split_0" />
            <input type="text" name="split_1" id="id_split_1" />
        </p>
        """)

    def test_multiple_hidden(self):
        """<input type="hidden"> for fields with a list of values"""

        some_choices = (
            ('foo', 'bar'),
            ('baz', 'meh'),
            ('heh', 'what?!'),
        )

        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput,
                                              choices=some_choices)

        rendered = MultiForm(data={'multi': ['heh', 'foo']}).as_p()
        self.assertHTMLEqual(rendered, """
        <input class=" form-control" id="id_multi" name="multi" type="hidden" value="['heh', 'foo']" />
        """)

    def test_datetime_with_initial(self):
        """SplitDateTimeWidget with an initial value"""
        value = now()
  
        class DateTimeForm(forms.Form):
            dt = forms.DateTimeField(initial=value,
                                     widget=forms.SplitDateTimeWidget)
  
        rendered = DateTimeForm().as_p()
        import time
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_dt_0">Dt:</label>
            <input type="text" name="dt_0" value="%s" id="id_dt_0">
            <input type="text" name="dt_1" value="%s" id="id_dt_1">
        </p>""" % (value.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S", time.localtime( time.time()))))


    def test_no_attrs_rendering(self):
        widget = forms.TextInput()
        try:
            rendered = widget.render('name', 'value')
            self.assertEqual(
                rendered,
                '<input type="text" name="name" value="value" class=" form-control" />',
            )
        except AttributeError:
            self.fail("Rendering with no attrs should work")

    def test_required_select(self):
        """The 'required' attribute on the Select widget"""
        choices = (('foo', 'foo'),
                   ('bar', 'bar'))

        class SelectForm(forms.Form):
            foo = forms.CharField(widget=forms.Select(choices=choices))

        rendered = SelectForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_foo">Foo:</label>
            <select class="form-control" id="id_foo" name="foo">
                <option value="foo">foo</option>
                <option value="bar">bar</option>
            </select>
        </p>""")

        class SelectFormWidget(forms.Form):
            foo = forms.CharField(widget=forms.Select(choices=choices),
                                  required=False)
 
        rendered = SelectFormWidget().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_foo">Foo:</label>
            <select class="form-control" name="foo" id="id_foo">
                <option value="foo">foo</option>
                <option value="bar">bar</option>
            </select>
        </p>""")

    def test_clearable_file_input(self):
        class Form(forms.Form):
            file_ = forms.FileField(required=False)

        fake_instance = {'url': 'test test'}
        rendered = Form(initial={'file_': fake_instance}).as_p()

        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label> <input type="file" name="file_" id="id_file_" />
        </p>""")

        form = Form(initial={'file_': fake_instance},
                    data={'file_-clear': True})
        self.assertTrue(form.is_valid())
        # file_ has been cleared
        self.assertFalse(form.cleaned_data['file_'])

    def test_rendered_file_input(self):
        class Form(forms.Form):
            file_ = forms.FileField()

            def clean_file_(self):
                raise forms.ValidationError('Some error')

        file_ = SimpleUploadedFile('name', b'some contents')

        form = Form(files={'file_': file_})
        valid = form.is_valid()
        self.assertFalse(valid)
        rendered = form.as_p()

        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li><small><font color="#ff0000">Some error</font></small></li>
        </ul>
        <p>
            <label for="id_file_">File :</label>
            <input id="id_file_" name="file_" type="file" >
        </p>""")

    def test_true_attr(self):
        """widgets with attrs={'foo': True} should render as <input foo>"""
        class Form(forms.Form):
            text = forms.CharField(widget=forms.TextInput(attrs={
                'foo': True,
                'bar': False,
            }))

        rendered = Form().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <input class=" form-control" type="text" foo="True" bar="False" id="id_text" name="text" >
        </p>""")


class WidgetRenderingTestWithTemplateStringIfInvalidSet(WidgetRenderingTest):
    pass

WidgetRenderingTestWithTemplateStringIfInvalidSet = override_settings(TEMPLATE_STRING_IF_INVALID=InvalidVariable(u'INVALID'))(WidgetRenderingTestWithTemplateStringIfInvalidSet)


class WidgetContextTests(TestCase):
    def test_widget_render_method_should_not_clutter_the_context(self):
        '''
        Make sure that the widget rendering pops the context as often as it
        pushed onto it. Otherwise this would lead to leaking variables into
        outer scopes.

        See issue #43 for more information.
        '''
        context = Context({
            'one': 1,
        })
        context_levels = len(context.dicts)
        widget = forms.TextInput()
        widget.context_instance = context
        widget.render('text', '')
        self.assertEqual(len(context.dicts), context_levels)
