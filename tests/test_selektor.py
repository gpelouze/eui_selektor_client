import unittest

from eui_selektor_client import EUISelektorClient, EUISelektorFormViewer
from eui_selektor_client.form import FormFields


class TestEUISelektorFormViewer(unittest.TestCase):
    form_ref = [
        FormFields.Number('detreg20', 0, 255),
        FormFields.Number('detreg21', 0, 255),
        FormFields.Number('detreg22', 0, 255),
        FormFields.Number('detreg23', 0, 255),
        FormFields.Number('detreg24', 0, 255),
        FormFields.Number('detreg25', 0, 255),
        FormFields.Number('detreg26', 0, 255),
        FormFields.Number('detreg27', 0, 255),
        FormFields.Number('detreg28', 0, 255),
        FormFields.Number('detreg29', 0, 255),
        FormFields.Number('detreg2a', 0, 255),
        FormFields.Number('detreg2b', 0, 255),
        FormFields.Number('detreg2c', 0, 255),
        FormFields.Number('detreg2d', 0, 255),
        FormFields.Number('detreg2e', 0, 255),
        FormFields.Number('detreg2f', 0, 255),
        FormFields.Number('detreg30', 0, 255),
        FormFields.Number('detreg31', 0, 255),
        FormFields.Number('detreg32', 0, 255),
        FormFields.Number('detreg33', 0, 255),
        FormFields.Number('detreg34', 0, 255),
        FormFields.Number('detreg35', 0, 255),
        FormFields.Number('detreg36', 0, 255),
        FormFields.Number('detreg37', 0, 255),
        FormFields.Number('detreg38', 0, 255),
        FormFields.Number('detreg39', 0, 255),
        FormFields.Number('detreg3a', 0, 255),
        FormFields.Number('detreg3b', 0, 255),
        FormFields.Number('detreg3c', 0, 255),
        FormFields.Number('detreg3d', 0, 255),
        FormFields.Number('detreg3e', 0, 255),
        FormFields.Number('detreg3f', 0, 255),
        FormFields.SingleChoice('level[]', ['L0', 'L1'], comment='LEVEL'),
        FormFields.Number(
            'image_size_min', 320, 3072, comment='NAXIS1=NAXIS2'
            ),
        FormFields.Number(
            'image_size_max', 320, 3072, comment='NAXIS1=NAXIS2'
            ),
        FormFields.MultipleChoice(
            'binning[]', ['1', '2', '4'], comment='BINNING'
            ),
        FormFields.MultipleChoice(
            'detector[]', ['FSI', 'HRI_EUV', 'HRI_LYA'], comment='DETECTOR'
            ),
        FormFields.MultipleChoice(
            'wavelnth[]', ['174', '304', '1216'], comment='WAVELNTH'
            ),
        FormFields.MultipleChoice(
            'recstate[]', ['on', 'off'], comment='RECSTATE'
            ),
        FormFields.MultipleChoice(
            'crrem[]', ['on', 'off'], comment='CRREM'
            ),
        FormFields.MultipleChoice(
            'compress[]', ['Lossless', 'Lossy-high quality', 'Lossy-strong',
                           'Lossy-extreme', 'None'], comment='COMPRESS \xa0'
            ),
        FormFields.MultipleChoice(
            'gaincomb[]', ['low-only', 'high-only', 'combined', 'both',
                           'other'], comment='GAINCOMB'
            ),
        FormFields.Number('combitpp_min', 0, 255, comment='COMBITPP'),
        FormFields.Number('combitpp_max', 0, 255, comment='COMBITPP'),
        FormFields.Number('readoutm_min', 0, 5, comment='READOUTM'),
        FormFields.Number('readoutm_max', 0, 5, comment='READOUTM'),
        FormFields.MultipleChoice(
            'ledstate[]', ['all off', 'main on', 'red on'], comment='LEDSTATE'
            ),
        FormFields.MultipleChoice(
            'imgtype[]', ['solar image', 'LED image', 'dark image',
                          'occulted image'], comment='IMGTYPE'
            ),
        FormFields.Number('xposure_min', 0, 7200, comment='XPOSURE'),
        FormFields.Number('xposure_max', 0, 7200, comment='XPOSURE'),
        FormFields.Number('crota_min', -360, 360, comment='CROTA'),
        FormFields.Number('crota_max', -360, 360, comment='CROTA'),
        FormFields.Number(
            'doorpos_min', 0, 255,
            comment=('DOORPOS 0=closed. FSI: occulter=15-25, 34=open. '
                     'HRI_LYA: 26=open. HRI_EUV: 34=open.')
            ),
        FormFields.Number(
            'doorpos_max', 0, 255,
            comment=('DOORPOS 0=closed. FSI: occulter=15-25, 34=open. '
                     'HRI_LYA: 26=open. HRI_EUV: 34=open.')
            ),
        FormFields.Number(
            'priority_min', 0, 255,
            comment=('PRIORITY 0=Low Latency. 255 = Dummy. Science data is '
                     'anything in between')
            ),
        FormFields.Number(
            'priority_max', 0, 255,
            comment=('PRIORITY 0=Low Latency. 255 = Dummy. Science data is '
                     'anything in between')
            ),
        FormFields.Number(
            'dsun_au_min', 0, 1.2,
            comment='DSUN_AU Distance to the Sun in AU'),
        FormFields.Number(
            'dsun_au_max', 0, 1.2,
            comment='DSUN_AU Distance to the Sun in AU'),
        FormFields.MultipleChoice(
            'doorext[]', ['open', 'closed'], comment='DOOREXT (L1+)'
            ),
        FormFields.SingleChoice(
            'orderby[]', ['obt_beg', 'date-beg', 'insertion_time'],
            comment='ORDERBY'
            ),
        FormFields.SingleChoice('order[]', ['ASC', 'DESC'], comment='ORDER'),
        FormFields.SingleChoice(
            'limit[]', ['100', '500', '5000'], comment='LIMIT'
            ),
        FormFields.Date('date_begin_start', '', comment='DATE-BEG'),
        FormFields.Number('date_begin_start_hour', 0, 23, comment='DATE-BEG'),
        FormFields.Number(
            'date_begin_start_minute', 0, 59, comment='DATE-BEG'
            ),
        FormFields.Date('date_begin_end', '', comment='DATE-BEG'),
        FormFields.Number('date_begin_end_hour', 0, 23, comment='DATE-BEG'),
        FormFields.Number('date_begin_end_minute', 0, 59, comment='DATE-BEG'),
        ]

    def setUp(self):
        self.form_viewer = EUISelektorFormViewer()

    def test_get_form(self):
        form = self.form_viewer.get_form()
        for f1, f2 in zip(form, self.form_ref):
            if repr(f1) != repr(f2):
                print('Mismatched fields')
                print('(web)', f1)
                print('(ref)', f2)
                self.fail()


class TestEUISelektorClient(unittest.TestCase):
    
    res_ref_repr = '''\
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

[500 rows x 118 columns]'''

    def setUp(self):
        self.client = EUISelektorClient()

    def test_search(self):
        res = self.client.search(
            {
                'detector[]': 'FSI',
                'wavelnth[]': '304',
                'imgtype[]': 'solar image',
                'date_begin_start': '2021-12-01',
                'date_begin_end': '2021-12-31',
                'limit[]': 500,
                }
            )
        assert repr(res) == self.res_ref_repr


if __name__ == '__main__':
    unittest.main()