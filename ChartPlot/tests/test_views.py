from django.test import TestCase
from django.urls import reverse


class ChartViewTestCase(TestCase):
    
    views_name = ('home', 'create', 'edit', 'detail', 'delete')
    app_name = 'ChartPlot'
    
    
    def test_status_code(self):
        for view in self.views_name:
            response = self.client.get(reverse(f'{self.app_name}:{view}'))
            self.assertEqual(response.status_code, 200)
    
    
    def test_tamplate_used(self):
        for view in self.views_name:
            if view != 'delete':
                response = self.client.get(reverse(f'{self.app_name}:{view}'))
                self.assertTemplateUsed(response, f'{self.app_name}/{view}.html')
