import collections

from rest_framework import serializers
from events.models import Events, Comments

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = [
            'id',
            'comment',
            'created_at',
            'event',
            'created_by'
        ]

class EventSerializer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Events
        # depth = 1
        fields = ['id',
                  'title',
                  'description',
                  'location',
                  'start_date',
                  'end_date',
                  'category',
                  'image',
                  'published',
                  'created_by'
                  ]
        read_only_fields = ['published']

    def get_created_by(self, obj):
        print(collections.OrderedDict)
        return obj.created_by.username
        # return "hi"


