import sys
import boto3
import botocore
import click
import json
import difflib

from cfntools.validate import validate_template


def get_template(client, stack):
    """Get the template for a stack"""
    try:
        response = client.get_template(
            StackName=stack
        )
        template = response["TemplateBody"]
        if isinstance(template, dict):
            template = json.dumps(template, indent=2, sort_keys=True)
        return template
    except botocore.exceptions.ClientError as e:
        click.echo(e.response["Error"]["Message"])
        sys.exit(1)


def read_file(file):
    try:
        with open(file, 'r') as f:
            return f.read()
    except IOError as e:
        click.echo(e)
        sys.exit(1)


def read_template(client, template):
    """Read the template from a file or the stack object"""
    if template.endswith(tuple(['.yaml', '.yml', '.json'])):
        validate_template(client, template)
        tmpl = read_file(template)
        if template.endswith('.json'):
            tmpl = json.dumps(json.loads(tmpl), indent=2, sort_keys=True)
    else:  # CloudFormation Stack
        tmpl = get_template(client, template)
    return tmpl


def create_cloudformation_session(profile=None, region=None):
    session = boto3.session.Session(profile_name=profile, region_name=region)
    return session.client('cloudformation')


@click.command(short_help='Diff stacks and/or templates')
@click.option('-p', '--profile', help='AWS profile')
@click.option('-r', '--region', help='AWS region')
@click.option('-p2', '--profile2', help='AWS profile (optional for second template)')
@click.option('-r2', '--region2', help='AWS region (optional for second template)')
@click.argument('TEMPLATE1')
@click.argument('TEMPLATE2')
def diff(template1, template2, profile, region, profile2, region2):
    """Diff stacks and/or templates

    \b
    cfn-tools diff TEMPLATE STACK
    cfn-tools diff STACK1 STACK2
    cfn-tools diff -r us-west-2 STACK1 -r2 us-east-1 STACK2
    """
    region2 = region2 or region
    profile2 = profile2 or profile

    client1 = create_cloudformation_session(profile, region)
    client2 = create_cloudformation_session(profile2, region2)

    tmpl1 = read_template(client1, template1)
    tmpl2 = read_template(client2, template2)

    diff = difflib.unified_diff(
        tmpl1.splitlines(),
        tmpl2.splitlines(),
        fromfile='a/' + template1,
        tofile='b/' + template2
    )
    for line in diff:
        if line.startswith("+"):
            click.secho(line, fg='green')
        elif line.startswith("-"):
            click.secho(line, fg='red')
        else:
            click.echo(line)


if __name__ == '__main__':
    diff()
