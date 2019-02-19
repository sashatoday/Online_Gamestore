from django.test import TestCase

class SearchGameTest(TestCase):    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/search_game/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get('/search_game/')
        self.assertTemplateUsed(response, 'games/search_game.html')
        
    def test_search_finds_game(self):
        response = self.client.get('/search_game/')
        response = self.client.get(reverse('authors')+'?page=2')
