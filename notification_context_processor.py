from board.models import Post

def notification(request):
    posts = Post.objects.all().order_by('-mod_date')
    if posts:
        context = {
            'latest_post' : posts[0]
        }
    else:
        context = {
            'latest_post' : ""
        }

    return context
