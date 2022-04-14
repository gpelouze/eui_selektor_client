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