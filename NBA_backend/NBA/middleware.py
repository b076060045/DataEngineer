from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import jwt
from django.conf import settings


class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        whitelist = ["/login"]  # 可自由擴充

        if request.path in whitelist:
            return  # 放行，不做驗證

        token = request.COOKIES.get("jwt_token")
        if not token or not self.is_valid_token(token):
            return JsonResponse({"error": "Unauthorized"}, status=401)

    def is_valid_token(self, token):
        try:
            # 嘗試用 SECRET_KEY 解碼 token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # 驗證成功，回傳 True
            return True
        except jwt.ExpiredSignatureError:
            # token 過期
            return False
        except jwt.InvalidTokenError:
            # token 無效
            return False
