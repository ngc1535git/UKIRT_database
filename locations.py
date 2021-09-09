# locations.py
#
# A list of observatory locations
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# Copyright May 2020
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from skyfield.api import Topos


#empty dict
locations = {}


###################################################################
# Arizona
###################################################################

#Hopkins
locations["Hopkins"] = Topos(31.688, -110.883, elevation_m=2608)

#Bigelow
locations["Bigelow"] = Topos(32.4165, -110.7345, elevation_m=2510)

#Bok
locations["Bok"] = Topos(31.9629, -111.6004, elevation_m=2071)

#Lemmon
locations["Mount Lemmon"] = Topos(32.44257, -110.7889, elevation_m=2805)

#Biosphere2
locations["Biosphere"] = Topos(32.58057, -110.8490, elevation_m=1164)


###################################################################
# Hawaii
###################################################################
#UKIRT
locations["UKIRT"] = Topos(19.8256111111, -155.4732222222, elevation_m=4194)

###################################################################
# LCO
###################################################################

#Haleakala
locations["Haleakala"] = Topos(20.7103846154, -156.256, elevation_m=3055)

#McDonald
locations["McDonald"] = Topos(30.67, -104.02, elevation_m=2070)

#CTIO
locations["CTIO"] = Topos(-30.1674, -70.8048, elevation_m=2198)

#Teide
locations["Teide"] = Topos(28.3, -16.5097222222, elevation_m=2330)

#South African Astronomical Observatory
locations["SAAO"] = Topos(-32.38, 20.81, elevation_m=1460)

#Siding Spring Observatory
locations["SidingSpring"] = Topos(-31.2733, 149.071, elevation_m=1116)
locations["SidingSpring_a"] = Topos(-31.2728611, 149.0708611, elevation_m=1116)






