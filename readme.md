# qtsquares

Example code for learning the basics of coding GUI apps in Python with Qt and Pyside6

## Getting started

Steps to reproduce:

 1. Create a clean environemnt
 2. Clone the code
 3. Run the squares.py script

 ### Create a virtual environment

 Create the virtual environment & activate it
 (select the appropriate script for your set up)
 Install dependencies for Qt and Pyside6
 Also requires pandas.

  ```
  python -m virtualenv qt6
  ./qt6/Scripts/activate.ps1

  python -m pip install -r requirements.txt
  ```

### Clone the code & run the script

```
git clone https://github.com/ian1roberts/qtsquares.git
cd qtsquares
python squares.py
```
Use the cursor keys to move the red square around the 8x8 grid
Pressing space hits the square, and turns it blue
Revisit a blue square and hit space again to deactivate it.

A text map of avtivated squares is shown to the right.

Hit quit to close the game.

  