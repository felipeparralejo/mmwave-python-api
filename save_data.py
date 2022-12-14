from datetime import datetime
import pickle
from mmwave.dataloader import DCA1000

FRAMES = 10

dca = DCA1000()

data = []

for _ in range(FRAMES):
    dca._clear_buffer()
    adc_data = dca.read()
    data.append(adc_data)

date = datetime.now().strftime('%d-%m-%y_%Hh%Mm%Ss')
pickle.dump(data, open(f'./data/openradar_{FRAMES}_frames_{date}.dat', 'bw'))
