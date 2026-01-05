from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
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
