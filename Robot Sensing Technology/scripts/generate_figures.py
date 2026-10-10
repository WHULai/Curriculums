"""Regenerate all vector diagrams in img/ using NumPy and Matplotlib.

Rendering coordinates are internal drawing coordinates. Figures use symbolic
parameter labels, exact key points, and explicitly stated schematic shapes.
No arbitrary numerical parameter choices are printed on the final figures.
"""
from theory_figures import generate_all as theory_figures
from exam_figures import generate_all as exam_figures

if __name__ == '__main__':
    theory_figures()
    exam_figures()
    print('Generated review diagrams and exam-style vector spectrum figures.')
