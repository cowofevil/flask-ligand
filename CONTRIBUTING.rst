============
Contributing
============

Contributions are welcome, encouraged and are greatly appreciated! Every little bit helps, and credit will always be
given.

The `Github forking workflow`_ is used for submitting proposals for change to this repo. The following sections will
give a brief overview of how this repo utilizes the workflow for managing community contributions.

------------
Get Started!
------------

Ready to contribute? Here's how to set up ``flask-ligand`` for local development using the handy built-in
``make`` tasks.

Prerequisites
-------------

- Python 3.10+
- virtualenvwrapper_

Getting Help with Make Tasks
============================

Execute the following command to get a full list of ``make`` targets::

    $ make help

Setup Python Development Environment
====================================

1. Create a Python virtual environment::

    $ mkvirtualenv -p py310 flask-ligand

2. Setup develop environment::

    $ make develop-venv

3. Setup git pre-commit hooks::

    $ make setup-pre-commit

4. Verify that environment is ready for development::

    $ make test-tox

Setup Fork & Local Feature Branch
---------------------------------

First step is to `fork this repo`_!

Once a fork has been created, follow these steps to make a local clone and create a feature branch:

1. Clone your fork locally::

    $ git clone git@github.com:your_name_here/flask-ligand.git

2. Setup develop environment::

    $ cd flask-ligand/
    $ make develop-venv # OR 'make develop' if you're not using virtualenvwrapper

3. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

-----------------------
Pull Request Guidelines
-----------------------

Run All the Tests
-----------------

Before creating a commit it is essential that the changes be tested first. Also, make sure to write appropriate tests
for the change you'll be proposing in the pull request!

Simply execute the following ``make`` target to run tests against all supported Python versions::

    $ make test-tox

Commit Message Formatting
-------------------------

This repo utilizes `python-semantic-release`_ with the `emoji commit parser`_ configuration enabled. The type of change
being proposed in the commit must be in brackets in the commit subject which is expressed as an emoji which represents
one of the following `semantic versioning`_ change concepts:

Major:

- \:boom:

Minor:

- \:sparkles:
- \:children_crossing:
- \:lipstick:
- \:iphone:
- \:egg:
- \:chart_with_upwards_trend:

Patch:

- \:ambulance:
- \:lock:
- \:bug:
- \:zap:
- \:goal_net:
- \:alien:
- \:wheelchair:
- \:speech_balloon:
- \:mag:
- \:apple:
- \:penguin:
- \:checkered_flag:
- \:robot:
- \:green_apple:

The body of the commit message should give a succinct description of what is being changed and why.

**Example:**

::

    [:ambulance:] Fix Broken Thing

    The thing feature was broken in the last release because of a typo.

Create the Pull Request on GitHub
---------------------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests. (Not looking for 100% coverage, but a sufficient level of testing)
2. If the pull request adds functionality, the docs should be updated.
3. Check GitHub Actions to make sure that all tests pass for all supported Python versions before requesting a PR
   review.

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _Github forking workflow: https://docs.github.com/en/get-started/quickstart/github-flow
.. _fork this repo: https://docs.github.com/en/get-started/quickstart/fork-a-repo
.. _python-semantic-release: https://python-semantic-release.readthedocs.io/en/latest/#
.. _emoji commit parser: https://python-semantic-release.readthedocs.io/en/latest/configuration.html#commit-parser
.. _semantic versioning: https://semver.org/
