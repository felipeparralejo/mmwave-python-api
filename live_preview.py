"""

LIVE PREVIEWS
=============
Run a live preview

"""

from live_plots import liveRangePreview, liveRangeHeatmapPreview, liveAzimuthRangePreview
from dca1000 import DCA1000

dca = DCA1000()

liveRangePreview(dca)
# liveRangeHeatmapPreview(dca)
# liveAzimuthRangePreview(dca)
