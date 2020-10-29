import mylibrary as ml
import matplotlib.pyplot as plt

soundfile = '../soundfiles/aiueo3.wav'
fig1 = '../graphfiles/a22.png'
fig2 = '../graphfiles/a22_spct.png'

fs = 16000

x, data = ml.read_wav(soundfile)
t = len(data) // fs

ml.init_graph()
plt.plot(x, data)
plt.savefig(fig1)
plt.show()


ml.make_spct(fig2, data, t)