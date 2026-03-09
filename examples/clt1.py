"""Example demonstrating CLT functionality in b3_mat."""

from b3_mat.materials import OrthotropicMaterial
from b3_mat.laminate import Laminate, calculate_laminate_properties

# Define a typical carbon/epoxy ply
carbon = OrthotropicMaterial(
    Ex=150e9,
    Ey=10e9,
    Ez=10e9,
    Gxy=5e9,
    Gxz=5e9,
    Gyz=3.5e9,
    nuxy=0.3,
    nuxz=0.3,
    nuyz=0.4,
    rho=1600.0,
    name="Carbon/Epoxy"
)

layers = [
    (carbon, 0.125e-3, 0),
    (carbon, 0.125e-3, 90),
    (carbon, 0.125e-3, 90),
    (carbon, 0.125e-3, 0),
]

print("=== CLT Example ===")
lam = Laminate(layers)

print("Engineering properties:")
eng = lam.engineering_properties()
for k, v in eng.items():
    print(f"  {k}: {v:.3e}")

print("\nA matrix (N/m):")
print(lam.A)

print("\nD matrix (Nm):")
print(lam.D)

print("\nUsing convenience function:")
props = calculate_laminate_properties(layers)
print(f"Ex = {props['Ex']:.3e} Pa")
