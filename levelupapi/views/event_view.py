from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Event, Gamer

class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def list(self, request):

        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """

        try:
            authenticated_player = Gamer.objects.get(user=request.auth.user)

        except Gamer.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            game = Game.objects.get(pk=request.data['game'])
        except Game.DoesNotExist:
            return Response({'message': 'You sent an invalid game ID'}, status=status.HTTP_404_NOT_FOUND)
        
        event = Event.objects.create(
            date_of_event=request.data["date_of_event"],
            start_time=request.data["start_time"],
            location=request.data["location"],
            host=authenticated_player,
            game=game
        )
        
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'date_of_event', 'start_time', 'location', 'game', 'host', 'attendees')