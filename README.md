**All endpoints**

**Merchant Endpoint:**

| URL                               | Method | Serializer                           | Logic                                                                            | Permission                               | App  |
|-----------------------------------|--------|--------------------------------------|----------------------------------------------------------------------------------|------------------------------------------|------|
| /api/v1/we/organizations/default/ | Post   | PrivateOrganizationDefaultSerializer | Merchant change their organization. Just pass the organization**uid** in payload | IsOrganization                           | weio |
| /api/v1/we/organizations/user/    | Post   | PrivateOrganizationSerializer        | Merchant can add user into a organization                                        | IsAuthenticated and role admin and staff | weio |
| /api/v1/we/products/              | Post   | PrivateProductSerializers            | Merchant can add product                                                         | IsOrganization                           | weio |
| /api/v1/we/search/product/        | Post   | PrivateBaseProductSearchSerializers  | Merchant can search base product                                                 | IsOrganizationStaff                      | weio |

**Customer Endpoint:**

| URL                      | Method                    | Serializer                                   | Logic                                                                               | Permission      | App  |
|--------------------------|---------------------------|----------------------------------------------|-------------------------------------------------------------------------------------|-----------------|------|
| /api/v1/me/addresses/    | Get,Post,Put,Delete(soft) | PublicAddressSerializers                     | Customer can make operation CRUD their address                                      | IsAuthenticated | meio |
| /api/v1/me/cart/         | Get,Post                  | PrivateAddToCart (Post),   PrivateCarts(Get) | Customer can add product/update product quantity/ can see the cart products         | IsAuthenticated | meio |
| /api/v1/me/order/        | Post                      | PublicOrderSerializer                        | Customer can add products to orders which is come from the cart                     | IsAuthenticated | meio |
| /api/v1/me/organization/ | Post                      | PublicOrganization                           | Customer can send request with their organization to django-admin and role of owner | IsAuthenticated | meio |

**Global Endpoint:**

| URL                         | Method | Serializer                                 | Logic                                                      | Permission | App  |
|-----------------------------|--------|--------------------------------------------|------------------------------------------------------------|------------|------|
| /api/v1/auth/registration/  | Post   | PublicUserRegistrationSerializer           | A user can register                                        |            | core |
| /api/v1/auth/token/         | Post   | TokenRefreshView (default by SimpleJWT)    | A user get access and refresh token                        |            | core |
| /api/v1/auth/token/logout/  | Post   | LogoutView (default by SimpleJWT)          | A user can logout from the server                          |            | core |
| /api/v1/auth/token/refresh/ | Post   | TokenObtainPairView (default by SimpleJWT) | A user can access and refresh token from the refresh token |            | core |
