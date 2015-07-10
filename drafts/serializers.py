from rest_framework import serializers
from drafts.models import Document, Draft


class DraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Draft
        fields = ('title', 'text', 'version', 'date_created')


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('hashid', 'latest_title', 'date_created')
