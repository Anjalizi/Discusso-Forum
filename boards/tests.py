from django.core.urlresolvers import reverse
from django.test import TestCase
from .views import home, board_topics, topic_posts
from django.urls import resolve, reverse
from .models import Board, Topic, Post

from django.contrib.auth.models import User

class HomeTests(TestCase):
	def setUp(self):
		self.board = Board.objects.create(Name='Mathematics', Description='This is the forum for Mathematics')
		url = reverse('home')
		self.response = self.client.get(url)

	def test_home_url_resolves_home_view(self):
		view = resolve('/')
		self.assertEquals(view.func, home)

	def test_home_view_status_code(self):
		self.assertEquals(self.response.status_code, 200) #status code 200 means success, 500 means internal server error

	def test_home_view_contains_link_to_topics_page(self):
		board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
		self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
	def setUp(self):
		Board.objects.create(Name='Mathematics', Description='This is the forum for Mathematics')

	def test_board_topics_view_contains_link_back_to_homepage(self):
		board_topics_url = reverse('board_topics', kwargs={'pk': 1})
		response = self.client.get(board_topics_url)
		homepage_url = reverse('home')
		self.assertContains(response, 'href="{0}"'.format(homepage_url))

	def test_board_topics_view_success_status_code(self):
		url = reverse('board_topics', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_board_topics_view_not_found_status_code(self):
		url = reverse('board_topics', kwargs={'pk': 99})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_board_topics_url_resolves_board_topics_view(self):
		view = resolve('/boards/1/')
		self.assertEquals(view.func, board_topics)

class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(Name='Django', Description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        topic = Topic.objects.create(subject='Hello, world', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func, topic_posts)