#!/usr/share/bin python

import bs4
import pandas as pd

from eui_selektor_client.auth import HTTPAuthClient
from eui_selektor_client.form import FormFields


class _EUISelektorClient:
    base_url = 'https://wwwbis.sidc.be/EUI/data_internal/selektor/index.php'
    service_id = 'EUI_SELEKTOR_CLIENT'

    def __init__(self):
        self.http_client = HTTPAuthClient('EUI_SELEKTOR_CLIENT')


class EUISelektorFormViewer(_EUISelektorClient):
    """ Parse the EUI selektor form to retrieve allowed search parameters

    Example
    =======
    >>> form_viewer = EUISelektorFormViewer()
    >>> form = form_viewer.get_form()
    >>> form_viewer.show_form(form)
    EUI SELEKTOR search parameters
    ------------------------------
    ..: ...
    detector[]: string (choices: 'FSI', 'HRI_EUV', 'HRI_LYA')  # DETECTOR
    wavelnth[]: string (choices: '174', '304', '1216')  # WAVELNTH
    ..: ...
    date_begin_start: date ('YYYY-MM-DD')  # DATE-BEG
    date_begin_start_hour: number (0-23)  # DATE-BEG
    date_begin_start_minute: number (0-59)  # DATE-BEG
    date_begin_end: date ('YYYY-MM-DD')  # DATE-BEG
    date_begin_end_hour: number (0-23)  # DATE-BEG
    date_begin_end_minute: number (0-59)  # DATE-BEG


    """

    @staticmethod
    def _parse_detreg_form_table(tab):
        """ Parse the form table containing detreg values """
        rows = list(tab.children)
        rows = rows[1::2]  # drop header rows, names are already in input tags
        search_params = []
        for row in rows:
            for input_widget in row.find_all('input'):
                sp = FormFields.Number(
                    input_widget['name'],
                    input_widget['min'],
                    input_widget['max'],
                    )
                search_params.append(sp)
        return search_params

    @staticmethod
    def _parse_main_form_table(tab):
        """ Parse the main form table """
        rows = list(tab.children)
        search_params = []
        for row in rows:
            comment = [td.text for td in row.find_all('td')
                       if td.find('input') is None]
            comment = ' '.join(comment)
            inputs = row.find_all('input')
            if inputs[0]['name'].endswith('[]'):
                """ Row consists of a single multiple choice field """
                name = inputs[0]['name']
                options = [inp['value'] for inp in row.find_all('input')]
                input_type = inputs[0]['type']
                if input_type == 'checkbox':
                    sp = FormFields.MultipleChoice(
                        name, options, comment=comment
                        )
                elif input_type == 'radio':
                    sp = FormFields.SingleChoice(
                        name, options, comment=comment
                        )
                else:
                    msg = 'could not parse form: unknown input type'
                    raise ValueError(msg)
                search_params.append(sp)
            else:
                """ Row consists of several (single-choice) fields """
                for input_widget in inputs:
                    if input_widget['type'] == 'number':
                        sp = FormFields.Number(
                            input_widget['name'],
                            input_widget['min'],
                            input_widget['max'],
                            comment=comment,
                            )
                    elif input_widget['type'] == 'date':
                        sp = FormFields.Date(
                            input_widget['name'],
                            input_widget['value'],
                            comment=comment,
                            )
                    else:
                        msg = 'could not parse form: unknown input type'
                        raise ValueError(msg)
                    search_params.append(sp)
        return search_params

    def get_form(self):
        """ Query the form from the selektor web page

        Returns
        =======
        search_params : list of form fields
            Search parameters, with description and allowed values
        """
        r = self.http_client.query(self.base_url)

        b = bs4.BeautifulSoup(r.content, features='html.parser')
        tables = b.find_all('table')
        search_params = self._parse_detreg_form_table(tables[0])
        search_params += self._parse_main_form_table(tables[1])

        return search_params

    @staticmethod
    def show_form(form):
        """ Display the search form """
        print('EUI SELEKTOR search parameters')
        print('------------------------------')
        for param in form:
            print(param)


class EUISelektorClient(_EUISelektorClient):
    """ EUI selektor client (https://wwwbis.sidc.be/EUI/data_internal/selektor)

    Example
    =======
    >>> client = EUISelektorClient()
    >>> res = client.search({
    ...   'detector[]': 'FSI',
    ...   'wavelnth[]': '304',
    ...   'imgtype[]:': 'solar image',
    ...   'date_begin_start': '2021-12-01',
    ...   'date_begin_end': '2021-12-31',
    ...   'limit[]': 500,
    ...   })
    >>> print(res)
           #                 date-beg detector  ...      crval2  crpix1  crpix2
    0      0  2021-12-30T23:45:15.335      FSI  ...  102.484419  1536.5  1536.5
    1      1  2021-12-30T23:30:15.547      FSI  ...  102.692080  1536.5  1536.5
    2      2  2021-12-30T23:15:15.269      FSI  ...  102.401791  1536.5  1536.5
    3      3  2021-12-30T23:00:15.501      FSI  ...  102.394845  1536.5  1536.5
    4      4  2021-12-30T22:45:15.239      FSI  ...  102.337948  1536.5  1536.5
    ..   ...                      ...      ...  ...         ...     ...     ...
    495  495  2021-12-26T15:38:15.297      FSI  ...  102.821920  1536.5  1536.5
    496  496  2021-12-26T15:36:15.297      FSI  ...  102.388034  1536.5  1536.5
    497  497  2021-12-26T15:34:15.297      FSI  ...  102.156946  1536.5  1536.5
    498  498  2021-12-26T15:32:15.297      FSI  ...  102.694615  1536.5  1536.5
    499  499  2021-12-26T15:30:15.296      FSI  ...  102.723120  1536.5  1536.5
    <BLANKLINE>
    [500 rows x 118 columns]

    """
    default_search_params = {
        'level[]': 'L1',
        'orderby[]': 'date-beg',
        'order[]': 'DESC',
        'limit[]': 100,
        }

    def _fill_default_search_params(self, search_params):
        default_params = self.default_search_params.copy()
        # use default params for keys that do not exist
        default_params.update(search_params)
        params = default_params
        # delete keys set to None
        params = {k: v for k, v in params.items() if v is not None}
        return params

    def search(self, search_params):
        """ Send search query and parse results

        Parameters
        ==========
        search_params : dict
            Dict of search parameters (call `.show_search_params()` to display
            available search keywords).

        Returns
        =======
        results : pd.DataFrame
            Search results.
        """
        search_params = self._fill_default_search_params(search_params)
        r = self.http_client.query(self.base_url, params=search_params)
        dfs = pd.read_html(r.content, flavor='bs4')
        try:
            return dfs[2]
        except IndexError:
            return None
