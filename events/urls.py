from django.urls import path
from events.views import EventListCreateAPI,\
    EventListApi,\
    EventDetailUpdateAPI,\
    EventsDetailAPI,\
    MyEventListCreateAPI,\
    CommentListAPI,\
    CommentDetailAPI, PublishEvent, fullfill_order, cancel_order


app_name = "events"

urlpatterns = [
    path('events/', EventListCreateAPI.as_view(), name='event_list_create'),
    path('my_events/', MyEventListCreateAPI.as_view(), name='my_event_list'),
    path('events_home/', EventListApi.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailUpdateAPI.as_view(), name='event_detail_update'),
    path('events_home/<int:pk>/', EventsDetailAPI.as_view(), name='event_detail'),
    path('events/<int:pk>/comments', CommentListAPI.as_view(), name= 'comment_list'),
    path('comments/<int:pk>/', CommentDetailAPI.as_view(), name='comment_detail'),
    path('payment/<str:pk>/', PublishEvent, name="pay"),
    path('pay_success/<str:pk>/', fullfill_order, name="fullfill"),
    path('pay_fail/', cancel_order, name="fail"),
]