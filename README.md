# openconstruct-jupyter

> Connect OpenConstruct to your Jupyter notebooks in one line.

## Install

```bash
pip install openconstruct-jupyter
```

## Quickstart

```python
# Load the extension
%load_ext openconstruct_jupyter

# Connect your notebook
import openconstruct_jupyter as oc
oc.connect(notebook=True)
```

## Cell Magic

```python
%%openconstruct --sense vision
# Cell output is captured as a vision shadow and auto-registered with the fleet

%%openconstruct --tick "analysis complete"
# Post a tick to the fleet

%%openconstruct --room my-analysis
# Create or load a Plato room from notebook context

%%openconstruct --fleet
# Show fleet discovery inline
```

## Python API

```python
import openconstruct_jupyter as oc

oc.connect(notebook=True)

# DataFrame → Plato room
import pandas as pd
df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
oc.from_dataframe(df, name="my_data")

# Python function → agent tool
def greet(name):
    return f"Hello, {name}!"
oc.from_function(greet, name="my_tool")

# ML model → sense module
# oc.from_model(model, name="my_model")

# REST API → agent resource
oc.from_api("https://api.example.com/data", name="my_api")

# Publish the notebook's room with the fleet
oc.publish_room()
```

## Example Notebooks

| # | Notebook | Description |
|---|----------|-------------|
| 01 | [Quickstart](openconstruct_jupyter/examples/01-quickstart.ipynb) | Load, connect, and use in 5 minutes |
| 02 | [Sense Modules](openconstruct_jupyter/examples/02-sense-modules.ipynb) | Build and register sense modules |
| 03 | [Fleet Discovery](openconstruct_jupyter/examples/03-fleet-discovery.ipynb) | Explore fleet topology and health |
| 04 | [Plato Rooms](openconstruct_jupyter/examples/04-plato-rooms.ipynb) | Create, populate, and share rooms |
| 05 | [Custom Module](openconstruct_jupyter/examples/05-custom-module.ipynb) | Build a sense module from scratch |

## Integration with Existing Work

openconstruct-jupyter is designed to slot into your existing Jupyter workflow:

- **Variables** from notebook cells are automatically available as room tiles
- **DataFrames** auto-convert to Plato room items with CR scores
- **Plot outputs** auto-capture as vision shadows
- **Import any Python library** and it becomes a sense module candidate
- **IPython widgets** provide interactive dashboards for fleet status, rooms, and ticks

## License

MIT
