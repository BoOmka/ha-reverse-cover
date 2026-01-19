# Reverse Cover

Reverse Cover is a Home Assistant integration that creates a new cover entity whose
movement, state, and position are inverted from a selected source cover.

## Usage

1. Add the integration via the Home Assistant UI.
2. Select the source cover you want to reverse.
3. A new reversed cover entity will be created.

## Notes

- Opening the reversed cover sends a close command to the source cover.
- Positions are inverted (0 becomes 100, 25 becomes 75, etc.).
