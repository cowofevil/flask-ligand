Release Process
===============

Automated Process
-----------------

This repo utilizes `python-semantic-release`_ in conjunction with `GitHub Actions`_ to create releases automatically.

Manually Process
----------------

**ONLY UNDER LIMITED CIRCUMSTANCES SHOULD THIS PROCESS BE USED!**

Configuring Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following environment variables are necessary for creating a full production release:

.. list-table:: **Environment Variables**
   :widths: 30 50

   * - **ENV**
     - **Description**
   * - ``GH_TOKEN``
     - A personal access token from GitHub. This is used for authenticating when pushing tags, publishing releases etc.
       See `Configuring push to Github`_ for usage.

       To generate a token go to https://github.com/settings/tokens and click on *Personal access token*.
   * - ``REPOSITORY_USERNAME``
     - Used together with REPOSITORY_PASSWORD when publishing artifact.

       Note: If you use token authentication with *pypi* set this to *__token__*.
   * - ``REPOSITORY_PASSWORD``
     - Used together with REPOSITORY_USERNAME when publishing artifact. Also used for token when using token
       authentication.

Publish the Release
~~~~~~~~~~~~~~~~~~~

Simply execute the following ``make`` target::

    $ make publish

.. _python-semantic-release: https://python-semantic-release.readthedocs.io/en/latest/#
.. _GitHub Actions: https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions
.. _Configuring push to Github: https://python-semantic-release.readthedocs.io/en/latest/automatic-releases/index.html#automatic-github
