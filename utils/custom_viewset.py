from rest_framework import permissions, status, views,viewsets
from utils.response_wrapper import ResponseWrapper

class CustomViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'

    # ..........***.......... Get All Data ..........***..........
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance = qs, many = True)
        return ResponseWrapper(data = serializer.data, msg='Success')

    # ..........***.......... Create ..........***..........
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            qs = serializer.save()
            return ResponseWrapper(data=serializer.data, msg='created')
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    # ..........***.......... Update ..........***..........
    def update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    # ..........***.......... Delete ..........***..........
    def destroy(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", error_code=400)

    # ..........***.......... Get Single Data ..........***..........

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseWrapper(serializer.data)