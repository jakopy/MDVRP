# MDVRP
Multi-Depot Vehicle Routing Problem

Please View/ Download the presentation slides for more information.

To ensure the code runs properly on your computer you will need to do the following: <br>
Get a Gurobi License: https://gurobi.com <br>
1. Make Sure Flask is installed for your python version: pip install flask <br>
2. You will need to edit the file titled map_view.html in the following way: <br>
replace YOUR KEY HERE with a google maps api key obtained from maps.googleapis.com <br>
< script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key= YOUR KEY HERE &sensor=false" > < / script > <br>
Additionally, you may wish to get a distance matrix api plug in for google maps and can edit the
API key in the distancematrix.py file <br>
3. Once This Directory is downloaded open a command prompt in the same directory and run python app.py
