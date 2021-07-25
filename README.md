# Parking Lot
## Problem Statement
I own a parking lot that can hold up to 'n' cars at any given point in time. Each slot is
given a number starting at 1 increasing with increasing distance from the entry point
in steps of one. I want to create an automated ticketing system that allows my
customers to use my parking lot without human intervention.  

When a car enters my parking lot, I want to have a ticket issued to the driver. The
ticket issuing process includes us documenting the registration number (number
plate) and the colour of the car and allocating an available parking slot to the car
before actually handing over a ticket to the driver (we assume that our customers are
nice enough to always park in the slots allocated to them). The customer should be
allocated a parking slot which is nearest to the entry. At the exit the customer returns
the ticket which then marks the slot they were using as being available.  

Due to government regulation, the system should provide me with the ability to find out:
  
● Registration numbers of all cars of a particular colour.  
● Slot number in which a car with a given registration number is parked.  
● Slot numbers of all slots where a car of a particular colour is parked.  

We interact with the system via a simple set of commands which produce a specific
output. The system should allow input in two ways.  

1) It should provide us with an interactive command prompt based shell where
commands can be typed in.
2) It should accept a filename as a parameter at the command prompt and read the
commands from that file  

To install run `bin/setup`  
It supports execution using file `bin/parking_lot file_input.txt`  
It also supports interactive execution `bin/parking_lot`  
Run tests `nosetests parking_lot/services/tests/parking_lot_service_test.py -v`  
End-to-End tests using file input `nosetests tests/parking_lot_file_input_test.py -v` 

## Further, plan of actions
Extend the Parking lot landscape according to:
1. Instead of flat parking lot, think n slot levels e.g. a matrix 3 * 4
2. Multi storey parking.(Multiple lanes in single floor)
3. Vehicle categories(bike-4 per slot,car-2 slot,bus/truck-1 slot)
4. Entrypoint are selected slots present in 4 corner slots
Assumptions: there is enough space to move vehicles between slots.

### Feasibility study
5. Introduce a chatbot which can recognise voice to text interpretation
6. Is it possible to go for an aggregator model for available  
peer to peer parking spaces?
7. Introduce dynamic pricing based on the timings e.g., the pricing model should also follow the OCP principle.
Start with segregation between weekday and weekend pricing