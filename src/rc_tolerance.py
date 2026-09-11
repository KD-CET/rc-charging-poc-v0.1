import numpy as np
import matplotlib.pyplot as plt

V0 = 5.0
VIH = 0.7 * V0

# R and C chosen for the LED lamp appliance controller (Part A),
# with tolerances typical of cheap general-purpose parts
# (5% carbon-film resistor, 20% Y5V/Z5U ceramic capacitor).
R_nominal = 150e3   # ohm
C_nominal = 100e-9  # F
R_tol = 0.05          # +-5%
C_tol = 0.20          # +-20%

R_min, R_max = R_nominal * (1 - R_tol), R_nominal * (1 + R_tol)
C_min, C_max = C_nominal * (1 - C_tol), C_nominal * (1 + C_tol)

def t_release(R, C):
    return -R * C * np.log(1 - VIH / V0)

# Both R and C increase t_release together here (their product's coefficient
# is a positive constant independent of R, C), so fastest = both minimum,
# slowest = both maximum.
t_nom = t_release(R_nominal, C_nominal)
t_fast = t_release(R_min, C_min)
t_slow = t_release(R_max, C_max)

def charging(t, R, C):
    tau = R * C
    return V0 * (1 - np.exp(-t / tau))

t_max = max(t_nom, t_fast, t_slow)
t = np.linspace(0, 5 * t_max, 500)

fig, ax = plt.subplots()
ax.plot(t, charging(t, R_nominal, C_nominal), color="black", linewidth=2.5,
        label=f"Nominal (R={R_nominal/1e3:.0f} k$\\Omega$, C={C_nominal*1e9:.0f} nF)")
ax.plot(t, charging(t, R_min, C_min), color="black", linestyle="--", linewidth=1.3,
        label="Fastest case (-5% R, -20% C)")
ax.plot(t, charging(t, R_max, C_max), color="black", linestyle="-.", linewidth=1.3,
        label="Slowest case (+5% R, +20% C)")
ax.axhline(VIH, linestyle=":", color="0.4")
ax.grid(False)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")
ax.set_title("POR timing under component tolerance")
ax.legend()

fig.savefig("figures/generated/rc_tolerance.pdf")