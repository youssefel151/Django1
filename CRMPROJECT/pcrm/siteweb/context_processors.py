from .authz import get_user_role
from .models import Etudiant, Profile


def user_role(request):
    role = get_user_role(request.user)
    current_student = None
    if role == Profile.ROLE_ETUDIANT:
        current_student = Etudiant.objects.filter(email__iexact=request.user.email).first()

    return {
        'current_student': current_student,
        'user_role': role,
    }
