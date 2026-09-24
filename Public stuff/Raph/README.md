# Raph

A color-sensor template built on the same pattern as
[useful libraries/main.py](../useful%20libraries/main.py), using a
**Double Motor** and a **Color Sensor**.

The color sensor spins the **left** motor of the Double Motor one full turn
when it sees a new color:

| Color  | Action                            |
|--------|-----------------------------------|
| Blue   | left motor clockwise (360°)       |
| Orange | left motor counterclockwise (360°)|

Every other color is an empty `Do...()` function — fill them in with
whatever you want. Change `LEFT_MOTOR_DEGREES` to turn more or less.

## Run

```bash
pip install legoeducation
python main.py
```

Set the `..._CARD_COLOR` / `..._CARD_SERIAL` values at the top of `main.py`
to match your connection cards first. `lelib.py` is a copy of the shared one
in `useful libraries/`.
