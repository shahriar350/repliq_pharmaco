from django.urls import path, include

app_name = 'we'
urlpatterns = [
    path('organizations/', include('weio.rest.urls.organizations')),
    path('products/', include('weio.rest.urls.products')),
    path('search/', include('weio.rest.urls.search')),

]
