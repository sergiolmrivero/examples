# -*- coding: utf-8 -*-
"""Government agent for the Simple Economy model."""

from EcoSimpy import DiscreteEventAgent
from .household import Household
from .firm import Firm


class Government(DiscreteEventAgent):
    """Government agent in the Simple Economy model.

    The Government is a single public-sector agent that:

    * Collects income taxes from households and profit taxes from firms.
    * Pays unemployment benefits to jobless households.
    * Computes macroeconomic aggregates: GDP, unemployment rate, and price level.
    * Records the government budget balance.

    Agent definition example (``model.json``)::

        {
            "agent_type": "Government",
            "agent_prefix": "Gov",
            "agent_spaces": [],
            "no_of_agents": 1,
            "has_observer": true
        }
    """

    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)

        # # Policy parameters
        # self.unemployment_benefit = 2.0
        # self.income_tax_rate = 0.15
        # self.profit_tax_rate = 0.20

        # # Government accounts
        # self.tax_revenue = 0.0
        # self.expenditure = 0.0
        # self.budget_surplus = 0.0

        # # Macroeconomic aggregates
        # self.gdp = 0.0
        # self.unemployment_rate = 0.0
        # self.price_level = 0.0
        # self.total_employment = 0
        # self.total_labor_force = 0

        # # Time series for analysis
        # self.gdp_history = []
        # self.unemployment_history = []
        # self.price_level_history = []

    # ------------------------------------------------------------------
    # step
    # ------------------------------------------------------------------

    def step(self):
        """Execute one time step for the National Accounting Office.

        Sequence of actions:
            1. :meth:`collect_taxes`
            2. :meth:`pay_unemployment_benefits`
            3. :meth:`compute_gdp`
            4. :meth:`compute_unemployment_rate`
            5. :meth:`compute_price_level`
            6. :meth:`balance_budget`
            7. :meth:`record_history`
        """
        self.collect_taxes()
        self.pay_unemployment_benefits()
        self.compute_gdp()
        self.compute_unemployment_rate()
        self.compute_price_level()
        self.balance_budget()
        self.record_history()

    # ------------------------------------------------------------------
    # Action methods
    # ------------------------------------------------------------------

    def collect_taxes(self):
        """Collect income tax from households and profit tax from firms.

        Tax amounts are computed here and subtracted from agent income/profit
        via the agents' own :meth:`pay_taxes` methods; this method tallies
        the government receipts.
        """
        self.tax_revenue = 0.0
        for agent in self.model.agents.values():
            if isinstance(agent, Household):
                self.tax_revenue += agent.taxes_paid
            elif isinstance(agent, Firm):
                self.tax_revenue += agent.taxes_paid

    def pay_unemployment_benefits(self):
        """Transfer unemployment benefits to all jobless household agents."""
        self.expenditure = 0.0
        for agent in self.model.agents.values():
            if isinstance(agent, Household) and not agent.employed:
                agent.receive_unemployment_benefit(self.unemployment_benefit)
                self.expenditure += self.unemployment_benefit

    def compute_gdp(self):
        """Compute GDP as the sum of revenues across all firms."""
        self.gdp = sum(
            agent.revenue
            for agent in self.model.agents.values()
            if isinstance(agent, Firm)
        )

    def compute_unemployment_rate(self):
        """Compute the share of unemployed workers in the labour force."""
        employed = 0
        total = 0
        for agent in self.model.agents.values():
            if isinstance(agent, Household):
                total += 1
                if agent.employed:
                    employed += 1
        self.total_employment = employed
        self.total_labor_force = total
        self.unemployment_rate = (
            (total - employed) / total if total > 0 else 0.0
        )

    def compute_price_level(self):
        """Compute the average output price across all active firms."""
        prices = [
            agent.price
            for agent in self.model.agents.values()
            if isinstance(agent, Firm) and agent.price > 0
        ]
        self.price_level = sum(prices) / len(prices) if prices else 0.0

    def balance_budget(self):
        """Record the government fiscal surplus (or deficit)."""
        self.budget_surplus = self.tax_revenue - self.expenditure

    def record_history(self):
        """Append current macroeconomic aggregates to the time-series lists."""
        self.gdp_history.append(self.gdp)
        self.unemployment_history.append(self.unemployment_rate)
        self.price_level_history.append(self.price_level)
