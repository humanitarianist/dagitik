import numpy as np
import matplotlib.pyplot as plt

mu1, sigma1 = 1, 1.2
mu2, sigma2 = 4, 1.3

# Histogramlarin dizi olarak tanimlanmasi
histogram1, histogram2 = [0]*41, [0]*41

# Belirtilen yontemle hesaplanacak olan iki histogramin arasindaki mesafeyi ifade eden degisken
distance = 0

# Birinci histogramin olusturulmasi
for i in range(0, 10000):
    e = int(round(np.random.normal(mu1, sigma1)))
    while e < -20 or e > 20:
        e = int(round(np.random.normal(mu1, sigma1)))
    histogram1[20 + e] += 1

# Ikinci histogramin olusturulmasi
for i in range(0, 10000):
    e = int(round(np.random.normal(mu2, sigma2)))
    while e < -20 or e > 20:
        e = int(round(np.random.normal(mu2, sigma2)))
    histogram2[20 + e] += 1

# Histogramlarin normalize edilmesi
for i in range(0, 41):
    histogram1[i] = float(histogram1[i])/10000
    histogram2[i] = float(histogram2[i])/10000

plt.bar(range(-20, 21), histogram1, alpha=0.7, color="r")
plt.bar(range(-20, 21), histogram2, alpha=0.7, color="b")
plt.xlabel('x ekseni')
plt.ylabel('y ekseni')
plt.title("iki ornek Histogram" "\n" " $\mu1=$ " + repr(mu1) + ", $\sigma1=$" + repr(sigma1) + "\n"
                                     " $\mu2=$ " + repr(mu2) + ", $\sigma2=$" + repr(sigma2))
plt.xticks(np.arange(-20, 20, 2))

plt.show()

# Iki histogramin arasindaki mesafenin olculmesi
for i in range(0, 41):
    if histogram1[i] == 0:
        pass
    for j in range(0, 41):
        if histogram2[j] == 0:
            pass
        if histogram2[j] > 0 and histogram2[j] >= histogram1[i]:
            distance += histogram1[i] * abs(j - i)
            histogram2[j] -= histogram1[i]
        if histogram1[i] > histogram2[j] > 0:
            distance += histogram2[j] * abs(j - i)
            histogram2[j] = 0
            histogram1[i] -= histogram2[j]

# Mesafeyi ekrana yazdirma
print "DISTANCE = " + repr(distance)

