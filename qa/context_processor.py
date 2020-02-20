from .models import Topic

def top_topics(request):
    return {
        'top_topics': Topic.objects.all().order_by('-times_used')[:8]
    }