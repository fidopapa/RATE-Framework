# -*- coding: utf-8 -*-
"""
RATE_ZZ_robustness.py
======================================================================
Appendix B: ZZ‑CAPM Non‑linear Self‑consistent Solution & Robustness Check
Companion script for paper "Risk‑Anchored Temporal Equilibrium"
Author: RATE Research Group, 2026

This script reproduces:
  • Figure B‑1: Comparison of linear vs. non‑linear psychological anchor n(σ)
  • Table B‑1: Sensitivity of equilibrium volatility σ* to λ (0.2, 0.25, 0.3)

All parameters are set to match the main text:
  r = 1.8%, g = 20%, M = 2 (value doubling target)
The non‑linear ZZ‑CAPM is solved via robust bisection.
========================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import root_scalar

# ----------------------------------------------------------------------
# 1. 固定参数（与正文完全一致）
# ----------------------------------------------------------------------
R = 0.018          # 无风险利率 r = 1.8%
G = 0.20           # 名义增长率 g = 20%
M = 2.0            # 目标倍数（翻倍）
SIGMA_MIN = 0.10   # 波动率下限
SIGMA_MAX = 0.65   # 波动率上限（略高于物理熔断线）
N_POINTS = 300     # 采样点数（曲线平滑度）

# 待检验的线性近似系数（正文使用λ=0.2，附录展示敏感性）
LAMBDA_LIST = [0.20, 0.25, 0.30]

# ----------------------------------------------------------------------
# 2. 核心模型函数
# ----------------------------------------------------------------------
def physical_anchor(sigma, g=G, M=M):
    """
    物理锚 E[T]：几何布朗运动首次到达时间期望。
    当 g - 0.5σ² ≤ 0 时返回 NaN（物理熔断区）。
    """
    mu_geo = g - 0.5 * sigma**2
    et = np.full_like(sigma, np.nan, dtype=np.float64)
    mask = mu_geo > 0
    et[mask] = np.log(M) / mu_geo[mask]
    return et

def psychological_anchor_linear(sigma, lam, r=R):
    """
    线性近似心理锚 n = 1/(r + λσ)
    lam : 线性风险补偿系数（正文取0.2）
    """
    k = r + lam * sigma
    return 1.0 / k

def zz_risk_premium(sigma, n):
    """
    ZZ‑CAPM 精确风险补偿率 c(σ, n)
    公式：c = - (1/n) * ln[ 2 * (1 - N(σ√n / 4)) ]
    """
    if n <= 0:
        return np.inf
    x = sigma * np.sqrt(n) / 4.0
    cdf_val = norm.cdf(x)
    arg = 2.0 * (1.0 - cdf_val)
    if arg < 1e-12:
        return 1e12   # 近似无穷大
    return -np.log(arg) / n

def psychological_anchor_nonlinear(sigma, r=R, guess_lam=0.4):
    """
    非线性精确心理锚 n：自洽求解方程 n = 1 / [r + c(σ, n)]
    使用二分法，强制收敛，返回 n 或 NaN（求解失败）
    """
    n_guess = 1.0 / (r + guess_lam * sigma)
    bracket_low = max(0.1 * n_guess, 0.5)
    bracket_high = min(10.0 * n_guess, 50.0)
    
    def equation(n):
        if n <= 0:
            return 1e6
        c = zz_risk_premium(sigma, n)
        return n - 1.0 / (r + c)
    
    try:
        sol = root_scalar(equation,
                          bracket=[bracket_low, bracket_high],
                          method='bisect',
                          xtol=1e-6)
        return sol.root if sol.converged else np.nan
    except:
        return np.nan

# ----------------------------------------------------------------------
# 3. 计算数据（波动率网格）
# ----------------------------------------------------------------------
sigma_grid = np.linspace(SIGMA_MIN, SIGMA_MAX, N_POINTS)
E_T = physical_anchor(sigma_grid)

# 线性心理锚（多个λ）
n_lin_dict = {}
for lam in LAMBDA_LIST:
    n_lin_dict[lam] = psychological_anchor_linear(sigma_grid, lam)

# 非线性心理锚（只需求解一次，与λ无关）
n_nonlin = np.array([psychological_anchor_nonlinear(s) for s in sigma_grid])
valid_mask = ~np.isnan(n_nonlin)
sigma_valid = sigma_grid[valid_mask]
n_nonlin_valid = n_nonlin[valid_mask]

# 物理熔断线
sigma_meltdown = np.sqrt(2 * G)

# ----------------------------------------------------------------------
# 4. 辅助函数：寻找均衡波动率 σ*（n 与 E[T] 的交点）
# ----------------------------------------------------------------------
def find_intersection(x, y1, y2):
    """线性插值寻找两条曲线的第一个交点"""
    diff = y1 - y2
    sign_change = np.where(np.diff(np.sign(diff)))[0]
    if len(sign_change) == 0:
        return None
    idx = sign_change[0]
    x1, x2 = x[idx], x[idx+1]
    y1_1, y1_2 = diff[idx], diff[idx+1]
    return x1 - y1_1 * (x2 - x1) / (y1_2 - y1_1)

# 非线性精确解的 σ*（固定值）
sigma_star_nonlin = find_intersection(sigma_valid, n_nonlin_valid, E_T[valid_mask])

# 各线性近似的 σ*
sigma_star_lin_dict = {}
for lam in LAMBDA_LIST:
    sigma_star_lin_dict[lam] = find_intersection(sigma_grid, n_lin_dict[lam], E_T)

# ----------------------------------------------------------------------
# 5. 输出表 B-1：参数敏感性分析
# ----------------------------------------------------------------------
print("\n" + "="*60)
print("表 B-1  不同线性近似系数下的均衡波动率与偏差")
print("="*60)
print(f"{'λ':<8} {'线性 σ*':<12} {'非线性 σ*':<14} {'偏差 Δσ*':<10}")
print("-"*60)
for lam in LAMBDA_LIST:
    lin_star = sigma_star_lin_dict[lam]
    nonlin_star = sigma_star_nonlin
    if lin_star is not None and nonlin_star is not None:
        diff = lin_star - nonlin_star
        print(f"{lam:<6.2f}  {lin_star:>7.1%}      {nonlin_star:>7.1%}        {diff:>+6.1%}")
print("="*60 + "\n")

# ----------------------------------------------------------------------
# 6. 绘制图 B-1：线性 vs 非线性心理锚（出版级矢量图）
# ----------------------------------------------------------------------
plt.style.use('default')
fig, ax = plt.subplots(figsize=(9, 6))

# ----- 物理锚（红色实线）-----
ax.plot(sigma_grid, E_T, 'r-', linewidth=2.5, label='Physical Anchor $E[T]$ (Rigid)')

# ----- 非线性精确心理锚（绿色实线）-----
ax.plot(sigma_valid, n_nonlin_valid, 'g-', linewidth=2.2, alpha=0.9,
        label='Exact $n$ (ZZ‑CAPM, non‑linear)')

# ----- 线性近似心理锚（不同λ，虚线）-----
colors = ['b', 'orange', 'purple']
for i, lam in enumerate(LAMBDA_LIST):
    ax.plot(sigma_grid, n_lin_dict[lam], linestyle='--', linewidth=1.8,
            color=colors[i], label=f'Linear $n$ ($\\lambda={lam:.2f}$)')

# ----- 物理熔断线（黑色点划线）-----
ax.axvline(x=sigma_meltdown, color='k', linestyle='-.', linewidth=1.2, alpha=0.7)
meltdown_val = sigma_meltdown * 100
ax.text(sigma_meltdown + 0.005, 2,
        rf'Physical Meltdown $\sigma_{{\max}} = \sqrt{{2g}} = {meltdown_val:.1f}\%$',
        fontsize=9, verticalalignment='bottom', rotation=90)

# ----- 标注均衡交点 -----
# 非线性精确交点（绿色圆点）
if sigma_star_nonlin is not None:
    y_star_nonlin = physical_anchor(np.array([sigma_star_nonlin]))
    ax.plot(sigma_star_nonlin, y_star_nonlin, 'go', markersize=8, zorder=5)
    ax.axvline(sigma_star_nonlin, ymin=0, ymax=0.3, color='g', linestyle=':', alpha=0.5)
    ax.text(sigma_star_nonlin - 0.08, y_star_nonlin - 2.5,
            rf'Exact $\sigma^*\approx{sigma_star_nonlin*100:.1f}\%$',
            color='g', fontsize=9, fontweight='bold')

# 线性交点（分别标注）
for i, lam in enumerate(LAMBDA_LIST):
    s_star = sigma_star_lin_dict[lam]
    if s_star is not None:
        y_star = physical_anchor(np.array([s_star]))
        ax.plot(s_star, y_star, 'o', color=colors[i], markersize=7, zorder=4)
        ax.axvline(s_star, ymin=0, ymax=0.25, color=colors[i], linestyle=':', alpha=0.4)
        ax.text(s_star + 0.005, y_star + 1.5,
                rf'$\lambda={lam:.2f}$ $\sigma^*\approx{s_star*100:.1f}\%$',
                color=colors[i], fontsize=8)

# 箭头指示“实际风险边界更紧”
if sigma_star_nonlin is not None and sigma_star_lin_dict[0.20] is not None:
    x_mid = (sigma_star_lin_dict[0.20] + sigma_star_nonlin) / 2
    y_mid = (physical_anchor(np.array([sigma_star_lin_dict[0.20]]))[0] +
             physical_anchor(np.array([sigma_star_nonlin]))[0]) / 2 - 4
    ax.annotate('', xy=(sigma_star_nonlin, y_star_nonlin),
                xytext=(sigma_star_lin_dict[0.20], y_star_nonlin - 2),
                arrowprops=dict(arrowstyle='->', color='dimgray', lw=1.8, alpha=0.8))
    ax.text(x_mid, y_mid, 'Actual risk boundary\nis tighter',
            ha='center', fontsize=9, style='italic', color='dimgray')

# ----- 坐标轴、图例、网格 -----
ax.set_xlabel('Total Volatility ($\\sigma$)', fontsize=12)
ax.set_ylabel('Time Horizon (Years)', fontsize=12)
ax.set_title('Figure B‑1: Linear Approximation vs. Non‑linear ZZ‑CAPM', fontsize=14, fontweight='bold')
ax.set_xlim(SIGMA_MIN, SIGMA_MAX)
ax.set_ylim(0, 25)
ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
# 保存为出版级矢量图（PDF）
plt.savefig('RATE_ZZ_robustness.pdf', dpi=300, bbox_inches='tight')
plt.show()

print("图 B‑1 已保存为 RATE_ZZ_robustness.pdf")
print("附录B全部数据与图表复现完成。")
