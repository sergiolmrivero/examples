"""
Auto-generated from nd-09_Equations_to_implement.tex
Each function implements one equation from the model.
"""
import numpy as np

def zc_expectation(zc_e_prev, zc_prev, lam):
    """z^e_{ct} = z^e_{ct-1} + lambda * (z_{ct-1} - z^e_{ct-1})"""
    return zc_e_prev + lam * (zc_prev - zc_e_prev)

def yD_ct(se_ct, nu, inv_ct_prev):
    """y^D_{ct} = s^e_{ct}(1 + nu) - inv_{ct-1}"""
    return se_ct * (1 + nu) - inv_ct_prev

def uD_ct(yD_ct, k_ct, mu_k):
    """u^D_{ct} = min(1, y^D_{ct} / (k_{ct} * mu_k))"""
    return min(1, yD_ct / (k_ct * mu_k))

def ND_ct(uD_ct, k_ct, l_k):
    """N^D_{ct} = u^D_{ct} * k_{ct} / l_k"""
    return uD_ct * k_ct / l_k

def N_ct(ND_ct, N_ct_prev):
    """N_{ct} = N^D_{ct} - N_{ct-1}"""
    return ND_ct - N_ct_prev

def mu_ct(mu_ct_prev, FN):
    """mu_{ct} = mu_{ct-1} * (1 ± FN)"""
    return mu_ct_prev * (1 + FN)

def p_ct(mu_ct, We_ct, ND_ct, yD_ct):
    """p_{ct} = (1 + mu_{ct}) * (We_{ct} * ND_{ct}) / yD_{ct}"""
    return (1 + mu_ct) * (We_ct * ND_ct) / yD_ct

def C_ct(W_ct, Lp_ct, C_kct):
    """C_{ct} = W_{ct} + Lp_{ct} + C_{kct}"""
    return W_ct + Lp_ct + C_kct

def W_ct(w_nt):
    """W_{ct} = sum of wages paid to workers n in ct"""
    return np.sum(w_nt)

def Lp_ct(i_l_j, L_cj, eta, t):
    """Lp_{ct} = sum over j = t-eta to t-1 of i^l_j * L_{cj} * (eta - ((t-1)-j))/eta"""
    return sum(i * L * (eta - ((t-1)-j))/eta for i, L, j in zip(i_l_j, L_cj, range(t-eta, t)))

def C_kct(k_k, p_k, kappa):
    """C_{kct} = sum over k in K_{ct-1} of (k^k * p^k) / kappa"""
    return sum(kk * pk / kappa for kk, pk in zip(k_k, p_k))

def R_ct(Sr_ct, I_d, Inv_c):
    """R_{ct} = Sr_{ct} + I_d + Inv_c"""
    return Sr_ct + I_d + Inv_c

def Sr_ct(s_ct, p_ct):
    """Sr_{ct} = s_{ct} * p_{ct}"""
    return s_ct * p_ct

def I_dct(i_d_bt_prev, D_ct_prev):
    """I_{dct} = i^d_{bt-1} * D_{ct-1}"""
    return i_d_bt_prev * D_ct_prev

def Inv_ct(inv_ct, uc_ct, inv_ct_prev, uc_ct_prev):
    """Inv_{ct} = (inv_{ct} * uc_{ct} - inv_{ct-1} * uc_{ct-1})"""
    return (inv_ct * uc_ct) - (inv_ct_prev * uc_ct_prev)

def uc_ct(W_ct, ND_ct, y_ct):
    """uc_{ct} ≈ (W^e_{ct} * N^D_{ct}) / y_{ct}"""
    return W_ct * ND_ct / y_ct

def pi_ct(R_ct, C_ct):
    """pi_{ct} = R_{ct} - C_{ct}"""
    return R_ct - C_ct

def T_ct(tau_pi_ct, pi_ct):
    """T_{ct} = max(tau_pi_ct * pi_{ct}, 0)"""
    return max(tau_pi_ct * pi_ct, 0)

