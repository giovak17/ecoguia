from core.models import Usuarios 
from django.shortcuts import redirect

# def login_required(view_func, role):
#     def _wrapped_view(request, *args, **kwargs):
#         if 'user_id' not in request.session:
#             return redirect('usuarios:login')  # or return a 403
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view

def login_required(role="usuario"): 
    def decorator(view_func): 
        def _wrapped_view(request, *args, **kwargs):
            if 'user_id' not in request.session:
                return redirect('usuarios:login')

            # id del rol de usuario por defecto
            id_rol = 2
            match role:
                case "administrador":
                    # id del rol de administrador
                    id_rol = 1
                case "recicladora":
                    # id del rol de recicladora
                    id_rol = 3

            if request.user.id_rol.id_rol != id_rol:
                return redirect('usuarios:login')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

class SimpleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        request.user = None
        if user_id:
            try:
                request.user = Usuarios.objects.get(pk=user_id)
            except Usuarios.DoesNotExist:
                pass
        return self.get_response(request)
