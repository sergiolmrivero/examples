# -*- coding: utf-8 -*-
"""Firm agent for the Simple Economy model."""

from EcoSimpy import DiscreteEventAgent
import random

from agents.agents import EconomicAgent


class CGFirm(EconomicAgent):
    """Firm agent in the Simple Economy model.

    Firms hire labour, produce consumer goods with a fixed labour
    productivity, set prices via a mark-up rule, sell output in the
    goods market, pay wages and profit taxes, and distribute dividends.

    Agent definition example (``model.json``)::

        {
            "agent_type": "CGFirm",
            "agent_prefix": "CG",
            "agent_spaces": ["Labor_Market", "CG_Market"],
            "no_of_agents": 100,
            "has_observer": true
        }
    """

    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)

        self.goods_market_name = "Goods_Market"
        self.labor_market_name = "Labor_Market"

        # # Production
        # self.labor_productivity = random.uniform(1.0, 3.0)
        # self.workers = []
        # self.labor_demand = 0
        # self.output = 0.0
        # self.inventory = random.uniform(10.0, 50.0)

        # # Pricing
        # self.markup = random.uniform(0.1, 0.3)
        # self.unit_cost = 1.0
        # self.price = 1.0

        # # Finance
        # self.wage_bill = 0.0
        # self.revenue = 0.0
        # self.profit = 0.0
        # self.profit_tax_rate = 0.20
        # self.taxes_paid = 0.0
        # self.dividend_payout_ratio = 0.6

        # # Adaptive sales expectations
        # self.expected_sales = random.uniform(50.0, 100.0)
        # self.actual_sales_prev = self.expected_sales
        # self.expectation_lambda = 0.25

        self.first_step = True

    # ------------------------------------------------------------------
    # step
    # ------------------------------------------------------------------

    def step(self):
        """Execute one time step for the Firm.

        Sequence of actions:
            1. :meth:`create_expectations`
            2. :meth:`plan_production`
            3. :meth:`hire_labor`
            4. :meth:`produce`
            5. :meth:`set_price`
            6. :meth:`offer_goods`
            7. :meth:`pay_wages`
            8. :meth:`compute_profit`
            9. :meth:`pay_taxes`
           10. :meth:`distribute_dividends`
        """
        if self.first_step:
            self.first_step = False

        self.create_expectations()
        self.plan_production()
        self.hire_labor()
        self.produce()
        self.set_price()
        self.offer_goods()
        self.pay_wages()
        self.compute_profit()
        self.pay_taxes()
        self.distribute_dividends()

    # ------------------------------------------------------------------
    # Action methods
    # ------------------------------------------------------------------

    def create_expectations(self):
        """Form adaptive expectations about next-period sales.

        Follows the standard adaptive expectation rule from the benchmark
        model: :math:`S^e_t = S^e_{t-1} + \\lambda (S_{t-1} - S^e_{t-1})`.
        """
        self.expected_sales = (
            self.expected_sales
            + self.expectation_lambda * (self.actual_sales_prev - self.expected_sales)
        )

    def plan_production(self):
        """Compute desired output and the implied labour demand.

        The firm targets expected sales plus a buffer inventory of 10 % of
        expected sales, net of current inventory.
        """
        desired_inventory_ratio = 0.10
        desired_output = (
            self.expected_sales * (1.0 + desired_inventory_ratio) - self.inventory
        )
        desired_output = max(desired_output, 0.0)
        self.labor_demand = int(desired_output / self.labor_productivity) + 1

    def hire_labor(self):
        """Post a labour demand in the labour market."""
        try:
            labor_market = self.get_a_space(self.labor_market_name)
            labor_market.set_demand(self, self.labor_demand)
        except KeyError:
            pass

    def produce(self):
        """Produce output proportional to the number of hired workers."""
        actual_labor = len(self.workers)
        self.output = actual_labor * self.labor_productivity
        self.inventory += self.output

    def set_price(self):
        """Set output price using a mark-up over average unit labour cost."""
        if self.workers:
            self.wage_bill = sum(w.reservation_wage for w in self.workers)
            if self.output > 0:
                self.unit_cost = self.wage_bill / self.output
        self.price = (1.0 + self.markup) * self.unit_cost

    def offer_goods(self):
        """List available inventory for sale in the goods market."""
        if self.inventory > 0:
            try:
                goods_market = self.get_a_space(self.goods_market_name)
                goods_market.set_offer(self, self.price, self.inventory)
            except KeyError:
                pass

    def pay_wages(self):
        """Transfer wages to each hired worker at their reservation wage."""
        for worker in self.workers:
            worker.receive_wage(worker.reservation_wage)

    def compute_profit(self):
        """Calculate gross profit as revenue minus wage bill."""
        self.profit = max(self.revenue - self.wage_bill, 0.0)

    def pay_taxes(self):
        """Deduct profit tax and record the amount paid."""
        self.taxes_paid = self.profit * self.profit_tax_rate
        self.profit -= self.taxes_paid

    def distribute_dividends(self):
        """Distribute a fixed fraction of after-tax profit to workers as dividends."""
        if self.profit > 0 and self.workers:
            total_dividends = self.profit * self.dividend_payout_ratio
            dividend_per_worker = total_dividends / len(self.workers)
            for worker in self.workers:
                worker.receive_dividends(dividend_per_worker)

    # ------------------------------------------------------------------
    # Notification methods (called by the market or other agents)
    # ------------------------------------------------------------------

    def hire_worker(self, worker):
        """Register a newly matched worker as an employee."""
        self.workers.append(worker)
        worker.employed = True

    def record_sale(self, quantity, price):
        """Update revenue and inventory after a market transaction."""
        self.revenue += quantity * price
        self.inventory = max(self.inventory - quantity, 0.0)
        self.actual_sales_prev = quantity
