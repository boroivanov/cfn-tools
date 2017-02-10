cfn-tools
=========

.. image:: https://img.shields.io/pypi/v/cfn-tools.svg
    :target: https://pypi.python.org/pypi/cfn-tools
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/boroivanov/cfn-tools.png
   :target: https://travis-ci.org/boroivanov/cfn-tools
   :alt: Latest Travis CI build status


* GitHub: https://github.com/boroivanov/cfn-tools
* PyPI: https://pypi.python.org/pypi/cfn-tools

Tools for AWS CloudFormation

* list stacks
* diff a stack and a template
* diff two stacks
* validate a template


Installation
------------

.. code:: bash

    pip install cfn-tools


Usage
-----

List stacks:

.. code:: bash

  cfn-tools ls
  cfn-tools ls NAME

  # Filter stacks by status.
  # Returns stacks which status contains the filter string.
  # Deleted stacks are not returned by default. Use `-f delete` to get those.

  cfn-tools ls -f create
  cfn-tools ls -f rollback NAME
  cfn-tools ls -f progress NAME

  # Filter out stacks by status.
  # Deleted stacks are not returned by default.

  cfn-tools ls -f \!create NAME


Diff Stacks/Templates:

.. code:: bash

  cfn-tools diff TEMPLATE STACK
  cfn-tools diff STACK1 STACK2
  cfn-tools diff -r us-west-2 STACK1 -r2 us-east-1 STACK2


Validate a template:

.. code:: bash

  cfn-tools validate TEMPLATE
  
Credits
=======
  
Huge thanks to `@stefansundin`_ and  `@dstokes`_
