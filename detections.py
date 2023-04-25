from skyfield.api import load

ts = load.timescale()
file = open('epochs.txt', 'a')
for _ in range(10):
    time = ts.now().tt_strftime()
    file.write(time + '\n')
file.close()