def Div_ct(rho_c, pi_ct, tau_pi_ct):
    """Div_{ct} = max(0, rho_c * pi_{ct} * (1 - tau_pi_ct))"""
    return max(0, rho_c * pi_ct * (1 - tau_pi_ct))

def OCF_ct(pi_ct, tau_c, C_kct, Inv_ct, Lp_ct):
    """OCF_{ct} = pi_{ct} * (1 - tau_c) + C_{kct} - Inv_{ct} - Lp_{ct}"""
    return pi_ct * (1 - tau_c) + C_kct - Inv_ct - Lp_ct

def r_ct(OCF, k_k, p_k, age_kt_prev, kappa):
    """r_{ct} = OCF / sum((k^k * p^k) * (1 - age_{kt-1}/kappa))"""
    denom = sum(kk * pk * (1 - age / kappa) for kk, pk, age in zip(k_k, p_k, age_kt_prev))
    return OCF / denom if denom != 0 else 0

def gD_ct(gamma1, r_ct_prev, r_bar, gamma2, uD_ct, u_bar):
    """g^D_{ct} = gamma1 * (r_{ct-1} - r_bar)/r_bar + gamma2 * (u^D_{ct} - u_bar)/u_bar"""
    return gamma1 * (r_ct_prev - r_bar) / r_bar + gamma2 * (uD_ct - u_bar) / u_bar

def iD_ct(gD_ct):
    """i^D_{ct} = g^D_{ct}"""
    return gD_ct

def ID_ct(iD_ct, p_k):
    """I^D_{ct} = i^D_{ct} * p^k"""
    return iD_ct * p_k

def LD_ct(ID_ct, Div_e_ct, sigma, We_ct, ND_ct, OCF_e_ct):
    """L^D_{ct} = I^D_{ct} + Div^e_{ct} + sigma * We_{ct} * ND_{ct} - OCF^e_{ct}"""
    return ID_ct + Div_e_ct + sigma * We_ct * ND_ct - OCF_e_ct

###############################
# KG firm equations
###############################
def zk_expectation(zk_e_prev, zc_prev, zc_e_prev, lam):
    """z^e_{kt} = z^e_{ct-1} + lambda * (z_{ct-1} - z^e_{ct-1})"""
    return zc_e_prev + lam * (zc_prev - zc_e_prev)

def yD_kt(se_kt, nu, inv_kt_prev):
    """y^D_{kt} = s^e_{kt}(1 + nu) - inv_{kt-1}"""
    return se_kt * (1 + nu) - inv_kt_prev

def ND_kt(yD_kt, mu_N):
    """N^D_{kt} = y^D_{kt} / mu_N"""
    return yD_kt / mu_N

def N_kt(ND_kt, N_kt_prev):
    """N_{kt} = N^D_{kt} - N_{kt-1}"""
    return ND_kt - N_kt_prev

def mu_kt(mu_ct_prev, FN):
    """mu_{kt} = mu_{ct-1} * (1 ± FN)"""
    return mu_ct_prev * (1 + FN)

def p_kt(mu_kt, We_kt, ND_kt, yD_kt):
    """p_{kt} = (1 + mu_{kt}) * (We_{kt} * ND_{kt}) / yD_{kt}"""
    return (1 + mu_kt) * (We_kt * ND_kt) / yD_kt

def C_kt(W_kt, I_lkt):
    """C_{kt} = W_{kt} + I_{lkt}"""
    return W_kt + I_lkt

def W_kt(w_nt):
    """W_{kt} = sum of wages paid to workers n in kt"""
    return np.sum(w_nt)

def I_lkt(i_l_j, L_cj, eta, t):
    """I_{lkt} = sum over j = t-eta to t-1 of i^l_j * L_{cj} * (eta - ((t-1)-j))/eta"""
    return sum(i * L * (eta - ((t-1)-j))/eta for i, L, j in zip(i_l_j, L_cj, range(t-eta, t)))

