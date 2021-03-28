from django.shortcuts import render
from django.conf import settings
import requests
import random

def index(request):

    books = []

    # Google Books API
    if request.method == 'POST':
        if request.POST['submit'] == 'search':
            url = 'https://www.googleapis.com/books/v1/volumes'

            search_params = {
                'q' : request.POST['search'],
                'key' : settings.GOOGLE_BOOK_API_KEY,
                'printType' : books,
                'maxResults' : 8
            }

            r = requests.get(url,params=search_params)
            results = r.json()['items']

            for result in results:
                try:
                    books_data = {'author': result['volumeInfo']['authors'][0]}
                except :
                    books_data = {
                        'title': result['volumeInfo']['title'],
                        'image': result['volumeInfo']['imageLinks']['thumbnail'],
                        'author': 'No Author'
                    }
                else:
                    books_data = {
                        'title': result['volumeInfo']['title'],
                        'image': result['volumeInfo']['imageLinks']['thumbnail'],
                        'author': result['volumeInfo']['authors'][0]
                        # 'description': result['searchInfo']['textSnippet']
                        #'product_url': result['saleInfo']['buyLink']
                    }
                    
                books.append(books_data)

            context = {
                    'books' : books
                }

            return render(request, 'search/index.html', context)

        elif request.POST['submit'] == 'lucky':
            random_number = random.randint(0,7)

            url = 'https://www.googleapis.com/books/v1/volumes'

            search_params = {
                'q' : request.POST['search'],
                'key' : settings.GOOGLE_BOOK_API_KEY,
                'printType' : books,
                'maxResults' : 8
            }

            r = requests.get(url,params=search_params)
            result = r.json()['items'][random_number]

            try:
                book_data = {'author': result['volumeInfo']['authors'][0]}
            except :
                book_data = {
                    'title': result['volumeInfo']['title'],
                    'image': result['volumeInfo']['imageLinks']['thumbnail'],
                    'author': 'No Author'
                }
            else:
                book_data = {
                    'title': result['volumeInfo']['title'],
                    'image': result['volumeInfo']['imageLinks']['thumbnail'],
                    'author': result['volumeInfo']['authors'][0]
                    # 'description': result['searchInfo']['textSnippet']
                    #'product_url': result['saleInfo']['buyLink']
                    }

            books.append(book_data)

            context = {
                'books' : books
            }
       

            return render(request, 'search/index.html', context)

    # New York Times Book API
    else:
        url = 'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction'

        search_params = {
                'api-key' : settings.NY_TIMES_API_KEY,
                'num_results' : 8
            }

        r = requests.get(url,params=search_params)
        results = r.json()['results']['books']

        for result in results:
            books_data = {
                'title' : result['title'],
                'image': result['book_image'],
                'author': result['author'],
                'description': result['description'],
                'product_url': result['amazon_product_url']
            }
            books.append(books_data)

        context = {
                'books' : books
            }

        return render(request, 'search/index.html', context)
