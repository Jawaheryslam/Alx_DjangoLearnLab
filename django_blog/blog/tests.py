from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.post = Post.objects.create(
                title='Test',
                conent='Hello world',
                author=self.user,
                published=True
        )

    def test_list_view(self):
        resp = self.client.get(reverse('blog:post-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test')

    def test_detail_view(self):
        resp = self.client.get(reverse('blog:post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello world')

    def test_create_requires_login(self):
        resp = self.client.get(reverse('blog:post-create'))
        self.assertNotEqual(resp.status_code, 200)

        # Login and try again
        self.client.login(username='author', password='pass')
        rsp = self.client.get(reverse('blog:post-create'))
        self.assertEqual(resp.status_code, 200)

    def test_update_only_author(self):

        # other user cannot edit
        self.client.login(username='author', password='pass')
        resp = self.client.get(reverse('blog:post-update', kwargs={'pk': self.post.pk}))
        self.assertNotEqual(resp.status_code, 200)

        # author can edit
        self.client.login(username='author', password='pass')
        resp = self.client.get(reverse('blog:post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_delete_only_author(self):
        self.client.login(username='other', password='pass')
        resp = self.client.get(reverse('blog:post-delete', kwargs={'pk': self.post.pk}))
        self.assertNotEqual(resp.status_code, 200)


class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.post = Post.objects.create(title='Test', content='Hello', author=self.user, published=True)

    def test_add_comment_requires_login(self):
        url = reverse('blog:comment-create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'Nice post'})
        self.assertNotEqual(resp.status_code, 200)  # should redirect to login
        self.client.login(username='other', password='pass')  # login & post
        resp = self.client.post(url, {'content': 'Nice post'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Nice post')
        self.assertEqual(self.post.comment.count(), 1)

    def test_edit_comment_only_author(self):
        comment = Comment.objects.create(post=self.post, author=self.other, content='I am other')
        url = reverse('blog:comment-update', kwargs={'pk': comment.pk})

        resp = self.client.get(url)  # not logged in
        self.assertNotEqual(resp.status_code, 200)

        self.client.login(username='author', password='pass') # logged is as user
        resp = self.client.get(url)
        self.assertNotEqual(resp.status_code, 200)

        self.client.login(username='other', password='pass')  # logged in as comment author
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_delete_comment_only_author(self):
        comment = Comment.objects.create(post=self.post, author=self.other, content='Delete me')
        url = reverse('blog:comment-delete', kwargs={'pk': comment.pk})
        self.client.login(username='author', password='pass')
        resp = self.client.get(url)
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username='other', password='pass')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
