from imaging_grid import ImagingGrid

import unittest

class TestImagingGrid(unittest.TestCase):
    def test_simple(self):
        grid = ImagingGrid((0,0), 50.0, 25.0, 25.0)
        # we expect there to be 6 imaging locaions
        # ... top left isn't fully in view, so need an additional row and col
        self.assertEqual(grid.get_num_cells(), 6)
        
        # the first cell should have a center of top left
        self.assertEqual(grid.get_cell(0).get_center_location(), (0, 0))

        # should be able to call all get_cells without error
        for i in range(grid.get_num_cells()):
            cell = grid.get_cell(i)
            print(cell.get_center_location())

        # cell locations should positively increase (unless the wrap lol)

        prev_grid = grid.get_cell(0)    
        for i in range(1, grid.get_num_cells()):
            new_grid = grid.get_cell(i)
            self.assertTrue(new_grid.get_center_location()[1] >= prev_grid.get_center_location()[1])
            prev_grid = new_grid

    def test_update(self):
        grid = ImagingGrid((5,5), 10., 5., 5.)  