from django.contrib import admin
from django.urls import path, include
from .views import *
from .api import *

urlpatterns = [
    path('', HomeView.as_view()),

    path('ticket', TicketView.as_view(), name = 'ticket'),
    path('ticket/delete_ticket/<int:id>', delete_ticket),
    path('ticket/payment_detail/<int:id>', payment_detail, name='payment_detail'),
    path('ticket_detail/<int:id>', ticket_detail, name='ticket_detail'),

    path('schedule', ShowtimeView.as_view(), name='schedule'),
    path('add_showtime', AddShowtimeView.as_view(), name='add_showtime'),
    path('update_showtime/<int:id>', update_showtime, name = 'update_showtime'),
    path('delete_showtime/<int:id>', delete_showtime),

    path("statistics/", statistic_view, name = "statistics"),
    path("chart/filter-option/", filter_option, name="chart_filter_options"),
    path("chart/sales/<int:year>/", get_sale_chart, name="chart_sales"),

    # path('list_showtime', ListShowtimeView.as_view())

    # path('api/get_film', api_get_movies),
    # path('api/post_film', api_post_movie),
    # path('api/update_film/<str:id>', api_update_movie),
    # path('api/delete_film/<str:id>', api_delete_movie),

]