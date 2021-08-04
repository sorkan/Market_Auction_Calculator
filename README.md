# Market_Auction_Calculator

Setup
  1. setup virtual environment
     1. pip3 install virtualenv
     2. virtualenv Market_Auction_calculator
     3. pip3 install -r requirements.txt
     
  
Two ways to run the file once you place the json file in the current path
1. python market_auction_challenge.py <enter>
   runs in interactive mode.  Type 'quit' to exit
  
2. python market_auction_challenge.py id,year <enter>
   calculates for the id if it is present in the file.  if the year is not present, calculates the market and auction value based on default ratios for market and auction.
  
 Test cases:
  run pytest
  
Running in Non-interactive mode
$> python market_auction_challenge.py 67352,2007


--------------------------------------------------
Identifier: 67352
Category: Earthmoving Equipment
Sub-cat: Dozers
Make: Caterpillar		Model: D8T

Schedule year: 2007
Market Value: $ 216,384.71
Auction Value: $ 126,089.53
--------------------------------------------------

  
$> python market_auction_challenge.py 87964,2011
ID: 87964 not found in source data feed!!
