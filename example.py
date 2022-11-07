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
        'imgtype[]': 'solar image',
        'date_begin_start': '2021-12-01',
        'date_begin_end': '2021-12-31',
        'limit[]': 500,
        })
    print(res)