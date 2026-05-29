# openconstruct-jupyter — Jupyter Integration for OpenConstruct

Connect OpenConstruct to your Jupyter notebooks in one line. Cell magic, widgets, fleet panels, and DataFrame-to-room conversion.

**Part of [SuperInstance OpenConstruct](https://github.com/SuperInstance/OpenConstruct).**

## What This Gives You

- **Cell magic** — `%%openconstruct --sense vision` captures output as a sense shadow
- **DataFrame → Plato room** — turn any pandas DataFrame into a knowledge graph
- **Python function → agent tool** — `oc.from_function(greet, name="my_tool")`
- **Fleet panel** — inline widget showing discovered fleet nodes
- **Room viewer** — visualize Plato room tiles and dependencies

## Quick Start

```python
# Load the extension
%load_ext openconstruct_jupyter

# Connect
import openconstruct_jupyter as oc
oc.connect(notebook=True)
```

### Cell Magic

```python
%%openconstruct --sense vision
# Cell output captured as a vision shadow

%%openconstruct --tick "analysis complete"
# Post a tick to the fleet

%%openconstruct --room my-analysis
# Create or load a Plato room
```

### Python API

```python
import pandas as pd

# DataFrame → room
df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
oc.from_dataframe(df, name="my_data")

# Function → agent tool
def greet(name):
    return f"Hello, {name}!"
oc.from_function(greet, name="greet_tool")

# REST API → agent resource
oc.from_api("https://api.example.com/data", name="external_data")
```

## Installation

```bash
pip install openconstruct-jupyter
```

## Testing

```bash
pytest tests/ -v
```

## License

MIT
