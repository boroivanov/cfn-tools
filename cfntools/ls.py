import sys
import boto3
import click

from botocore.exceptions import ClientError


status_map = {
    'CREATE_IN_PROGRESS': 'CP',
    'CREATE_FAILED': 'CF',
    'CREATE_COMPLETE': 'C',
    'ROLLBACK_IN_PROGRESS': 'RP',
    'ROLLBACK_FAILED': 'RF',
    'ROLLBACK_COMPLETE': 'R',
    'DELETE_IN_PROGRESS': 'DP',
    'DELETE_FAILED': 'DF',
    'DELETE_COMPLETE': 'D',
    'UPDATE_IN_PROGRESS': 'UP',
    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS': 'UCP',
    'UPDATE_COMPLETE': 'U',
    'UPDATE_ROLLBACK_IN_PROGRESS': 'URP',
    'UPDATE_ROLLBACK_FAILED': 'URF',
    'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS': 'URCP',
    'UPDATE_ROLLBACK_COMPLETE': 'UR',
    'REVIEW_IN_PROGRESS': 'RevP'
}


def get_stacks(client, filters):
    """Returns a list of StackSummaries"""
    try:
        response = client.list_stacks(StackStatusFilter=filters)
        stacks = response['StackSummaries']
        while True:
            if 'NextToken' not in response:
                break
            response = client.list_stacks(
                NextToken=response['NextToken'], StackStatusFilter=filters)
            stacks += response['StackSummaries']
        return stacks
    except ClientError as e:
        click.echo(e.response["Error"]["Message"])
        sys.exit(1)


def get_filters(filter):
    """Returns a list of filtered stack status codes"""
    if filter is None or 'COMPLETE' in filter.upper():
        return [k for k in status_map.keys() if 'DELETE_' not in k]
    elif filter.startswith('!') is True:
        return [k for k in status_map.keys() if filter[1:].upper() not in k and 'DELETE_' not in k]
    else:
        return [k for k in status_map.keys() if filter.upper() in k]


def list_codes(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    for k, v in sorted(status_map.iteritems()):
        print('{0:>4} {1}'.format(v, k))
    ctx.exit()


def format_listing(stack, time_label):
    s = stack
    print('{0:<20} {1:<4} {2}'.format(
        s[time_label].strftime("%Y-%m-%d %H:%M:%S"), status_map[s['StackStatus']], s['StackName']))


@click.command(short_help='List stacks')
@click.option('-f', '--filter', help='filter stacks by status code')
@click.option('-c', '--codes', is_flag=True, callback=list_codes, expose_value=False,
              is_eager=True, help='List status codes')
@click.option('-p', '--profile', default=None, help='AWS profile')
@click.option('-r', '--region', default=None, help='AWS region')
@click.argument('name', default='')
def ls(name, filter, profile, region):
    """List stacks

    Deleted stacks are filtered out by default

    \b
    cfn-tools ls
    cfn-tools ls FUZZY_SEARCH

    \b
    cfn-tools --codes
    cfn-tools ls FUZZY_SEARCH -f update
    cfn-tools ls FUZZY_SEARCH -f \!update
    """

    session = boto3.session.Session(profile_name=profile, region_name=region)
    client = session.client('cloudformation')

    filters = get_filters(filter)
    stacks = get_stacks(client, filters)
    if name is not None:
        stacks = [k for k in stacks if name in k['StackName']]

    for s in stacks:
        if s['StackStatus'].startswith('CREATE_') is True:
            format_listing(s, 'CreationTime')
        elif s['StackStatus'].startswith('UPDATE_') is True:
            format_listing(s, 'LastUpdatedTime')
        elif s['StackStatus'].startswith('DELETE_') is True:
            format_listing(s, 'DeletionTime')
        else:
            click.echo(status_map[s['StackStatus']], s['StackName'])
