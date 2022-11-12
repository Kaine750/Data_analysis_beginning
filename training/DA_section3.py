from matplotlib import pyplot as plt
import numpy as np

guzai = np.linspace(-1, 1, 1000)
lam = [5,50]

def calc_S_t(lam):
    S1 = (1 + np.sinh(lam*guzai)/np.sinh(lam))/2
    S2 = 1 - np.sinh(lam*guzai)/np.sinh(lam)
    tau = lam*np.cosh(lam*guzai)/np.sinh(lam)/2
    return S1, S2, tau
    
def show_S(lam,S1,S2):
    plt.plot(guzai, S1, label="S_1 (λ={})".format(lam))
    plt.plot(guzai, S2, label="S_2 (λ={})".format(lam))
    plt.xlabel("ξ")
    plt.ylabel("S")
    
def show_t(lam,tau):
    plt.plot(guzai, tau, label="τ (λ={})".format(lam))
    plt.xlabel("ξ")
    plt.ylabel("τ")
    
S1 = np.zeros((2,1000))
S2 = np.zeros((2,1000))
tau = np.zeros((2,1000))

for i in range(2):
    S1[i], S2[i], tau[i] = calc_S_t(lam[i])

plt.plot(guzai, S1[0], label="S_1 (λ=5)")
plt.plot(guzai, S2[0], label="S_2 (λ=5)")
plt.plot(guzai, S1[1], label="S_1 (λ=50)")
plt.plot(guzai, S2[1], label="S_2 (λ=50)")
plt.title("Relationship between displacement and axial stress")
plt.xlabel("ξ")
plt.ylabel("S")
plt.legend()
plt.show()

plt.plot(guzai, tau[0], label="τ (λ=5)")
plt.plot(guzai, tau[1], label="τ (λ=50)")
plt.title("Relationship between displacement and shear stress")
plt.xlabel("ξ")
plt.ylabel("τ")
plt.legend()
plt.show()