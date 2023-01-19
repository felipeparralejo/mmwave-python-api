"""

RECORD AND SAVE DCA1000 DATA
============================

Read FRAMES from DCA1000 and save a .dat file with a dictionary with these keys:

    - DESC: description of the acquired data
    - id: shortened description
    - date: time of recording
    - config: dictionary with DCA1000 configuration
    - frames: number of recorded frames
    - data: recorded data

"""

from datetime import datetime
import pickle
from dca1000 import DCA1000
from params import PARAMS

<<<<<<< HEAD
FRAMES = 20
DESC = 'static corner reflector QM office'
=======
FRAMES = 100
DESC = 'Person walking configured with params from demo visualizer for comparison'
>>>>>>> 6c1dc784e6391bfdfb36cb4821696cc70180c1e9

dca = DCA1000()

data = []

for _ in range(FRAMES):
    dca._clear_buffer()
    adc_data = dca.read()
    data.append(adc_data)

date = datetime.now().strftime('%d-%m-%y')
desc_short = ''.join([c[0].upper() for c in DESC.split()])

obj = {'description': DESC,
       'id': desc_short,
       'date': datetime.now().strftime('%d/%m/%y-%H:%M:%S'),
       'config': PARAMS.CONFIG,
       'frames': FRAMES,
       'data': data}

pickle.dump(obj, open(f'./data/openradar_{date}_{desc_short}.dat', 'bw'))
