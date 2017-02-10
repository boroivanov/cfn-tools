# -*- coding: utf-8 -*-

import click
from cfntools import __version__
from ls import ls
from diff import diff
from validate import validate


@click.group()
@click.version_option(version=__version__)
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
