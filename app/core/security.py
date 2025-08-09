from fastapi.security import OAuth2PasswordBearer, HTTPBearer


oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# class AccessTokenBearer(HTTPBearer):
#     async def __call__(self, request):
#         auth_credentials = await super().__call__(request)
#         token = auth_credentials.credentials
#         token_data = verify_access_token(token)
#
#         return token_data
#
#
#
# access_token_bearer = AccessTokenBearer()