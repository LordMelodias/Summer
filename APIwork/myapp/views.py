from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from .serializers import ItemSerializer
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def getdata(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST', 'PUT', 'DELETE'])
def manage_item(request, pk=None):
    # Add Item
    if request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Update Item
    if request.method == 'PUT':
        if pk is None:
            return Response({"error": "Item ID is required for updating."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete Item
    if request.method == 'DELETE':
        if pk is None:
            return Response({"error": "Item ID is required for deleting."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  