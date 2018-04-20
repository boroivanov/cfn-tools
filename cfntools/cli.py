# -*- coding: utf-8 -*-

import click

from cfntools.ls import ls
from cfntools.diff import diff
from cfntools.validate import validate

version = '0.1.6'


@click.group()
@click.version_option(version=version, message=version)
def main(args=None):
    """Tools for AWS CloudFormation

       \b
       cfn-tools --help
       cfn-tools <command> --help
    """


main.add_command(ls)
main.add_command(diff)
main.add_command(validate)


if __name__ == "__main__":
    main()
