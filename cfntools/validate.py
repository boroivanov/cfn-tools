import sys
import boto3
import botocore
import click

client = boto3.client('cloudformation')


def validate_template(client, filename):
    try:
        with open(filename, 'r') as f:
            template = f.read()
            client.validate_template(TemplateBody=template)
    except botocore.exceptions.ClientError as e:
        click.echo(e.response["Error"]["Message"])
        sys.exit(1)


@click.command(short_help='Validate template')
@click.option('-p', '--profile', default=None, help='AWS profile')
@click.option('-r', '--region', default=None, help='AWS region')
@click.argument('filename')
def validate(filename, profile, region):
    """Validate template

    \b
    cfn-tools validate TEMPLATE
    """
    session = boto3.session.Session(profile_name=profile, region_name=region)
    client = session.client('cloudformation')

    validate_template(client, filename)


if __name__ == '__main__':
    validate()