def R_kt(Sr_kt, I_dkt, Inv_kt):
    """R_{kt} = Sr_{kt} + I_{dkt} + Inv_{kt}"""
    return Sr_kt + I_dkt + Inv_kt

def Sr_kt(s_kt, p_kt):
    """Sr_{kt} = s_{kt} * p_{kt}"""
    return s_kt * p_kt

def I_dkt(i_d_bt_prev, D_kt_prev):
    """I_{dkt} = i^d_{bt-1} * D_{kt-1}"""
    return i_d_bt_prev * D_kt_prev

def Inv_kt(inv_kt, uc_kt, inv_kt_prev, uc_kt_prev):
    """Inv_{kt} = (inv_{kt} * uc_{kt} - inv_{kt-1} * uc_{kt-1})"""
    return (inv_kt * uc_kt) - (inv_kt_prev * uc_kt_prev)

def uc_kt(W_kt, ND_kt, y_kt):
    """uc_{kt} ≈ (W^e_{kt} * N^D_{kt}) / y_{kt}"""
    return W_kt * ND_kt / y_kt

def pi_kt(R_kt, C_kt):
    """pi_{kt} = R_{kt} - C_{kt}"""
    return R_kt - C_kt

def T_kt(tau_pi_kt, pi_kt):
    """T_{kt} = max(tau_pi_kt * pi_{kt}, 0)"""
    return max(tau_pi_kt * pi_kt, 0)

def Div_kt(rho_k, pi_kt, tau_pi_kt):
    """Div_{kt} = max(0, rho_k * pi_{kt} * (1 - tau_pi_kt))"""
    return max(0, rho_k * pi_kt * (1 - tau_pi_kt))

def OCF_kt(pi_kt, tau_k, Inv_kt, Lp_kt):
    """OCF_{kt} = pi_{kt} * (1 - tau_k) - Inv_{kt} - Lp_{kt}"""
    return pi_kt * (1 - tau_k) - Inv_kt - Lp_kt

def Lp_kt(i_l_j, L_kj, eta, t):
    """Lp_{kt} = sum over j = t-eta to t-1 of i^l_j * L_{kj} * (eta - ((t-1)-j))/eta"""
    return sum(i * L * (eta - ((t-1)-j))/eta for i, L, j in zip(i_l_j, L_kj, range(t-eta, t)))

def LD_kt(Div_e_kt, sigma, We_kt, ND_kt, OCF_e_kt):
    """L^D_{kt} = Div^e_{kt} + sigma * We_{kt} * ND_{kt} - OCF^e_{kt}"""
    return Div_e_kt + sigma * We_kt * ND_kt - OCF_e_kt

###############################
# Bank equations
###############################
def CR_bt(NW_bt, Ltot_bt):
    """CR_{bt} = NW_{bt} / Ltot_{bt}"""
    return NW_bt / Ltot_bt if Ltot_bt != 0 else 0

def i_l_bt(i_l_bt_prev, FN, CR_bt, CR_T_t):
    """Interest rate on loans, depends on capital ratio"""
    if CR_bt < CR_T_t:
        return i_l_bt_prev * (1 + FN)
    else:
        return i_l_bt_prev * (1 - FN)

def i_l_bt_avg(i_l_bt_prev_list):
    """Average interest rate in the prior period"""
    return np.mean(i_l_bt_prev_list)

def ds_Ld(i_l_bt, eta, Ld):
    """ds^{L^d} = (i^l_{bt} + 1/eta) * L^d"""
    return (i_l_bt + 1/eta) * Ld

def prD_x(OCF_xt, zeta_x, ds_Ld):
    """pr^D_x = 1 / (1 + exp((OCF_{xt} - zeta_x * ds^{L^d}) / ds^{L^d}))"""
    return 1 / (1 + np.exp((OCF_xt - zeta_x * ds_Ld) / ds_Ld))

def i_d_bt(i_d_bt_prev, FN, LR_bt, LR_T_t):
    """Interest rate on deposits, depends on liquidity ratio"""
    if LR_bt < LR_T_t:
        return i_d_bt_prev * (1 + FN)
    else:
        return i_d_bt_prev * (1 - FN)

