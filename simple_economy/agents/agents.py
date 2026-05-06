from EcoSimpy import DiscreteEventAgent
import random as rnd 


"""Economic Agent module for the Simple Economy model."""



class Household(DiscreteEventAgent):
    """Household agent in the Simple Economy model.
    """

    def __init__(self, simulation, scenario, agent_number, agent_def):
        super().__init__(simulation, scenario, agent_number, agent_def)
        self.active_scenario = scenario

    # ------------------------------------------------------------------
    # step
    # ------------------------------------------------------------------

    def step(self):
        """Execute one time step for the Household."""

        self.update_reservation_wage()
    
       
    # ------------------------------------------------------------------
    # Action methods
    # ------------------------------------------------------------------


    def update_reservation_wage(self):
        """Lower the reservation wage with each additional period of unemployment.

        The wage floor declines by 1 % per unemployment period down to a
        minimum of 1.0, following the adaptive mechanism used in the
        benchmark model.
        ....
        """    
        self.gdp_value = self.active_scenario.get_scenario_variable("gdp")
        self.reservation_wage *= (1.0 - 0.01 * rnd.uniform(0, 1))
        self.reservation_wage = max(self.reservation_wage, 1.0)