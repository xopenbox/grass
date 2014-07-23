import grass.gunittest
from grass.gunittest.gmodules import SimpleModule

cell_seed_500 = """\
north: 20
south: 10
east: 25
west: 15
rows: 10
cols: 10
2 12 183 135 117 176 138 117 182 40
157 70 195 1 30 125 122 74 108 104
163 146 82 164 67 63 60 3 147 193
151 173 144 173 128 77 141 6 144 193
180 56 14 121 124 107 46 107 90 60
177 57 12 104 178 13 167 104 163 187
55 133 27 114 195 60 78 35 49 11
55 138 25 105 32 58 47 18 139 32
24 74 36 71 131 124 87 161 160 154
136 45 48 146 9 182 69 12 35 19
"""

dcell_seed_600 = """\
north: 20
south: 10
east: 25
west: 15
rows: 10
cols: 10
130.790433856418332 101.3319248101491041 33.5781271447787759 37.4064724824657944 98.2794723130458152 73.9118866262841863 185.9530433718733775 74.5210037729812882 166.1178416001017695 90.9915650902159996
109.2478664232956334 25.6499350759712215 150.9024447059825036 125.7544119036241312 66.7235333366722614 167.9375729129454271 123.1009291055983965 12.0922254083554606 59.389026967287819 113.2843489528100349
40.0044184023145277 135.8273774212801186 71.6737798852435049 191.6223505280372876 4.1546013811569615 143.3082794522489962 177.043829294835632 115.0300571162354402 141.8985452774071234 127.8949967123638061
93.2842559637482793 9.7471880052423856 118.1216452002055632 158.1474162140586088 67.2957262519499437 3.6524546350146849 147.0965842667525862 37.060628529871579 47.3408278816968959 66.2219633495724054
175.5638637866295539 67.1399023507611901 162.2058392782793703 198.1586789345953719 36.474049475167746 49.2589028048889617 112.1169663235969836 22.0227597984432535 95.9169228571662131 86.7470895014531322
93.5401613888204935 193.7821104138942587 193.8286564351004699 3.2623643889134684 94.6955247357847725 25.7099391122614307 155.592251526775442 25.3392337002970294 48.3979699868663005 99.6836079482556272
104.16296861365457 190.7865884377180805 6.2841805474238619 49.3731395705159528 100.1903962703459285 116.927654961282343 19.8626348109264264 40.9693022766258466 81.6500759554420057 169.2220572316770131
118.8112518721558217 55.8955021401724039 112.9150308215961331 62.6399760484719081 85.400498505854145 191.0144187084912062 124.2128169358724534 167.9341741649760706 170.6149695243870781 158.3034517206661462
130.0453795775294736 64.1996403829061535 62.9317494959142465 175.1909990236256931 122.9624852869890361 79.9546265736285733 9.6594013716963367 114.0611338072915544 11.9371167643030809 186.9121199748369122
3.2891990250261536 30.9245408751958379 46.4021422454598991 104.2378950097200203 47.424093232347019 73.4801303522840499 22.4778583078695213 132.870185207462697 48.1666164169167388 100.5504714442693057
"""

fcell_seed_700 = """\
north: 20
south: 10
east: 25
west: 15
rows: 10
cols: 10
146.756378 192.682159 2.644822 147.270462 62.178818 192.668198 94.320778 107.710426 98.319664 114.444504
12.995321 18.026272 151.590958 5.249451 197.266708 103.663635 115.424088 28.01062 78.555168 62.912098
164.053619 154.652039 98.536011 44.601639 85.322289 168.383957 44.93845 128.62262 89.910591 107.242188
111.182487 63.080284 177.791473 47.439354 42.451859 72.396568 170.597778 170.622742 141.88858 105.126854
120.76828 148.581085 42.124866 56.432236 164.652176 98.094009 60.741329 66.286987 187.847427 160.120056
50.530689 179.090652 138.114014 138.629211 193.147903 172.861481 133.72728 108.720459 103.508438 28.81559
39.653179 101.948265 35.744762 25.570076 78.767021 154.600616 144.907684 82.370148 116.378654 18.218494
35.587288 66.534409 65.744408 186.476959 137.081116 151.379272 48.261463 8.323328 130.432739 53.346546
152.67189 15.512391 146.049072 185.276245 34.417141 127.522453 124.54998 52.08218 167.141342 87.771118
69.0522 43.57811 63.15279 68.677063 74.202805 97.429077 167.123199 19.892767 120.593437 190.960815
"""


