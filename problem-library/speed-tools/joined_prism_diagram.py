"""
Reusable diagram generator for "joined two rectangular prisms" volume problems.

Why this exists (2026-10-17): a full isometric 3D render of a composite
step-shaped solid is a trap -- however carefully the two boxes' touching
faces are built, the join reads as ambiguous (does the tall box's height
label include the short box's or not?). Took 3 rounds to find this out the
hard way on QR5 #20. The real official diagrams (Test Innovators "Volume of
Solids" series) and this repo's own already-approved redo-set-2/3 diagrams
never use full isometric for this -- they draw a TRUE-TO-SCALE flat 2D
L-shaped front outline (so the two height segments visually stack with no
ambiguity and the step is a real geometric corner) plus two small
parallelogram "flaps" only, at the step and the outer-top corner, to cue
depth. Reserve full isometric rendering for a SINGLE solid (one cube/prism,
e.g. QR4 #27's shaded unit cube) -- it's composite/joined shapes specifically
where it fails. Full writeup: GENERATION_WORKFLOW.md, "Diagram-type sanity
check".

Usage:
    from joined_prism_diagram import joined_prisms_svg
    diag = joined_prisms_svg(w1=4, h1=9, w2=6, h2=5, depth=4)

This draws a narrower prism (w1 x depth x h1) sitting on top of a wider one
(w2 x depth x h2), both flush-left, matching the standard real-test layout
(small block upper-left, step down to a wider block lower-right). w1 must
be <= w2. Produces 6 labels by default: both top-face edges of the small
block (width + depth, since the real diagrams label both even when a value
repeats), the small block's own height, the total combined outer-left
height (a built-in consistency check the real test includes), the large
block's own height, and the large block's full bottom width. The shared
depth is labeled once (on the small block's flap) per the usual "depth
labeled once" convention -- pass label_depth=False to omit it entirely if
the question text already states it.

Tuned and verified against QR5 #20's real values (w1=4, h1=9, w2=6, h2=5,
depth=4) -- that combination renders cleanly, byte-for-byte reproducible.
For very different proportions (w1 much smaller than w2, or two-digit
labels), re-render and eyeball it before publishing: the fixed label
offsets can crowd or clip at extreme aspect ratios. Always QA-check inside
a real `.card` with the page's actual CSS (see GENERATION_WORKFLOW.md) in
both themes before shipping, same as any other diagram.
"""


def joined_prisms_svg(w1, h1, w2, h2, depth, unit='', sc=9, label_depth=True):
    assert w1 <= w2, "the narrower prism (w1) must sit within the wider one's footprint (w2)"

    x0, y0 = 20, 16
    off = (13, -10)  # fixed decorative "receding into depth" offset; NOT scaled by the true depth value

    A = (x0, y0)
    B = (x0 + w1 * sc, y0)
    C = (x0 + w1 * sc, y0 + h1 * sc)
    D = (x0 + w2 * sc, y0 + h1 * sc)
    E = (x0 + w2 * sc, y0 + (h1 + h2) * sc)
    F = (x0, y0 + (h1 + h2) * sc)

    def add(p, o):
        return (p[0] + o[0], p[1] + o[1])

    flap1 = [A, B, add(B, off), add(A, off)]
    side1 = [B, C, add(C, off), add(B, off)]
    flap2 = [C, D, add(D, off), add(C, off)]
    side2 = [D, E, add(E, off), add(D, off)]
    outline = [A, B, C, D, E, F]

    def poly(pts, fill, sw=1.3):
        s_ = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        return f'<polygon points="{s_}" fill="{fill}" stroke="currentColor" stroke-width="{sw}"/>'

    parts = [
        poly(flap1, 'var(--surface-alt)'),
        poly(flap2, 'var(--surface-alt)'),
        poly(side1, 'var(--surface)'),
        poly(side2, 'var(--surface)'),
        poly(outline, 'none', sw=1.8),
    ]

    def text(x, y, t, anchor='middle'):
        return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="11" fill="currentColor">{t}</text>'

    u = f' {unit}' if unit else ''
    labels = []
    mx = (A[0] + B[0]) / 2
    labels.append(text(mx + 4, A[1] + off[1] - 8, f'{w1}{u}'))
    if label_depth:
        Ao = add(A, off)
        mx, my = (A[0] + Ao[0]) / 2, (A[1] + Ao[1]) / 2
        labels.append(text(A[0] - 6, my - 2, f'{depth}{u}', anchor='end'))
    mx, my = B[0], (B[1] + C[1]) / 2
    labels.append(text(mx - 8, my, f'{h1}{u}', anchor='end'))
    mx, my = D[0], (D[1] + E[1]) / 2
    labels.append(text(mx + 16, my, f'{h2}{u}', anchor='start'))
    mx, my = A[0], (A[1] + F[1]) / 2
    labels.append(text(mx - 8, my, f'{h1 + h2}{u}', anchor='end'))
    mx, my = (F[0] + E[0]) / 2, F[1]
    labels.append(text(mx, my + 14, f'{w2}{u}'))

    Ao = add(A, off)
    minx = min(p[0] for p in [A, B, C, D, E, F, Ao]) - 30
    maxx = flap2[2][0] + 10
    miny = min(Ao[1], flap1[2][1]) - 18
    maxy = F[1] + 20
    vb_w, vb_h = maxx - minx, maxy - miny

    return (f'<svg viewBox="{minx:.1f} {miny:.1f} {vb_w:.1f} {vb_h:.1f}" '
            f'width="{vb_w:.0f}" height="{vb_h:.0f}" role="img">'
            + ''.join(parts) + ''.join(labels) + '</svg>')


if __name__ == '__main__':
    # smoke test matching QR5 #20's real values
    print(joined_prisms_svg(w1=4, h1=9, w2=6, h2=5, depth=4))
