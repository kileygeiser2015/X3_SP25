from Air import *
from matplotlib import pyplot as plt
import numpy as np

class ottoCycleModel():
    def __init__(self, p_initial=1000.0, v_cylinder=1.0, t_initial=298, t_high=1500.0, ratio=6.0, name='Air Standard Otto Cycle'):
        self.units = units()
        self.air = air()
        self.p_initial = p_initial
        self.T_initial = t_initial
        self.T_high = t_high
        self.Ratio = ratio
        self.V_Cylinder = v_cylinder

        self.State1 = self.air.set(P=self.p_initial, T=self.T_initial)
        self.air.n = self.V_Cylinder / self.State1.v
        self.air.m = self.air.n * self.air.MW

        self.State2 = self.air.set(v=self.State1.v / self.Ratio, s=self.State1.s)
        self.State3 = self.air.set(T=self.T_high, v=self.State2.v)
        self.State4 = self.air.set(v=self.State1.v, s=self.State3.s)

        self.W_Compression = self.air.n * (self.State2.u - self.State1.u)
        self.W_Power = self.air.n * (self.State3.u - self.State4.u)
        self.Q_In = self.air.n * (self.State3.u - self.State2.u)
        self.Q_Out = self.air.n * (self.State4.u - self.State1.u)
        self.W_Cycle = self.W_Power - self.W_Compression
        self.Eff = 100.0 * self.W_Cycle / self.Q_In

        self.upperCurve = StateDataForPlotting()
        self.lowerCurve = StateDataForPlotting()

    def getSI(self):
        return self.units.SI


class dieselCycleModel():
    def __init__(self, p_initial=1000.0, v_cylinder=1.0, t_initial=298.0, t_high=1500.0, ratio=18.0, r_cutoff=2.0,
                 name='Air Standard Diesel Cycle'):
        self.units = units()
        self.air = air()
        self.p_initial = p_initial
        self.T_initial = t_initial
        self.T_high = t_high
        self.Ratio = ratio
        self.r_cutoff = r_cutoff
        self.V_Cylinder = v_cylinder

        self.State1 = self.air.set(P=self.p_initial, T=self.T_initial)
        self.air.n = self.V_Cylinder / self.State1.v
        self.air.m = self.air.n * self.air.MW

        self.State2 = self.air.set(v=self.State1.v / self.Ratio, s=self.State1.s)
        self.State3 = self.air.set(P=self.State2.P, v=self.State2.v * self.r_cutoff)
        self.State4 = self.air.set(v=self.State1.v, s=self.State3.s)

        self.W_Compression = self.air.n * (self.State2.u - self.State1.u)
        self.W_Power = self.air.n * (self.State3.u - self.State4.u)
        self.Q_In = self.air.n * (self.State3.u - self.State2.u)
        self.Q_Out = self.air.n * (self.State4.u - self.State1.u)
        self.W_Cycle = self.W_Power - self.W_Compression
        self.Eff = 100.0 * self.W_Cycle / self.Q_In

        self.upperCurve = StateDataForPlotting()
        self.lowerCurve = StateDataForPlotting()

    def getSI(self):
        return self.units.SI


class ottoCycleView():
    def __init__(self):
        # You already have this class implemented in your current file. No changes required.
        pass


