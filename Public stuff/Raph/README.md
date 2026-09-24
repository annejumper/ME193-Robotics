# Raph

A driving template built on the same pattern as
[useful libraries/main.py](../useful%20libraries/main.py), for a car with a
**Double Motor**, **Controller**, and **Color Sensor**.

- Joysticks drive the car tank-style (left stick = left wheel, right stick =
  right wheel).
- The color sensor triggers an action when it sees a new color:

| Color   | Action        |
|---------|---------------|
| Red     | stop          |
| Green   | forward       |
| Yellow  | slow forward  |
| Magenta | reverse       |
| Blue    | turn left 90° |
| Purple  | turn right 90°|
| Orange  | spin 180°     |

Teal, White, Azure, and "No color" are empty — fill in the `Do...()`
functions with whatever you want.

## Run

```bash
pip install legoeducation
python main.py
```

Set the `..._CARD_COLOR` / `..._CARD_SERIAL` values at the top of `main.py`
to match your connection cards first. `lelib.py` is a copy of the shared one
in `useful libraries/`.