def i_d_bt_avg(i_d_bt_prev_list):
    """Average deposit interest rate in the prior period"""
    return np.mean(i_d_bt_prev_list)

###############################
# Household equations
###############################
def pe_ht(pe_ht_prev, p_ht_prev, lam_h):
    """p^e_{ht} = p^e_{ht-1} + lambda_h * (p_{ht-1} - p^e_{ht-1})"""
    return pe_ht_prev + lam_h * (p_ht_prev - pe_ht_prev)

def wD_ht(wD_ht_prev, FN, u_hist, u_t_prev, upsilon):
    """Reservation wage update, see LaTeX for logic"""
    unemployed_quarters = sum(u_hist)
    if unemployed_quarters > 2:
        return wD_ht_prev * (1 - FN)
    elif unemployed_quarters > 2 and u_t_prev <= upsilon:
        return wD_ht_prev * (1 + FN)
    else:
        return wD_ht_prev

def y_ht(w_ht, iD_bt_prev, D_ht_prev, Div_ht):
    """y_{ht} = w_{ht} + i^D_{bt-1} * D_{ht-1} + Div_{ht}"""
    return w_ht + iD_bt_prev * D_ht_prev + Div_ht

def yd_h(tau_h, w_ht, iD_bt_prev, D_ht_prev, Div_ht, omega):
    """yd_h = (1 - tau_h) * (w_{ht} + i^D_{bt-1} * D_{ht-1} + Div_{ht}) + omega"""
    return (1 - tau_h) * (w_ht + iD_bt_prev * D_ht_prev + Div_ht) + omega

def cD_ht(alpha1, yd_ht, pe_ht, alpha2, NW_ht):
    """c^D_{ht} = alpha1 * yd_{ht} / pe_{ht} + alpha2 * NW_{ht} / pe_{ht}"""
    return alpha1 * yd_ht / pe_ht + alpha2 * NW_ht / pe_ht

###############################
# Government equations
###############################
def T_t(T_Ht, T_Kt, T_Ct, T_Bt):
    """T_t = T_Ht + T_Kt + T_Ct + T_Bt"""
    return T_Ht + T_Kt + T_Ct + T_Bt

def T_t_alt(tau_c, pi_ct, tau_k, pi_kt, tau_b, pi_bt, tau_h, y_ht):
    """T_t = tau_c * pi_ct + tau_k * pi_kt + tau_b * pi_bt + tau_h * y_ht"""
    return tau_c * pi_ct + tau_k * pi_kt + tau_b * pi_bt + tau_h * y_ht

def yg_t(T_t, pi_CBt):
    """yg_t = T_t + pi_CBt"""
    return T_t + pi_CBt

def N_gt(g, N_t):
    """N_{gt} = g * N_t"""
    return g * N_t

def govLayoff(upsilon, N_gt):
    """govLayoff = upsilon * N_{gt}"""
    return upsilon * N_gt

def W_gt(W_n):
    """W_{gt} = sum of W_n in N_{gt}"""
    return np.sum(W_n)

def UD_t(U_t, d_t):
    """UD_t = U_t * d_t"""
    return U_t * d_t

def B_t(p_b, b_t):
    """B_t = p_b * b_t"""
    return p_b * b_t

def G_t(W_gt, UD_t, i_b, B_t_prev):
    """G_t = W_{gt} + UD_t + i_b * B_{t-1}"""
    return W_gt + UD_t + i_b * B_t_prev

def Gb_t(yg_t, G_t):
    """Gb_t = yg_t - G_t"""
    return yg_t - G_t

###############################
# Central Bank equations
###############################
def pi_CBt(i_b, B_t_prev, i_a, CA_CBt):
    """pi_{CBt} = i_b * B_{t-1} + i_a * CA_{CBt}"""
    return i_b * B_t_prev + i_a * CA_CBt