class CycleController():
    def __init__(self, model=None, ax=None):
        self.model = model if model else ottoCycleModel()
        self.view = ottoCycleView()
        self.view.ax = ax

    def calc(self):
        T0 = float(self.view.le_TLow.text())
        P0 = float(self.view.le_P0.text())
        V0 = float(self.view.le_V0.text())
        TH = float(self.view.le_THigh.text())
        CR = float(self.view.le_CR.text())
        metric = self.view.rdo_Metric.isChecked()

        if self.view.radio_otto.isChecked():
            self.model = ottoCycleModel(P0, V0, T0, TH, CR)
        elif self.view.radio_diesel.isChecked():
            self.model = dieselCycleModel(P0, V0, T0, TH, CR, r_cutoff=2.0)

        self.set(T_0=T0, P_0=P0, V_0=V0, T_High=TH, ratio=CR, SI=metric)

    def set(self, T_0=25.0, P_0=100.0, V_0=1.0, T_High=1500.0, ratio=6.0, SI=True):
        self.model.units.set(SI=SI)
        self.model.T_initial = T_0 if SI else T_0 / self.model.units.CF_T
        self.model.p_initial = P_0 if SI else P_0 / self.model.units.CF_P
        self.model.T_high = T_High if SI else T_High / self.model.units.CF_T
        self.model.V_Cylinder = V_0 if SI else V_0 / self.model.units.CF_V
        self.model.Ratio = ratio

        self.model.State1 = self.model.air.set(P=self.model.p_initial, T=self.model.T_initial)
        self.model.State2 = self.model.air.set(v=self.model.State1.v / self.model.Ratio, s=self.model.State1.s)
        self.model.State3 = self.model.air.set(T=self.model.T_high, v=self.model.State2.v)
        self.model.State4 = self.model.air.set(v=self.model.State1.v, s=self.model.State3.s)

        self.model.air.n = self.model.V_Cylinder / self.model.air.State.v
        self.model.air.m = self.model.air.n * self.model.air.MW

        self.model.W_Compression = self.model.State2.u - self.model.State1.u
        self.model.W_Power = self.model.State3.u - self.model.State4.u
        self.model.Q_In = self.model.State3.u - self.model.State2.u
        self.model.Q_Out = self.model.State4.u - self.model.State1.u

        self.model.W_Cycle = self.model.W_Power - self.model.W_Compression
        self.model.Eff = 100.0 * self.model.W_Cycle / self.model.Q_In

        self.buildDataForPlotting()
        self.updateView()

    def buildDataForPlotting(self):
        self.model.upperCurve.clear()
        self.model.lowerCurve.clear()
        a = air()

        DeltaT = np.linspace(self.model.State2.T, self.model.State3.T, 30)
        for T in DeltaT:
            state = a.set(T=T, v=self.model.State2.v)
            self.model.upperCurve.add((state.T, state.P, state.u, state.h, state.s, state.v))

        DeltaV = np.linspace(self.model.State3.v, self.model.State4.v, 30)
        for v in DeltaV:
            state = a.set(v=v, s=self.model.State3.s)
            self.model.upperCurve.add((state.T, state.P, state.u, state.h, state.s, state.v))

        DeltaT = np.linspace(self.model.State4.T, self.model.State1.T, 30)
        for T in DeltaT:
            state = a.set(T=T, v=self.model.State4.v)
            self.model.upperCurve.add((state.T, state.P, state.u, state.h, state.s, state.v))

        DeltaV = np.linspace(self.model.State1.v, self.model.State2.v, 30)
        for v in DeltaV:
            state = a.set(v=v, s=self.model.State1.s)
            self.model.lowerCurve.add((state.T, state.P, state.u, state.h, state.s, state.v))

    def updateView(self):
        self.view.updateView(cycle=self.model)

    def setWidgets(self, w=None):
        [self.view.lbl_THigh, self.view.lbl_TLow, self.view.lbl_P0, self.view.lbl_V0, self.view.lbl_CR,
         self.view.le_THigh, self.view.le_TLow, self.view.le_P0, self.view.le_V0, self.view.le_CR,
         self.view.le_T1, self.view.le_T2, self.view.le_T3, self.view.le_T4,
         self.view.lbl_T1Units, self.view.lbl_T2Units, self.view.lbl_T3Units, self.view.lbl_T4Units,
         self.view.le_PowerStroke, self.view.le_CompressionStroke, self.view.le_HeatAdded, self.view.le_Efficiency,
         self.view.lbl_PowerStrokeUnits, self.view.lbl_CompressionStrokeUnits, self.view.lbl_HeatInUnits,
         self.view.rdo_Metric, self.view.cmb_Abcissa, self.view.cmb_Ordinate,
         self.view.chk_LogAbcissa, self.view.chk_LogOrdinate, self.view.ax, self.view.canvas] = w

    def plot_cycle_XY(self, X='s', Y='T', logx=False, logy=False, mass=False, total=False):
        self.view.plot_cycle_XY(self.model, X=X, Y=Y, logx=logx, logy=logy, mass=mass, total=total)

    def print_summary(self):
        self.view.print_summary(self.model)

    def get_summary(self):
        return self.view.get_summary(self.model)



