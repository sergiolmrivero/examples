# -*- coding: utf-8 -*-
""" Basic Market Class implementation 

This module implements the generic macthing process 
in an economic market.

Example:


Todo: 
"""

from EcoSimpy import Space
import random

class Market(Space):
    """ Abstract Market """
    def __init__(self, model, name, variables):
        """ Intialize abstract market """
        super().__init__(model, name, variables)
        self.offers = {}
        self.demand = {}
        self.accepted_offers = {}

    def update(self):
        """ """
        self.matching()


    def matching(self):

        self.market_not_empty = True

        while self.has_demand():
            self.a_demand = self.get_demand()
            self.this_remaining_demand = self.a_demand.c_quantity
            self.buyer = self.a_demand.c_owner
            self.have_unmet_demand = True

            while self.have_unmet_demand:
                if self.has_offers():
                    self.an_offer = self.get_offer()
                    self.seller = self.an_offer.c_producer
                    if self.an_offer.c_quantity <= self.this_remaining_demand:
                        self.this_remaining_demand -= self.an_offer.c_quantity
                        self.seller.offer_accepted(self, self.buyer)
                        self.accepted_offers[self.seller.name] = self.an_offer
                        self.offers.pop(self.seller.name)
                    else:
                        self.partial_offer = self.set_partial_offer(self.an_offer)
                        self.partial_offer.c_quantity = self.this_remaining_demand
                        self.an_offer.c_quantity -= self.this_remaining_demand
                        self.this_remaining_demand = 0.0
                        self.have_unmet_demand = False
                        self.seller.offer_partially_accepted(self, self.buyer, self.partial_offer)
                        self.accepted_offers[self.seller.name] = self.partial_offer
                    if self.this_remaining_demand == 0:
                        self.have_unmet_demand = False
                        self.release_offers()
                        self.buyer.demand_is_met()
                        self.buyer.get_accepted_offers(self.accepted_offers)

                else:
                    self.market_has_no_offers()
                    self.have_unmet_demand = False
                    self.buyer.get_accepted_offers(self.accepted_offers)



    def set_demand(self, an_owner, a_good):
        """
        Set the demand for a good.

        Parameters:
        - an_owner: The owner of the demand.
        - a_good: The good for which the demand is being set.
        """
        self.demand[an_owner.name] = a_good

    def set_offer(self, an_owner, a_good):
        """
        Set the offer for a good.

        Parameters:
        - an_owner (str): The owner of the offer.
        - a_good (str): The good being offered.

        Returns:
        None
        """
        self.offers[an_owner.name] = a_good


    def get_demand(self):
         """ Implements the maching in market """
         if(self.market_type == "random"):
             a_demand = self.random_demand_matching()
         elif(self.market_type == "hop"):
             a_demand = self.hop_demand_matching()
         elif(self.market_type == "lop"):
             a_demand = self.lop_demand_matching()
         elif(self.market_type == "bhop"):
             a_demand = self.bhop_demand_matching()
         elif(self.market_type == "blop"):
             a_demand = self.blop_demand_matching()
         else:
             # Add error treatment here
             raise ValueError("Invalid market matching type")
         return a_demand
    
    def get_offer(self):
         """ Implements the maching in market """
         if(self.market_type == "random"):
             an_offer = self.random_offer_matching()
         elif(self.market_type == "hop"):
             an_offer = self.hop_offer_matching()
         elif(self.market_type == "lop"):
             an_offer = self.lop_offer_matching()
         elif(self.market_type == "bhop"):
             an_offer = self.bhop_offer_matching()
         elif(self.market_type == "blop"):
             an_offer = self.blop__offer_matching()
         else:
             # Add error treatment here
             raise ValueError("Invalid market matching type")
         return an_offer

    def random_demand_matching(self):
        """ Randomly pop a demand from the demand dictionary and return it """
        if not self.demand:
            raise ValueError("No demand available in market ", self.name)
        else:   
            a_demand = self.demand.popitem()[1]
            return a_demand

    def hop_demand_matching(self):
        pass

    def lop_demand_matching(self):
        pass

    def bhop_demand_matching(self):
        pass

    def blop_demand_matching(self):
        pass

    def hop_offer_matching(self):
        pass

    def lop_offer_matching(self):
        pass

    def bhop_offer_matching(self):
        pass

    def blop_offer_matching(self):
        pass


    def market_has_no_offers(self):
        self.demand = {}
        
    def has_offers(self):
        """ A market answers if is has offers (True or False) """
        if not self.offers:
            return False
        else:
            return True

    def has_demand(self):
        """ A market answers if is has demand (True or False) """
        if not self.demand:
            return False
        else:
            return True

    def no_of_offers(self):
        """ A market answers the number of offers it has """
        return self.offers.__len__()
        
    def random_offer_matching(self):
        """ Randomly get an item from self.offers dict without excluding it from dict """
        if not self.offers:
            raise ValueError("No offers available in market ", self.name)
        else:
            offer = random.choice(list(self.offers.values()))
            return offer

    def release_demand(self):
        """Inform the bider that their demand was not satisfied
        """
        for demand in self.demand.values():
            demand.c_owner.release_demand()
            self.demand = {}

    def release_offers(self):
        """Inform the producers/household that their offer was not bought
        """
        self.offers = {}

    def set_partial_offer(self, an_offer):
        partial_offer = type(an_offer)()
        partial_offer = an_offer.copy_attributes(partial_offer)
        return partial_offer
  
   

class CGMarket(Market):
    """Consumers Goods Market

    Args:
        Market (_type_): _description_
    """
    def __init__(self, model, name, variables):
        super().__init__(model, name, variables)


class LaborMarket(Market):
    """Labor Market

    Args:
        Market (_type_): _description_
    """

    def __init__(self, model, name, variables):
        super().__init__(model, name, variables)

        