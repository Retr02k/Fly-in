*This project has been created as part of the 42 curriculum by psilva-p.*

# Fly-in

## Description

Fly-in is a Python simulation of drones travelling through a directed-looking
map of bidirectional hub connections. Drones must move from one start hub to
one goal hub while respecting hub capacity, connection capacity, weighted zone
costs, restricted-zone transit, simultaneous movement, and deadlock rules.

The project deliberately uses no graph library. Parsing, validation, routing,
simulation, terminal rendering, logging, and tests are implemented in Python
with Pydantic used for the core data models.

The map parser requires exactly one `start_hub` and one `end_hub`, positive
drone and capacity values, unique hub names, unique hub coordinates, valid
integer coordinates, valid zone metadata, and connections that reference
existing hubs. Coordinates may be negative: they are still valid integers and
are useful for maps laid out around an origin. Invalid maps produce a
filepath- and line-aware `MapParseError`.

## Instructions

Install the project and development dependencies with:

```bash
uv sync
```

Run the interactive terminal application:

```bash
make run
```

Or:

```bash
uv run fly-in
```

The menu lists the supplied maps and also accepts a custom map path. Choose a
complete run or step-by-step mode, then optionally save the run log. Existing
log files are overwritten so each file describes one reproducible run. Log
filenames are always stored below the repository's `output/` directory;
absolute paths and path traversal are rejected.

Run the automated checks:

```bash
make test
make lint
make lint-strict
```

For debugger use:

```bash
make debug
```

The detailed architecture and implementation rationale are documented in
[`docs/explanation.md`](docs/explanation.md).

The program also exposes a testable `run_cli()` function. It accepts injected
input and output streams, so tests do not need to control a real terminal.

## Algorithm and implementation

The parser converts map directives into typed hubs, connections, and map
objects. The graph builder creates bidirectional adjacency without external
dependencies. `GraphTraversal.find_best_route()` uses a heap-based weighted
search. Normal and priority zones cost one, restricted zones cost two, and
blocked zones are excluded. Equal-cost routes prefer more priority zones and
then deterministic hub ordering.

Each simulation turn has separate phases:

1. Existing transit is progressed.
2. Waiting drones calculate legal planned moves.
3. Hub and connection reservations are checked in deterministic drone-ID
   order.
4. Approved moves become active transit states.

Restricted movement occupies its connection for two turns and reserves the
destination before departure. The simulator keeps physical hub occupancy,
destination reservations, and shared bidirectional connection usage distinct.
Active transit is valid progress, so it cannot be mistaken for a deadlock.

Routes are cached by origin and destination. The cache stores immutable tuples,
while capacity checks remain dynamic and are performed every turn.

The design is object-oriented without pretending that every operation must be
a method. `MapParser`, `MapBuilder`, `GraphBuilder`, `GraphTraversal`, and
`Simulator` each own a cohesive responsibility. `Map`, `Hub`, `Connection`,
`Drone`, `TransitState`, and `PlannedMove` are typed objects representing the
domain state. Composition connects these objects: the simulator owns drones
and uses graph and model objects, while the parser composes handlers and a
builder. Small pure helper functions are kept where they improve clarity;
object-oriented design is demonstrated by responsibility, encapsulation, and
collaboration between domain objects, not simply by placing every line inside
a class.

## Map validation errors

Errors identify the source file, physical line, and reason. For example:

```text
maps/example.txt: line 4: nb_drones must be greater than zero
maps/example.txt: line 7: hub 'waypoint1' has the same coordinates
as hub 'start'
```

This makes malformed input easier to correct without exposing an internal
traceback. Negative coordinates are accepted because the format requires
integers, not only non-negative integers.

## Visual representation

The standard-library TUI displays the current turn, start and goal, each hub's
coordinates-derived ordering, zone type, and drones currently at that hub.
Restricted drones are shown on their active connection. Step mode pauses after
each rendered turn so the movement can be inspected. ANSI colors are enabled
when the output is a terminal and are omitted from redirected output.

After delivery, the program reports total turns, movement events, average
turns per drone, total and average weighted path cost, waiting turns,
restricted transits, throughput, and route-cache hits and misses.

## Example

Select `src/maps/easy/01_linear_path.txt` and choose a complete run:

```text
Turn 0 | start -> goal
Turn 1 movement events:
  D1 moved start -> waypoint1 (arrived this turn).
Turn 2 movement events:
  D1 moved waypoint1 -> waypoint2 (arrived this turn).
  D2 moved start -> waypoint1 (arrived this turn).
...
Delivered 2 drones in 4 turns.

Simulation statistics
  Turns: 4
  Total movement events: 8
```

Movement output explicitly distinguishes departures, completed arrivals, and
restricted drones in transit on a connection. The hub snapshot below each
turn shows where drones are physically located; a drone listed as in transit
is not physically occupying either endpoint hub.

## Resources

- Python documentation: https://docs.python.org/3/
- Pytest documentation: https://docs.pytest.org/
- Pydantic documentation: https://docs.pydantic.dev/
- Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- 42 Lisboa project subject and map-format specification.

AI was used as an engineering aid during development. The project was
designed and implemented by the author, with AI assistance for architecture
discussions, debugging, test design, documentation, and code review. The
author made the final implementation decisions, validated the results, and is
responsible for understanding and maintaining the code.
