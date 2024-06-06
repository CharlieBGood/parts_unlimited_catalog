from collections import defaultdict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from parts.models import Part
from parts.serializers import PartsSerializer

class PartsViewSet(viewsets.ModelViewSet):
    """
    Parts viewset
    """
    serializer_class = PartsSerializer
    queryset = Part.objects.all()

    @action(detail=False, url_path='most-common-words')
    def most_common_words(self, _):
        words = defaultdict(int)

        for description in self.queryset.values_list('description', flat=True):
            description_words = description.split()

            for word in description_words:
                words[word] += 1

        repeated_words_ranking = [word[0] for word in sorted(words.items(), key=lambda item: item[1], reverse=True)]

        return Response({'most_common_words': repeated_words_ranking[0:5]})
