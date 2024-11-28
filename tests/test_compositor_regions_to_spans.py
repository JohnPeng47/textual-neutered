from textual._compositor import Compositor
from textual.geometry import Region


def test_regions_to_ranges_disjoint_regions_same_line():
    regions = [Region(0, 0, 1, 2), Region(2, 0, 1, 1)]
    assert list(Compositor._regions_to_spans(regions)) == [
        (0, 0, 1),
        (0, 2, 3),
        (1, 0, 1),
    ]


def test_regions_to_ranges_directly_adjacent_ranges_merged():
    regions = [Region(0, 0, 1, 2), Region(1, 0, 1, 2)]
    assert list(Compositor._regions_to_spans(regions)) == [
        (0, 0, 2),
        (1, 0, 2),
    ]
