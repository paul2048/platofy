from .models import Topic

def top_topics(request):
    """ Returns the names of the top 8 topics """
    return {
        'top_topics': Topic.objects.all().order_by('-times_used')[:8].values_list('name', flat=True)
    }