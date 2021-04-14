from pyeda.inter import *

from attractors import attractors
from attractors.fatal_attractors import monotone_attractor


def psolB(g):
    for curr_color in range(0, g.p + 1):
        player = curr_color % 2
        x = g.gamma[curr_color] & (g.phi_0 | g.phi_1)
        cache = expr2bdd(expr(False))
        while not (x.is_zero() or x is cache):
            cache = x
            m_attr_x = monotone_attractor(g, player, x, curr_color)
            if (m_attr_x | x) is m_attr_x:
                attr_ma = attractors.attractor(g, player, m_attr_x)
                ind_game = g.induced_game(~attr_ma)
                (w_0, w_1) = psolB(ind_game)
                if player == 0:
                    w_0 = w_0 | attr_ma
                else:
                    w_1 = w_1 | attr_ma
                return w_0, w_1
            else:
                x = x & m_attr_x

    return expr2bdd(expr(False)), expr2bdd(expr(False))