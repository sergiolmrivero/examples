"""
macro_equations.py

This module implements each macroeconomic equation from the file 'rolim_lima_baltar.tex' as a standalone Python function.
Each function's parameters are the independent variables, and the dependent variable is returned.
"""
import math

def prob_innovation_success(zeta, L_res):
    """Equation 1: Probability of innovation success"""
    return 1 - math.exp(-zeta * L_res)

def new_consumption_good_productivity(y_c_star, x_c):
    """Equation 2: New consumption good productivity if innovation succeeds"""
    return y_c_star * (1 + x_c)

def new_capital_good_productivity(y_k, x_k):
    """Equation 3: New capital good productivity if innovation succeeds"""
    return y_k * (1 + x_k)

def technology_adoption_rule(p_k_old, gamma_old, p_k_new, gamma_new, b):
    """Equation 4: Technology adoption rule (minimizes cost)"""
    return min(p_k_old + b * gamma_old, p_k_new + b * gamma_new)

def direct_labor_demand_capital(I_c_D_sum, y_k):
    """Equation 5: Direct labor demand (capital goods firm)"""
    return math.ceil(I_c_D_sum / y_k)

def indirect_labor_demand_capital(rho2, I_c_D_nom_sum, w_k_ind, rho3, L_k_dir):
    """Equation 6: Indirect labor demand (capital goods firm)"""
    return math.floor(rho2 * I_c_D_nom_sum / w_k_ind) + math.floor(rho3 * L_k_dir)

def capital_goods_production(L_k_dir, y_k, h, L_k_man_D, L_k_dir_D, L_k_man, L_k_dir_actual, Q_indicator, I_c_D_sum):
    """Equation 7: Capital goods production (with management adjustment)"""
    management_shortage = (L_k_man_D / L_k_dir_D - L_k_man / L_k_dir_actual) if Q_indicator else 0
    prod = abs(L_k_dir * y_k * (1 - h * management_shortage))
    return min(prod, I_c_D_sum)

def price_new_machines(mu_k, w_k_dir, rho3, w_k_ind, y_k):
    """Equation 8: Price of new machines"""
    return (1 + mu_k) * (w_k_dir + rho3 * w_k_ind) / y_k

def direct_labor_demand_consumption(Q_c_d, y_c_star_avg):
    """Equation 9: Direct labor demand (consumption goods firms)"""
    return math.ceil(Q_c_d / y_c_star_avg)

def indirect_labor_demand_consumption(rho4, L_c_dir, rho5, L_c_dir_fc):
    """Equation 10: Indirect labor demand (consumption goods firms)"""
    return rho4 * L_c_dir + rho5 * L_c_dir_fc

def consumption_goods_production(L_c_dir, y_c_avg, h, L_c_ind_D, L_c_dir_D, L_c_ind, L_c_dir_actual, Q_indicator):
    """Equation 11: Consumption goods production (with management adjustment)"""
    management_shortage = (L_c_ind_D / L_c_dir_D - L_c_ind / L_c_dir_actual) if Q_indicator else 0
    return L_c_dir * y_c_avg * (1 - h * management_shortage)

def payback_period(p_k, gamma_y_m, gamma_y_star):
    """Equation 12: Payback period for machine replacement"""
    return p_k / (gamma_y_m - gamma_y_star)

def markup_market_share(mu_c_prev, nu1, ms_c_prev, ms_c_prev2):
    """Equation 13: Mark-up rate component based on market share"""
    return mu_c_prev * (1 + nu1 * (ms_c_prev / ms_c_prev2 - 1))

def markup_unit_costs(m_c_prev, nu2, nu3, delta_gamma, gamma_prev):
    """Equation 14: Mark-up rate deviation based on unit costs"""
    return nu2 * m_c_prev - nu3 * (delta_gamma / gamma_prev)

def firm_competitiveness(p_n, l_n):
    """Equation 15: Firm competitiveness"""
    return (1 - p_n + 1 - l_n) / 2

