#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_palette`
=======================

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>
Created on 2016-09-13, 09:38

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import pytest
import numpy as np

from hitherdither import palette
from hitherdither.exceptions import PaletteCouldNotBeCreatedError
from hitherdither.data import scene, scene_bayer0, scene_undithered
from .tools import test_jpeg, test_png


@pytest.mark.parametrize("hex_colour, rgb_colour", (("#ffffff", (255,255,255)),
                                                    ("#abcdef", (171,205,239)),
                                                    ("#012345", (1, 35, 69)),
                                                    (0x82f698, (130, 246, 152)),
                                                    ("0x82f698", (130, 246, 152))))
def test_hex2rgb(hex_colour, rgb_colour):
    assert palette.hex2rgb(hex_colour) == rgb_colour


@pytest.mark.parametrize("hex_colour, rgb_colour", (("#ffffff", (255,255,255)),
                                                    ("#abcdef", (171,205,239)),
                                                    ("#012345", (1, 35, 69)),
                                                    (0x82f698, (130, 246, 152)),
                                                    ("0x82f698", (130, 246, 152))))
def test_rgb2hex(hex_colour, rgb_colour):
    try:
        if isinstance(hex_colour, int):
            hc = hex_colour
        else:
            hc = int(hex_colour, 16)
    except:
        hc = int(hex_colour[1:], 16)
    assert palette.rgb2hex(*rgb_colour) == hc


@pytest.mark.parametrize("input_data, n_colours",
                         (([
                               np.array((255, 255, 255)),
                               np.array((171, 205, 239)),
                               np.array((1, 35, 69)),
                               np.array((130, 246, 152))
                           ], 4),
                          ([
                               (255, 255, 255),
                               (171, 205, 239),
                               (1, 35, 69),
                               (130, 246, 152)
                           ], 4),
                          (np.array([
                               (255, 255, 255),
                               (171, 205, 239),
                               (1, 35, 69),
                               (130, 246, 152),
                               (0, 0, 0)
                           ]), 5),
                          ([
                               "#ff21ee",
                               "#123456",
                               "#abcdef",
                               "#000000",
                           ], 4),
                          ([
                               0xff21ee,
                               0x123456,
                               0xabcdef,
                               0x000000,
                           ], 4),
                          (test_png().convert('P'), 104),
                          (test_jpeg().convert('P'), (80, 82)),
                          (scene_bayer0(), 16),
                          (scene_undithered(), 16),
                         ))
def test_create(input_data, n_colours):
    p = palette.Palette(input_data)
    if isinstance(n_colours, tuple):
        # JPEG gets 80 colours in Python 2.7.9 and 3.4,
        # 82 in Python 2.7.12 and 3.5, 3.6...
        assert len(p) in n_colours
        assert len([c for c in p]) in n_colours
    else:
        assert len(p) == n_colours
        assert len([c for c in p]) == n_colours


@pytest.mark.parametrize("input_data, n_colours",
                         (
                          (test_png(), 104),
                          (test_jpeg(), 82),
                          (test_jpeg().convert("L"), 82),
                          (scene(), 82)
                         ))
def test_create_fails(input_data, n_colours):
    with pytest.raises(PaletteCouldNotBeCreatedError):
        p = palette.Palette(input_data)
