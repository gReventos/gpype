import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

csv_file = "test_20250211_113032.csv"
montage = ['C3', 'CP3', 'Cz', 'C4', 'CP4', 'PO7', 'POz', 'PO8']
id_target = 2
id_nontarget = 1
# csv_file = "test_20250213_144216.csv"

fs = 250
t_pre = 0.1
t_post = 0.7

data = pd.read_csv(csv_file, header=None).values
trigger = np.round(data[1:, 9].astype(float)).astype(int)
y = data[1:, 1:9].astype(float)

trig_nt = np.where(np.round(trigger) == id_nontarget)[0]
trig_t = np.where(np.round(trigger) == id_target)[0]

n_vec_trig = np.arange(-int(t_pre * fs), int(t_post * fs) + 1)
t_vec_trig = n_vec_trig / fs

y_nt_trig = np.array([y[idx + n_vec_trig, :]
                      for idx in trig_nt if idx + n_vec_trig[-1] < len(y)])
y_t_trig = np.array([y[idx + n_vec_trig, :]
                     for idx in trig_t if idx + n_vec_trig[-1] < len(y)])

y_target = np.mean(y_t_trig, axis=0)
y_nontarget = np.mean(y_nt_trig, axis=0)


offset = np.arange(8) * 10
plt.figure()
for i in range(y_target.shape[1]):
    plt.plot(t_vec_trig,
             y_target[:, i] - y_nontarget[:, i] + offset[i],
             label=montage[i])

plt.xlabel('Time relative to Stimulus onset (s)')
plt.yticks(offset, montage)
plt.grid(True)
plt.box(True)
plt.show()
