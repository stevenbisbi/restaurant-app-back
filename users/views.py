from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from drf_yasg import openapi # type: ignore

from .serializer import UserSerializer, CustomerSerializer, LoginSerializer, StaffSerializer
from .models import Customer, Staff

User = get_user_model()

# Permiso personalizado: Solo dueño o admin
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin tiene acceso completo
        if request.user.is_superuser:
            return True
            
        # Cliente solo puede acceder a su propio perfil
        if hasattr(request.user, 'customer'):
            return obj.user == request.user
            
        # Staff también podría necesitar acceso
        if hasattr(request.user, 'staff'):
            return obj.user == request.user
            
        return False


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  authentication_classes = [TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]
  
  def get_permissions(self):
        if self.action in ['create', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]

 # Vista para obtener el perfil del cliente autenticado
class CustomerProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Obtener perfil del cliente autenticado
            customer = request.user.customer
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Perfil de cliente no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_permissions(self):
        if self.action == 'create':
            # Cualquiera puede crear cliente
            return [AllowAny()]
        elif self.action == 'list':
            # Solo admin puede ver lista completa
            return [IsAuthenticated(), IsAdminUser()]
        else:
            # Detalle/actualización: solo dueño o admin
            return [IsAuthenticated(), IsOwnerOrAdmin()]


class LoginView(APIView):
  permission_classes = []
  authentication_classes = []

  @swagger_auto_schema(
    request_body = LoginSerializer,
    responses = {
      200: openapi.Response("Exito", schema=UserSerializer),
      400: openapi.Response("Error", schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        proferties = {'error': openapi.Schema(type=openapi.TYPE_STRING)}
      )),
    }
  )

  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
      return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    user_serializer = UserSerializer(user)

    # 🔽 NUEVO: buscamos el customer (si existe)
    customer_data = None
    if hasattr(user, 'customer'):
      customer = user.customer
      customer_data = {"id": str(customer.id)}

    return Response({
      "token": token.key,
      "user": user_serializer.data,
      "customer": CustomerSerializer(user.customer).data if hasattr(user, "customer") else None
    })


class StaffViewSet(viewsets.ModelViewSet):
  queryset = Staff.objects.all()
  serializer_class =  StaffSerializer
  authentication_classes = [TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

