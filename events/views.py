import stripe
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from events.serializers import EventSerializer, CommentSerializer
from events.models import Events, Comments
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView


stripe.api_key = 'sk_test_51KGQMoSHH8WqtIRyo6XGgOPRlC0HO7G8lvnFAb1CtPymhUjUOrCGDUSiDqCw5dZValm5FeOyduM0KAsXyVkqy27C00B4S7SURw'
endpoint_secret = "whsec_jgZliM2H6ycKmBzvttqVgNr3USAsFXpA"
YOUR_DOMAIN = 'http://localhost:8000'


# Create your views here.

class EventListCreateAPI(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    # queryset = Events.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        return Events.objects.all().filter(Q(created_by=self.request.user) | Q(published=True))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if data.get('start_date') >= data.get('end_date'):
                return Response({"start date should be less than end date"})
            else:
                instance = Events.objects.create(
                    title=data.get('title'),
                    description=data.get('description'),
                    location=data.get('location'),
                    start_date=data.get('start_date'),
                    end_date=data.get('end_date'),
                    category=data.get('category'),
                )
                instance.created_by = self.request.user

                files = [file for file in request.FILES]
                image = request.FILES.get(files[0])
                instance.image = image
                instance.save()

        else:
            return Response({"all fields are required"})

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class MyEventListCreateAPI(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_queryset(self):
        events= Events.objects.all().filter(Q(created_by=self.request.user) & Q(published=False))
        return events

class EventListApi(ListAPIView):

    permission_classes = [AllowAny]
    queryset = Events.objects.all().filter(published=True)
    serializer_class = EventSerializer

class EventDetailUpdateAPI(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        events= Events.objects.all().filter(Q(created_by=self.request.user))
        return events

    def update(self, request, *args, **kwargs):
        partial = False
        if 'PATCH' in request.method:
            partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            data = serializer.validated_data
            instance.title = data.get('title', instance.title)
            instance.description = data.get('description', instance.description)
            instance.location = data.get('location', instance.location)
            instance.start_date = data.get('start_date', instance.start_date)
            instance.end_date = data.get('end_date', instance.end_date)
            instance.category = data.get('category', instance.category)

            if instance.start_date >= instance.end_date:
                return Response({"Start date should be less than end date"})
            else:
                if request.FILES:
                    files = [file for file in request.FILES]
                    image = request.FILES.get(files[0])
                    instance.image = image
                    instance.save()
            serializer.save()
        else:
            return Response({"enter valid data"})
        return Response(serializer.data)


class EventsDetailAPI(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Events.objects.all().filter(published=True)
    serializer_class = EventSerializer
    lookup_field = 'pk'


class CommentListAPI(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        url=self.request.path.split('/')
        event_id = (url[3])
        return Comments.objects.all().filter(event=event_id)

    def perform_create(self, serializer):
        url = self.request.path.split('/')
        event_id = (url[3])
        serializer.save(created_by=self.request.user, event=Events.objects.get(id=event_id))

class CommentDetailAPI(RetrieveUpdateDestroyAPIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comments.objects.all().filter(created_by=self.request.user)


@api_view(['GET'])
def PublishEvent(request, pk):

    if not request.user.is_authenticated:
        return Response({'Not Authorised'})
    else:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Events',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/api/pay_success/{0}/'.format(pk),
        cancel_url=YOUR_DOMAIN + '/pay_fail/',
        )
        print(checkout_session.id)
        return Response(checkout_session.url)

@api_view(['GET'])
def fullfill_order(request,pk):

    event = Events.objects.get(id=pk)
    event.published = True
    event.save()
    return Response({"Your Event is successfully published"})

@api_view(['GET'])
def cancel_order(request):

    if not request.user.is_authenticated:
        return Response({'Not Authorised'})
    else:
        return Response({"Your operation is failed Please Try Again"})