"""."""
import numpy as _np


def _get_matrix_ss_section(leng):
    return _np.array([
        [1, -leng/2, 0, 0],
        [1, leng/2, 0, 0],
        [0, 0, 1, -leng/2],
        [0, 0, 1, leng/2]])


# NOTE: these matrices translates the desired angle and positions of
# the bump to the BPM orbit distortions needed to get them.
BUMP_MATRICES = {
    'SA': _get_matrix_ss_section(7.0358),
    'SB': _get_matrix_ss_section(6.1758),
    'SP': _get_matrix_ss_section(6.1758),
    # The BC matrix was calculated using the storage ring model.
    # The script used calculate it is
    'BC': _np.array([
        [1.11371, -0.61624, 0, 0],
        [1.25316, 1.54265, 0, 0],
        [0, 0, 0.90631, -0.57170],
        [0, 0, 0.69528, 1.80929]]),
    }


def si_calculate_bump(orbx, orby, subsec, agx=0, agy=0, psx=0, psy=0):
    """Calculate bumps on SA, SB, SP and BC subsections.

    Inputs:
        agx, agy, psx, psy - are the desired angles and positions at the
            center of the straight section/center of BC. The must have the same
            unit as orbx and orby.
        subsec - is a 4 character string with the name of the subsection where
            the bump is to be made. Examples: '01SA', '10SA', '13BC', '02SB'
        orbx, orby - the 160 long vector related to the storage ring orbit.
            Ideally this is the reference orbit around which the bump will be
            made.

    Outputs:
        orbx, orby - The orbits with the bump applied to them
    """
    # These are the indices of the BPMs inside one section of the ring:
    bpmidcs = {'BC': 4, 'SA': 0, 'SB': 0, 'SP': 0}

    # get section and subsection
    sec = int(subsec[:2])
    if not 1 <= sec <= 20:
        raise ValueError('Section must be between 01..20.')
    sec -= 1
    subname = subsec[2:]

    vec = _np.array([psx, agx, psy, agy])
    pos_bpm = _np.dot(BUMP_MATRICES[subname], vec)

    bpm1 = sec * 8 + bpmidcs[subname] - 1
    bpm2 = sec * 8 + bpmidcs[subname]

    orbx, orby = orbx.copy(), orby.copy()
    orbx[bpm1] += pos_bpm[0]
    orbx[bpm2] += pos_bpm[1]
    orby[bpm1] += pos_bpm[2]
    orby[bpm2] += pos_bpm[3]
    return orbx, orby