def market_share_evolution(ms_c_prev, nu4, E_c, E_avg):
    """Equation 16: Market share evolution"""
    return ms_c_prev * (1 + nu4 * (E_c - E_avg) / E_avg)

def markup_deviation_exports(m_c_prime_prev, nu2, nu5, delta_X_D_prev, X_D_prev2):
    """Equation 17: Mark-up deviation for exports"""
    return nu2 * m_c_prime_prev - nu5 * (delta_X_D_prev / X_D_prev2)

def export_price(k, p_x_x, mu_c_star, m_c, m_c_prime, gamma_u, epsilon):
    """Equation 18: Export price (in foreign currency)"""
    return k * p_x_x + (1 - k) * ((1 + mu_c_star + m_c + m_c_prime) * gamma_u / epsilon)

def export_market_share(iota2, p_x_c, p_x_x, iota3):
    """Equation 19: Export market share"""
    return iota2 * (1 - math.exp(-pow(p_x_c / p_x_x, iota3)))

def real_export_demand(ms_c_prime, c_x, Y_x):
    """Equation 20: Real export demand"""
    return ms_c_prime * c_x * Y_x

def realized_exports(Q_c_s, Q_c_D, X_c_D):
    """Equation 21: Realized exports (if supply < demand)"""
    return Q_c_s / Q_c_D * X_c_D

def desired_wage_worker(w_h_star, gamma1, g_prev, indicator_g, T_w, gamma2):
    """Equation 22: Desired wage by workers"""
    if T_w == 0:
        return w_h_star * (1 + gamma1 * g_prev * indicator_g)
    else:
        return w_h_star * (1 - gamma2 * T_w)

def household_consumption_demand(c1, C_h_prev, p_C_prev, p_C_exp, c2_j, w_h, Pi_h_prev, tau, d_h, c3, D_h):
    """Equation 23: Household consumption demand"""
    option1 = c1 * (C_h_prev / p_C_prev) * p_C_exp
    option2 = c2_j * ((w_h + Pi_h_prev) * (1 - tau) + d_h) + c3 * D_h
    return max(option1, option2)

def interest_rate_rule(lambda1, p_hat_prev, lambda2, p_hat_T, i_prev):
    """Equation 24: Interest rate rule (inflation targeting)"""
    return (1 - lambda1) * (p_hat_prev + lambda2 * (p_hat_prev - p_hat_T)) + lambda1 * i_prev

def firm_desired_wage(w_f_prev, gamma3, eta_prev, eta_prev2):
    """Equation 25: Firm's desired wage"""
    return w_f_prev * (1 + gamma3 * (eta_prev - eta_prev2))

def wage_setting(phi, eta_prev, w_f_d, w_f_s):
    """Equation 26: Wage setting (bargaining)"""
    return (1 - phi * eta_prev) * w_f_d + phi * eta_prev * w_f_s

def price_imported_goods(p_x_x, epsilon):
    """Equation 27: Price of imported goods"""
    return p_x_x * epsilon

def import_market_share(iota4, p_C_avg, p_x, iota5):
    """Equation 28: Import market share"""
    return iota4 * (1 - math.exp(-pow(p_C_avg / p_x, iota5)))

def nominal_import_demand(ms_x, p_x, C_h_D_sum):
    """Equation 29: Nominal import demand/realized imports"""
    return ms_x * p_x * C_h_D_sum

def nominal_exchange_rate(epsilon_prev, lambda3, X_prev, IM_prev, Y_prev, lambda4, delta_i_diff_sum):
    """Equation 30: Nominal exchange rate dynamics"""
    return epsilon_prev * (1 - lambda3 * (X_prev - IM_prev) / Y_prev + lambda4 * delta_i_diff_sum)

def real_exchange_rate(epsilon, p_x_x, p_C_star):
    """Equation 31: Real exchange rate"""
    return epsilon * p_x_x / p_C_star
