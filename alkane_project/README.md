drew a PES(Potential Energy Surface) of Ethane using PyDFT in following order/attempts.

1. obtained the coordinates of Ethane from Avogadro
2. successfully read the input Avogadro file from Python
3. attempted to plot the energy curve but failed because the energy calculation did not converge for some bond lengths that were too long for PyPDF to cover
4. tried the other way around - to reduce the bond length from 2.0 Angstrom to 1.0 Angstrom (both within the range of PYDFT convergence)
5. attempted to plot the energy curve but failed because Hydrogens were facing inwards
6. fixed the Hydrogens orientation (to face outward) and successfully drew the energy curve

