from test2021.models import Post

def notification(request):
    posts = Post.objects.all().order_by('-pub_date')
    if posts:
        context = {
            'latest_post' : posts[0]
        }
    else:
        context = {
            'latest_post' : ""
        }

    return context
