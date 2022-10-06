.. rstcheck: ignore-roles=auth0

=============
Auth0 Support
=============

This guide will cover how to configure :auth0:`Auth0 <>` for use with ``flask-ligand``. Given the configurability of
Auth0, this guide will only cover a narrow example that is for demonstration purposes only. The sections below will
guide you through the steps needed to fully configure Auth0 by linking to the pertinent
:auth0:`Auth0 documentation <docs>`.

.. important:: It is highly encouraged that the :auth0:`Auth0 documentation <docs>` be consulted in depth before using
    ``flask-ligand`` + :auth0:`Auth0 <>` in a production environment.

User(s) and Role(s)
===================

The ``flask-ligand``'s RBAC support requires roles to be associated with clients (a.k.a
:auth0:`API <docs/get-started/auth0-overview/set-up-apis>`).
:auth0:`Auth0 has a built-in RBAC system <docs/manage-users/access-control/rbac>` , but this guide will not be using
will only be using certain aspects of the system. Another limitation that needs to noted is that Auth0 only
supports associating roles with users which means that
:auth0:`machine-to-machine flows <docs/customize/actions/flows-and-triggers/machine-to-machine-flow>` will have to use a
specific user to add roles to a particular :auth0:`API <docs/get-started/auth0-overview/set-up-apis>`).

1. :auth0:`Create the roles <docs/manage-users/access-control/configure-core-rbac/roles/create-roles>` 'admin' and
   'user'. (Defaults for ``flask-ligand``, but you can define your own.)
2. :auth0:`Create a user <docs/manage-users/user-accounts/create-users>` 'test@test.com' with a
   :auth0:`Username-Password-Authentication connection <docs/authenticate/database-connections>`
3. :auth0:`Assign <docs/manage-users/access-control/configure-core-rbac/rbac-users/assign-roles-to-users>` the
   'admin' role to the 'test' user .

Application and APIs
====================

:auth0:`Auth0 applications <docs/get-started/applications>` are the core of adding authentication to your web app,
mobile device or microservice. An API will allow a ``flask-ligand`` microservice to authenticate with an Auth0
application. In Auth0 this is called the
":auth0:`machine-to-machine flow <docs/customize/actions/flows-and-triggers/machine-to-machine-flow>`"

1. Create the "flask-ligand" application.
2. Configure "flask-ligand" to be a
   :auth0:`Machine to Machine <docs/get-started/applications/application-settings#application-properties>`
   application type.
3. Configure "flask-ligand" with **only** the following :auth0:`grant types <docs/get-started/applications/application-grant-types#spec-conforming-grants>`:
    a. ``client_credentials``
    b. ``password`` (Required for RBAC support)
4. Create the "flask-ligand-mtm" :auth0:`API <docs/get-started/auth0-overview/set-up-apis>`.
    a. **Note**:
    :auth0:`Enabling RBAC will have no affect <docs/get-started/apis/enable-role-based-access-control-for-apis>`!
5. :auth0:`Associate <docs/get-started/apis/api-settings#machine-to-machine-applications>` the "flask-ligand-mtm"
   API to the "flask-ligand" application.

Auth Pipeline Rule
==================

Using :auth0:`Auth0 rules <https://auth0.com/docs/customize/rules>`, the roles associated with a particular user can be
added to the ID and access tokens. (It is not strictly necessary to add roles to the ID token, so you can choose to
not add the roles if it doesn't fit your needs)

1. Create a :auth0:`rule <docs/customize/rules/create-rules>` named "Add User Roles to ID and Access Tokens".
2. Copy the following script into the rule:

    .. code-block:: javascript

        function (user, context, callback) {
          const assignedRoles = (context.authorization || {}).roles;

          let idTokenClaims = context.idToken || {};
          let accessTokenClaims = context.accessToken || {};

          idTokenClaims.realm_access = {'roles': assignedRoles};
          accessTokenClaims.realm_access = {'roles': assignedRoles};

          context.idToken = idTokenClaims;
          context.accessToken = accessTokenClaims;

          callback(null, user, context);
        }


3. Save changes to the rule.

Get a Token
===========

As mentioned before, Auth0 only supports associating roles with users which means that getting an access token with
embedded roles will require the
:auth0:`Resource Owner Password Flow <docs/get-started/authentication-and-authorization-flow/call-your-api-using-resource-owner-password-flow>`.

Use the following ``curl`` command to generate a token.

.. code-block:: bash

    curl --request POST \
      --url 'https://YOUR_DOMAIN/oauth/token' \
      --header 'content-type: application/x-www-form-urlencoded' \
      --data grant_type=password \
      --data client_id=YOUR_CLIENT_ID \
      --data client_secret=YOUR_CLIENT_SECRET \
      --data username=test@test.com \
      --data password=PASSWORD \
      --data audience=flask-ligand-mtm \
      --data 'scope=email openid profile'

Verify that the access token contains the roles for the given user by navigating to https://jwt.io/ and pasting in the
token.

Configure flask-ligand
======================

The ``OIDC_ISSUER_URL`` `environment variable`_ needs to be set to the
:auth0:`Domain <docs/get-started/applications/application-settings#basic-information>` HTTPS URL for the
"flask-ligand" Auth0 application. The ``OIDC_REALM`` `environment variable`_ should be set
to an **empty string** which will configure ``flask-ligand`` to assume Auth0 is being used **without** realm support.

If you would like to quickly test your Auth0 configuration with ``flask-ligand`` then it is recommended to follow the
`quickstart guide <quickstart.html>`_ to setup the example project. The example project can be quickly configured to
use your Auth0 setup by altering the ``.env`` `file <quickstart.html#explore-the-app>`_ with the appropriate Auth0
settings.

Here is an Auth0 ``.env`` file configuration that *could* work with the example project:

.. code-block:: bash

    OIDC_ISSUER_URL=https://dev-wbgr6rna.us.auth0.com
    OIDC_REALM=''
    SQLALCHEMY_DATABASE_URI=postgresql+pg8000://admin:password@localhost:5432/app
    OPENAPI_GEN_SERVER_URL=http://localhost:8888

.. _`environment variable`: configuration.html#prod
