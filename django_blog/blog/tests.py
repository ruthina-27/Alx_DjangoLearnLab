from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.published_date)

    def test_post_str_representation(self):
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )
        self.assertEqual(str(post), 'Test Post')
