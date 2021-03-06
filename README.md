# EUI Selektor client

Lightweight client for [EUI Selektor].


## Installation

Clone the repository (or download the sources), and install with pip:

```bash
git clone https://github.com/gpelouze/eui_selektor_client
pip install --user eui_selektor_client
```


## Example

```python
from eui_selektor_client import EUISelektorClient, EUISelektorFormViewer

if __name__ == '__main__':

    # Download the form and print available search keywords
    form_viewer = EUISelektorFormViewer()
    form = form_viewer.get_form()
    form_viewer.show_form(form)

    # Query images captured in December 2021 with FSI 304
    client = EUISelektorClient()
    res = client.search({
        'detector[]': 'FSI',
        'wavelnth[]': '304',
        'imgtype[]:': 'solar image',
        'date_begin_start': '2021-12-01',
        'date_begin_end': '2021-12-31',
        'limit[]': 500,
        })
    print(res)
    # #                 date-beg detector  ...      crval2  crpix1  crpix2
    # 0      0  2021-12-30T23:45:15.335      FSI  ...  102.484419  1536.5  1536.5
    # 1      1  2021-12-30T23:30:15.547      FSI  ...  102.692080  1536.5  1536.5
    # 2      2  2021-12-30T23:15:15.269      FSI  ...  102.401791  1536.5  1536.5
    # 3      3  2021-12-30T23:00:15.501      FSI  ...  102.394845  1536.5  1536.5
    # 4      4  2021-12-30T22:45:15.239      FSI  ...  102.337948  1536.5  1536.5
    # ..   ...                      ...      ...  ...         ...     ...     ...
    # 495  495  2021-12-26T15:38:15.297      FSI  ...  102.821920  1536.5  1536.5
    # 496  496  2021-12-26T15:36:15.297      FSI  ...  102.388034  1536.5  1536.5
    # 497  497  2021-12-26T15:34:15.297      FSI  ...  102.156946  1536.5  1536.5
    # 498  498  2021-12-26T15:32:15.297      FSI  ...  102.694615  1536.5  1536.5
    # 499  499  2021-12-26T15:30:15.296      FSI  ...  102.723120  1536.5  1536.5
```


## Authentication

The EUI selektor page is password protected.
The first time you run the client, you will be prompted for a username and password.
These are then securely stored by your OS using the [keyring] library, and retrieved the next time you use the client.

To manually update the credentials, run:

```python
from eui_selektor_client import EUISelektorClient
client = EUISelektorClient()
client.update_credentials()
```


## License

This package is released under a MIT open source licence. See `LICENSE.txt`.


[EUI Selektor]: https://wwwbis.sidc.be/EUI/data_internal/selektor
[keyring]: https://pypi.org/project/keyring/