# -*- coding: utf-8 -*-
"""
RATE Framework Calculation Engine
功能：计算心理时间(n)、物理时间(E[T])及时间悖论指数(TPI)
"""

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 模型函数定义
# ==========================================

def calc_psychological_time(r, sigma, risk_coeff=0.2):
    """
    计算心理时间 n (基于 ZZ-CAPM)
    公式: k = r + c(sigma), n = 1/k
    """
    k = r + risk_coeff * sigma
    return 1.0 / (k + 1e-6) # 防止分母为0

def calc_physical_time(g, sigma, M=2.0):
    """
    计算物理时间 E[T] (基于 GBM 首达时间)
    公式: E[T] = ln(M) / (g - 0.5 * sigma^2)
    """
    mu_geo = g - 0.5 * sigma**2
    
    # 物理极限判定：若几何增长率非正，时间趋于无穷
    if mu_geo <= 0:
        return np.inf 
    else:
        return np.log(M) / mu_geo

# ==========================================
# 2. 参数设定 (基准情景)
# ==========================================
g_nominal = 0.20      # 名义增长率 20%
target_multiple = 2.0 # 目标倍数：2倍
r_low = 0.018         # 低利率环境 1.8%
r_high = 0.040        # 常态利率环境 4.0%

# 波动率扫描区间：1% 到 70%
sigma_range = np.linspace(0.01, 0.70, 100)

# ==========================================
# 3. 计算过程
# ==========================================
# 心理时间 (不同利率环境)
n_low = [calc_psychological_time(r_low, s) for s in sigma_range]
n_high = [calc_psychological_time(r_high, s) for s in sigma_range]

# 物理时间 (与利率无关)
et_curve = [calc_physical_time(g_nominal, s, target_multiple) for s in sigma_range]

# ==========================================
# 4. 绘图输出
# ==========================================
plt.figure(figsize=(10, 6))

# 物理时间曲线
plt.plot(sigma_range, et_curve, 'r-', linewidth=2.5, label='Physical Time E[T]')

# 心理时间曲线
plt.plot(sigma_range, n_low, 'b--', linewidth=2, label=f'Psychological Time n (r={r_low:.1%})')
plt.plot(sigma_range, n_high, 'g:', linewidth=1.5, label=f'Psychological Time n (r={r_high:.1%})')

# 物理边界线
sigma_max = np.sqrt(2 * g_nominal)
plt.axvline(x=sigma_max, color='k', linestyle='-.', alpha=0.5)
plt.text(sigma_max + 0.01, 15, r'$\sigma_{max}=\sqrt{2g}$', rotation=90)

# 标注错配区域 (TPI > 0)
idx_cross = np.argwhere(np.diff(np.sign(np.array(n_low) - np.array(et_curve)))).flatten()
if len(idx_cross) > 0:
    cross_sigma = sigma_range[idx_cross]
    plt.fill_between(sigma_range, et_curve, n_low, 
                     where=(sigma_range > cross_sigma) & (sigma_range < sigma_max),
                     color='gray', alpha=0.3, label='Mispricing Zone (TPI > 0)')

plt.title('RATE Framework: Temporal Equilibrium Analysis')
plt.xlabel('Volatility ($\sigma$)')
plt.ylabel('Time (Years)')
plt.ylim(0, 30)
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()
