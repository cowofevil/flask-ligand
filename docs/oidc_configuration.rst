.. rstcheck: ignore-roles=oidc,auth0

OpenID Connect Configuration
============================

``flask-ligand`` uses :doc:`flask-jwt-extended <flask-jwt-extended:basic_usage>` for authorization and authentication
with and `IAM`_ that supports the :oidc:`OpenID Connect (OIDC) <>` protocol. The ``OIDC_DISCOVERY_URL``
`environment variable`_ is used to specify the
:oidc:`OIDC discovery URL <specs/openid-connect-discovery-1_0.html#ProviderConfigurationRequest>`. Below are links to
popular `IAM`_ solutions documentation on how to obtain the
:oidc:`OIDC discovery URL <specs/openid-connect-discovery-1_0.html#ProviderConfigurationRequest>`:

- `Keycloak`_ (Realm Settings -> Endpoints -> OpenID Endpoint Configuration)
- :auth0:`Auth0 <docs/get-started/applications/application-settings#endpoints>`
- `Microsoft Azure Active Directory`_
- `AWS IAM`_

.. _IAM: https://www.crowdstrike.com/cybersecurity-101/identity-access-management-iam/
.. _`environment variable`: configuration.html#prod
.. _`Microsoft Azure Active Directory`: https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-protocols-oidc
.. _Keycloak: https://www.keycloak.org/docs/latest/server_admin/#using-the-admin-console
.. _`AWS IAM`: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html
