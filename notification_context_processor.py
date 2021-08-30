from board.models import Post

def notification(request):
	posts = Post.objects.all().order_by('-mod_date')
	context = {
		'latest_post' : posts[0]
	}

	return context
