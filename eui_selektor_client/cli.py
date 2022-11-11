import argparse
import sys

from eui_selektor_client import EUISelektorClient, EUISelektorFormViewer


def parse_query_args(query_strings):

    query_dict = {}
    for param_string in query_strings:
        param_split = param_string.split(':')
        if len(param_split) != 2:
            raise ValueError(
                f'could not parse query parameter: {param_string}')
        k, v = param_split
        query_dict[k] = v
    return query_dict


def cli():
    p = argparse.ArgumentParser(
        description='Lightweight client for EUI selektor')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        '--view-form', action='store_true',
        help='retrieve and display the search form parameters')
    g.add_argument(
        '--update-credentials', action='store_true',
        help='update the username and password stored in the keyring')
    g.add_argument(
        '--query', metavar='param', nargs='+',
        help='run a query (parameter format: "name:value")')
    p.add_argument(
        '--output', metavar='csv_file',
        help='save the query results to a file')
    p.add_argument(
        '--nolimit', action='store_true',
        help='make multiple queries in case maximum number of results is reached')
    args = p.parse_args()

    if args.view_form:
        form_viewer = EUISelektorFormViewer()
        form = form_viewer.get_form()
        form_viewer.show_form(form)

    if args.update_credentials:
        client = EUISelektorClient()
        client.update_credentials()

    if args.query:
        client = EUISelektorClient()
        query = parse_query_args(args.query)

        res = client.search_nolimit(query) if args.nolimit else client.search(query)

        if res is None:
            print('No results found')
            sys.exit(1)
        else:
            res_str = res.to_csv(args.output)
            if res_str is not None:
                print(res_str)
