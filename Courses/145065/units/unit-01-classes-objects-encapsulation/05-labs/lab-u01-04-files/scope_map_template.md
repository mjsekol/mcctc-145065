# Scope Map · shift_counters.py

Lab U01-04, Part 1. Copy this file as `scope_map.md` in the same folder as `shift_counters.py`,
then replace every TODO.

**Level** is one of: module (global), class, instance, local.
**Lives until** is when the name stops existing: the program ends, the object is gone, or the
function returns.
**Who should change it** names the code that is allowed to change it.

| Name | Level | Lives until | Who should change it |
|---|---|---|---|
| `SHIFT_NAMES` | TODO | TODO | TODO |
| `current_shift` | TODO | TODO | TODO |
| `line_name` | TODO | TODO | TODO |
| `starts_this_shift` | TODO | TODO | TODO |
| `asset_tag` | TODO | TODO | TODO |
| `strokes`, as `self.strokes` | TODO | TODO | TODO |
| `strokes`, inside `run` | TODO | TODO | TODO |
| `minutes` | TODO | TODO | TODO |
| `presses`, inside `main` | TODO | TODO | TODO |
| `press`, the loop variable in `main` | TODO | TODO | TODO |
| `lines`, inside `summary` | TODO | TODO | TODO |

## The three bugs

For each: the line, the level the name was at, the level it should have been at, and the fix.

1. TODO
2. TODO
3. TODO

## One design question

The smallest fix for one of the bugs uses the `global` statement. In two or three sentences,
say why a program with many functions that change globals is hard to trust, and where
`current_shift` could live instead.

TODO