class TestRandFunction(grass.gunittest.TestCase):

    # TODO: replace by unified handing of maps
    to_remove = []

    @classmethod
    def setUpClass(cls):
        cls.use_temp_region()
        cls.runModule('g.region', n=20, s=10, e=25, w=15, res=1)

    @classmethod
    def tearDownClass(cls):
        cls.del_temp_region()
        cls.runModule('g.remove', rast=','.join(cls.to_remove))

    def rinfo_contains_number(self, raster, number):
        """Test that r.info stdandard output for raster contains a given number
        """
        rinfo = SimpleModule('r.info', map=raster)
        self.runModule(rinfo)
        self.assertIn(str(number), rinfo.outputs.stdout)

    def test_seed_not_required(self):
        """Test that seed is not required when rand() is not used"""
        self.assertModule('r.mapcalc', expression='nonrand_cell = 200')
        self.to_remove.append('nonrand_cell')

    def test_seed_required(self):
        """Test that seed is required when rand() is used"""
        self.assertModuleFail('r.mapcalc', expression='rand_x = rand(1, 200)')
        # TODO: assert map not exists but it would be handy here

    def test_seed_cell(self):
        """Test given seed with CELL against reference map"""
        seed = 500
        self.runModule('r.in.ascii', input='-', stdin=cell_seed_500,
                       output='rand_cell_ref')
        self.to_remove.append('rand_cell_ref')
        self.assertModule('r.mapcalc', seed=seed,
                          expression='rand_cell = rand(1, 200)')
        self.to_remove.append('rand_cell')
        # this assert is using r.mapcalc but we are testing different
        # functionality than used by assert
        self.assertRastersNoDifference(actual='rand_cell',
                                       reference='rand_cell_ref',
                                       precision=0)
        self.rinfo_contains_number('rand_cell', seed)

    def test_seed_dcell(self):
        """Test given seed with DCELL against reference map"""
        seed = 600
        self.runModule('r.in.ascii', input='-', stdin=dcell_seed_600,
                       output='rand_dcell_ref')
        self.to_remove.append('rand_dcell_ref')
        self.assertModule('r.mapcalc', seed=seed,
                          expression='rand_dcell = rand(1.0, 200.0)')
        self.to_remove.append('rand_dcell')
        # this assert is using r.mapcalc but we are testing different
        # functionality than used by assert
        self.assertRastersNoDifference(actual='rand_dcell',
                                       reference='rand_dcell_ref',
                                       precision=0.00000000000001)
        self.rinfo_contains_number('rand_dcell', seed)

    def test_seed_fcell(self):
        """Test given seed with FCELL against reference map"""
        seed = 700
        self.runModule('r.in.ascii', input='-', stdin=fcell_seed_700,
                       output='rand_fcell_ref')
        self.to_remove.append('rand_fcell_ref')
        self.assertModule('r.mapcalc', seed=seed,
                          expression='rand_fcell = rand(float(1), 200)')
        self.to_remove.append('rand_fcell')
        # this assert is using r.mapcalc but we are testing different
        # functionality than used by assert
        self.assertRastersNoDifference(actual='rand_fcell',
                                       reference='rand_fcell_ref',
                                       precision=0.000001)
        self.rinfo_contains_number('rand_fcell', seed)

    def test_auto_seed(self):
        """Test that two runs with -s does not give same maps"""
        self.assertModule('r.mapcalc', flags='s',
                          expression='rand_auto_1 = rand(1., 2)')
        self.to_remove.append('rand_auto_1')
        self.assertModule('r.mapcalc', flags='s',
                          expression='rand_auto_2 = rand(1., 2)')
        self.to_remove.append('rand_auto_2')
        self.assertRastersDifference(
            'rand_auto_1', 'rand_auto_2',
            statistics=dict(min=-1, max=1, mean=0),
            precision=0.5)  # low precision, we have few cells

if __name__ == '__main__':
    grass.gunittest.test()
