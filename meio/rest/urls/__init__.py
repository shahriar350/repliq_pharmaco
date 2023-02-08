from django.urls import path, include

app_name = 'me'

urlpatterns = [
	path('cart/', include('meio.rest.urls.carts')),
	path('order/', include('meio.rest.urls.orders')),
	path('addresses/', include('meio.rest.urls.addresses')),
	path('organization/', include('meio.rest.urls.organizations'))

]
