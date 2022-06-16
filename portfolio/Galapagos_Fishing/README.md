# Chinese Fishing Vessel Tracking

*Sadly due to the cost of the satelite data this will be just a proof of concept using sample data.*

Due to the rich marine life in the Galapagos Marine Reserve, the limits of its reserve are swarmed by fishing ships, where more than 300 of these ships are chinese.
From my dad's experience when sailing from the Galapagos Islands to Tahiti, these conglomerate of fishing ships are so bug that from the distance their lights make it look as there is a city in the middle of the ocean, as there are not just fishing ships, but tanker ships to refuel and fish processing ships, where fishing ships transfer their catch to them so they can stay longer.

It has also been seen that some ships even turn their tracking systems of to go closer or even into the marine reserve without being spotted.  As we can see this is a great threat to the marine life of the islands at the magnitude these ships fish.

The idea of this project is to create a simple model to try and track fishing ships that turn of their tracking systems.
The model is simple, fishing ships data will be collected from an area surrounding the marine reserve.  This data includes Vessel ID, Vessel Type (fishing, tanked, etc), Latitude, Longitude, Heading, Speed and more.
The attributes named above can easily give us an idea if the vessel is heading a direction that intercepts the marine reserve.  With this in mind the model will do the following if a vessel is in a heading intercepting the marine reserve within a certain distance at time T and on the next API call or T+1 the vessel is no longer showing up, I will conclude that this vessel has turned off its tracking system to get closer or into the Marine Reserve without being tracked.