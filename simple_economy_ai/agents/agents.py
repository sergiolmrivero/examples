from EcoSimpy import DiscreteEventAgent

"""Economic Agent module for the Simple Economy model."""



class EconomicAgent(DiscreteEventAgent):
    """Basic Economic Agent

    This module implements the basic functions of an economic agent
    in the benchmark model. The ``EconomicAgent`` class implements the basic
    actions for the economic agents in the model.

    Example:
            To create an economic agent we must include the agent definition
            in the ``model.json`` file. The definition can be done as follows:

            "agents": [
                    {
                    "agent_type": "EconomicAgent",
                    "agent_prefix": "EA",
                    "agent_spaces": [
                        "Market"
                    ],
                    "no_of_agents": 500
                    }
                ],

    This will create 500 instances of the class EconomicAgent in the model and will
    include the agents in the ``space`` ``Market``.

    Economic agents are subclass of DiscreteEventAgent in the model kernel.


    Todo:
        * implement agent methods

    """

    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)

        # note: these variables need to go to some
        # bookeeping object (that will deal with them)


    def step(self):
        """Implemented by subclass"""

