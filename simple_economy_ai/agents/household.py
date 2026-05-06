# -*- coding: utf-8 -*-
"""Household agent for the Simple Economy model."""

from EcoSimpy import DiscreteEventAgent
import random

from agents.agents import EconomicAgent


class Household(EconomicAgent):
    """Household agent in the Simple Economy model.

    Households offer labour in the labour market, demand consumption goods
    in the goods market, earn wages and dividends, and pay income tax.

    Agent definition example (``model.json``)::

        {
            "agent_type": "Household",
            "agent_prefix": "HH",
            "agent_spaces": ["Labor_Market", "CG_Market"],
            "no_of_agents": 100,
            "has_observer": true
        }
    """

    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)

        self.cg_market_name = "CG_Market"
        self.labor_market_name = "Labor_Market"

        # # Labour
        # self.employed = False
        # self.unemployment_duration = 0
        # self.reservation_wage = random.uniform(5.0, 15.0)

        # # Income and wealth
        # self.wage = 0.0
        # self.dividends = 0.0
        # self.income = 0.0
        # self.savings = random.uniform(10.0, 100.0)

        # # Consumption
        # self.marginal_propensity_to_consume = 0.8
        # self.consumption_budget = 0.0

        # # Taxation
        # self.income_tax_rate = 0.15
        # self.taxes_paid = 0.0

        self.first_step = True

    # ------------------------------------------------------------------
    # step
    # ------------------------------------------------------------------

    def step(self):
        """Execute one time step for the Household.

        Sequence of actions:
            1. :meth:`update_employment_status`
            2. :meth:`update_reservation_wage`
            3. :meth:`offer_labor`
            4. :meth:`calculate_income`
            5. :meth:`plan_consumption`
            6. :meth:`consume`
            7. :meth:`pay_taxes`
            8. :meth:`update_savings`
        """
        if self.first_step:
            self.first_step = False

        self.update_employment_status()
        self.update_reservation_wage()
        self.offer_labor()
        self.calculate_income()
        self.plan_consumption()
        self.consume()
        self.pay_taxes()
        self.update_savings()

    # ------------------------------------------------------------------
    # Action methods
    # ------------------------------------------------------------------

    def update_employment_status(self):
        """Track unemployment duration.

        Increments the unemployment counter when the agent has no job;
        resets it to zero when employed.
        """
        if not self.employed:
            self.unemployment_duration += 1
        else:
            self.unemployment_duration = 0

    def update_reservation_wage(self):
        """Lower the reservation wage with each additional period of unemployment.

        The wage floor declines by 1 % per unemployment period down to a
        minimum of 1.0, following the adaptive mechanism used in the
        benchmark model.
        """
        if not self.employed and self.unemployment_duration > 0:
            self.reservation_wage *= (1.0 - 0.01 * self.unemployment_duration)
            self.reservation_wage = max(self.reservation_wage, 1.0)

    def offer_labor(self):
        """Post a labour offer in the labour market when unemployed."""
        if not self.employed:
            try:
                labor_market = self.get_a_space(self.labor_market_name)
                labor_market.set_offer(self, self.reservation_wage)
            except KeyError:
                pass

    def calculate_income(self):
        """Compute total income as wages plus dividends.

        Unemployed workers also receive a transfer from the
        :class:`National_Accounting_Office`.
        """
        self.income = self.wage + self.dividends

    def plan_consumption(self):
        """Determine the consumption budget.

        Uses a Keynesian rule: a fixed fraction of income is consumed plus
        a wealth component drawn from accumulated savings.
        """
        self.consumption_budget = (
            self.marginal_propensity_to_consume * self.income
            + 0.05 * self.savings
        )
        self.consumption_budget = max(self.consumption_budget, 0.0)

    def consume(self):
        """Submit a demand for consumption goods to the goods market."""
        if self.consumption_budget > 0:
            try:
                cg_market = self.get_a_space(self.cg_market_name)
                cg_market.set_demand(self, self.consumption_budget)
            except KeyError:
                pass

    def pay_taxes(self):
        """Deduct income tax from current-period income."""
        self.taxes_paid = self.income * self.income_tax_rate
        self.income -= self.taxes_paid

    def update_savings(self):
        """Accumulate or deplete savings from the income–consumption gap."""
        residual = self.income - self.consumption_budget
        self.savings = max(self.savings + residual, 0.0)

    # ------------------------------------------------------------------
    # Notification methods (called by other agents)
    # ------------------------------------------------------------------

    def receive_wage(self, amount):
        """Register a wage payment and mark the agent as employed."""
        self.wage = amount
        self.employed = True

    def receive_dividends(self, amount):
        """Accumulate dividend income."""
        self.dividends += amount

    def receive_unemployment_benefit(self, amount):
        """Add an unemployment transfer to current income."""
        self.income += amount
