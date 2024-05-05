from package.serializers import PackageSerializer
from .models import Package
from rest_framework.generics import RetrieveAPIView

class Package(RetrieveAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = 'id'