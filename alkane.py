#practicing with CO first
from pydft import MoleculeBuilder, DFT

CO = MoleculeBuilder().from_name("CO")

dft=DFT(CO, basis='sto3g')

res=dft.scf(tol=1e-4)

print("Total Electronic energy: %.6f Ht"%res['energy'])
