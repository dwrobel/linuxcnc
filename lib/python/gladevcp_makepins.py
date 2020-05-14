# Backward compatible name

from __future__ import absolute_import
import warnings

warnings.warn("gladevcp_makepins name is deprecated. Use gladevcp.makepins instead")

from gladevcp.makepins import *
