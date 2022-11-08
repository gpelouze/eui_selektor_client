import argparse
import pandas

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

    if args.query:
        client = EUISelektorClient()
        query = parse_query_args(args.query)

        if args.nolimit:  # --no-limit requires ascending sorting by date, requested sorting will be done at the end
            req_order_by = query['orderby[]'] if 'orderby[]' in query else client.default_search_params['orderby[]']
            req_order = query['order[]'] if 'order[]' in query else client.default_search_params['order[]']
            query['orderby[]'] = 'date-beg'
            query['order[]'] = 'ASC'
            query['limit[]'] = '500'

        final = None
        while True:
            res = client.search(query)
            if res is None:
                break
            else:
                final = pandas.concat([res, final])
                if len(res) < int(query['limit[]']):
                    break
            if args.nolimit is False:
                break
            # update date, hour, minute fields for next iteration
            last_date = res['date-beg'][res.index[-1]]  # is last index because orderby and order were forced
            query['date_begin_start'] = last_date[0:10]
            query['date_begin_start_hour'] = last_date[11:13]
            query['date_begin_start_minute'] = last_date[14:16]

        if final is not None:
            if args.nolimit:  # re-sort values according to query/default if --nolimit is set
                final.sort_values(by=req_order_by, ascending=req_order == 'ASC')
            res_str = final.to_csv(args.output)
            if res_str is not None:
                print(res_str)
