# Code

## Files
### climate_lib.py
This contains code that is shared between climate_app.py and climate.ipynb.
I made a class called Climate_Database to handle the SQLAlchemy code for the database.

### climate.ipynb
This contains code to analyze the data using charts.
#### How to Run
<ol>
	  <li>In the terminal, initialize an Anaconda environment using "source activate <i>{your environment}</i>".</li>
	  <li>Open Jupyter Notebook using "jupyter notebook" in the terminal.</li>
	  <li>In the Jupyter Notebook, open the ipynb file that contains the code.</li>
	  <li>
	    With the code open, you have two options on how to run the code:
	    <ul>
	      <li>
		In the menu bar open Kernel > Restart and Clear Output.  Then you can use Shift+Enter to run the code one block at a time.
	      </li>
	      <li>In the menu bar open Kernel > Restart and Run All.  This will run all of the blocks of code at once.</li>
	    </ul>
	  </li>
</ol>

### climate_app.py
This contains code for running a web server.
The web server provides APIs to access the data within the database.
#### How to Run
<ol>
    <li>Open this (code) folder in a terminal.</li>
    <li>In the terminal, run "python climate_app.py"</li>
    <li>A url should be provided in the output. Open that URL in a web browser</li>
    <li>The index page should provide further instructions to access the API endpoints.</li>
</ol>