How to use this:

`cd` into the `static` folder.
Run the command `npm i` to install all the stuff from the node package manager.
Run the command `npm run build` (or `npm run watch`).
`cd` into the `server` folder.
Install the python requirements in `requirements.txt` (most likely with `python pip install -r requirements.txt`).
Run `python server.py`.
Visit the location that the previous command printed out.

Then, type out your schedule like the following:

Sleep (9 hours)
Work out (1h 20m)
Eat (2.5h)

and hit the "Send input!" button.

The app will compute the total amount of time of the things you put in the schedule.

Note that the backend (the part that computes the total time) is written completely in Python.
So this gives a nice way to have fun with little python scripts.
Feel free to edit and use to create your own websites!
