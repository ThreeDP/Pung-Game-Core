from django.http import JsonResponse

def info_controller(request, name):
    if (request.method == "GET"):
        test = {
                "title": "test1",
                "pub_date": "article.pub_date.strftime",
                "author": "article.author.name"
            }
        
        if (name == 1):
            test =  {
                "title": "test2",
                "pub_date": "article.pub_date.strftime",
                "author": "article.author.name"
            }
        articles_data = [
            test
        ]

        context = {
            "method": request.method,
            "articles": articles_data
        }
        return JsonResponse(context)
    return JsonResponse({"error": "Not Found"}, status=404)