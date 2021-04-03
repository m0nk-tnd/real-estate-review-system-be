from django.shortcuts import render


def handler404(request, exception):
    all_urls = exception.args[0]['tried']

    path = exception.args[0]['path']

    urlpatterns = [
        url
        for url in all_urls
        if str(url[0].pattern) in path or path in str(url[0].pattern)
    ]

    data = {
        'urlpatterns': urlpatterns or all_urls,
    }

    return render(request, '404.html', context=data)
