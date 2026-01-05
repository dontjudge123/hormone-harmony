from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
from django.template import Template, Context
from .models import PeriodCycle


class PeriodCycleTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(username='tester', password='password')

	def test_model_creation(self):
		p = PeriodCycle.objects.create(user=self.user, start_date='2023-01-01', cycle_length=28)
		self.assertEqual(p.cycle_length, 28)

	def test_view_requires_login(self):
		url = reverse('core:period')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)

	def test_post_creates_periodcycle(self):
		self.client.login(username='tester', password='password')
		url = reverse('core:period')
		response = self.client.post(url, {'start_date': '2023-02-01', 'cycle_length': 27})
		self.assertEqual(response.status_code, 302)
		self.assertTrue(PeriodCycle.objects.filter(user=self.user, cycle_length=27).exists())

	def test_post_with_end_date_sets_cycle_length(self):
		self.client.login(username='tester', password='password')
		url = reverse('core:period')
		response = self.client.post(url, {'start_date': '2023-03-01', 'end_date': '2023-03-05'})
		self.assertEqual(response.status_code, 302)
		self.assertTrue(PeriodCycle.objects.filter(user=self.user, cycle_length=5).exists())

	def test_end_date_property(self):
		p = PeriodCycle.objects.create(user=self.user, start_date='2024-01-01', cycle_length=7)
		self.assertEqual(str(p.end_date), '2024-01-07')

	def test_predicted_next_period_shown(self):
		# create two cycles and verify prediction shows next start
		PeriodCycle.objects.create(user=self.user, start_date='2024-01-01', cycle_length=28)
		PeriodCycle.objects.create(user=self.user, start_date='2024-01-29', cycle_length=28)
		self.client.login(username='tester', password='password')
		url = reverse('core:period')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		# prediction should be last start_date + cycle_length = 2024-02-26
		self.assertEqual(response.context.get('predicted_next_period'), '2024-02-26')

class TemplateTagTests(TestCase):
    def test_add_class_appends_to_existing(self):
        class DummyForm(forms.Form):
            name = forms.CharField(widget=forms.TextInput(attrs={'class': 'existing'}))

        form = DummyForm()
        tpl = Template('{% load form_tags %}{{ form.name|add_class:"new" }}')
        rendered = tpl.render(Context({'form': form}))
        self.assertIn('class="existing new"', rendered)

    def test_add_class_creates_when_missing(self):
        class DummyForm(forms.Form):
            name = forms.CharField(widget=forms.TextInput())

        form = DummyForm()
        tpl = Template('{% load form_tags %}{{ form.name|add_class:"new" }}')
        rendered = tpl.render(Context({'form': form}))
        self.assertIn('class="new"', rendered)