# Chess PyQt6 – Domain Driven Design

A fully interactive chess application built with **PyQt6** and **Domain-Driven Design** principles. All graphics are procedurally generated (no asset files). Click to move pieces, drag to resize the window.

## Features

✅ **Fully Playable**: Click pieces to select, valid moves highlight in green
✅ **All 6 Piece Types**: Pawn, Rook, Knight, Bishop, Queen, King with proper move rules
✅ **Responsive UI**: Drag window edges to resize — board scales smoothly
✅ **Procedural Graphics**: All pieces drawn with QPainter, no assets
✅ **Full Move Validation**: Blocks, captures, piece-specific rules implemented
✅ **36 Comprehensive Tests**: Domain, services, moves, rendering all tested
✅ **Clean Architecture**: DDD with factories, repositories, services, use cases

## Quick Start

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the game
python main.py

# Run tests
pytest tests/ -v
```

## How to Play

1. **Click a piece** — highlights selected piece (yellow) and valid moves (green)
2. **Click a valid green square** — moves the piece
3. **Drag window edges** — board resizes smoothly with all pieces scaling

## Architecture

### Domain Layer (`src/domain/`)
- **entities.py**: Position (immutable), Piece, PieceType, Team value objects
- **board.py**: Board aggregate managing 32 pieces at standard starting positions

### Infrastructure Layer (`src/infrastructure/`)
- **factories.py**: PieceFactory for object creation
- **repositories.py**: PieceRepository, BoardRepository abstractions

### Application Layer (`src/application/`)
- **services.py**: 
  - `BoardSetupService`: Initialize standard game
  - `BoardQueryService`: Query piece positions
  - `MoveValidator`: Calculate valid moves per piece type
  - `MoveExecutor`: Execute validated moves
- **usecases.py**: 
  - `InitializeGameUseCase`
  - `GetValidMovesUseCase`
  - `ExecuteMoveUseCase`
  - `RenderBoardUseCase`
- **rendering.py**: 
  - `SVGPieceRenderer`: Procedural piece drawing with QPainter
  - `PieceRenderingStrategy`: Strategy pattern for renderers

### Presentation Layer (`src/presentation/`)
- **controller.py**: `ChessController` orchestrating use cases and UI interaction
- **ui.py**: 
  - `ChessBoardWidget`: Board rendering, mouse events, resizing
  - `ChessApplication`: PyQt6 window wrapper

### Tests (`tests/`)
- **test_domain.py** (15 tests): Position, Piece, Board operations
- **test_factories.py** (2 tests): Factory creation
- **test_moves.py** (11 tests): Move validation for all piece types
- **test_rendering.py** (2 tests): Rendering integration
- **test_services.py** (6 tests): Service layer operations

**Total: 36 tests, all passing ✅**

## Design Patterns

| Pattern | Location | Purpose |
|---------|----------|---------|
| Factory | `PieceFactory` | Centralized piece creation |
| Strategy | `PieceRenderingStrategy` | Pluggable rendering implementations |
| Repository | `PieceRepository`, `BoardRepository` | Data access abstraction |
| Use Case | All in `usecases.py` | Isolated business operations |
| Service Layer | `services.py` | Orchestrate domain + repos |
| MVC | `ChessController` + `ChessBoardWidget` | Separation of concerns |

## SOLID Principles

| Principle | Implementation |
|-----------|-----------------|
| **S**ingle Responsibility | Each class has one reason to change (MoveValidator only validates, MoveExecutor only executes) |
| **O**pen/Closed | Open for extension via PieceRenderingStrategy; closed for modification |
| **L**iskov Substitution | All rendering strategies implement consistent interface |
| **I**nterface Segregation | Minimal, focused interfaces (BoardQueryService separate from BoardSetupService) |
| **D**ependency Inversion | High-level modules depend on abstractions (services, use cases) not concrete UI |

## Move Validation

Each piece type has specific movement rules:

- **Pawn**: Forward 1-2 squares, diagonal capture only
- **Rook**: Any direction straight line, blocked by pieces
- **Knight**: L-shaped (2+1), jumps over pieces
- **Bishop**: Diagonal any distance, blocked by pieces
- **Queen**: Rook + Bishop combined movement
- **King**: One square in any direction

All moves include:
- ✓ Friendly fire prevention
- ✓ Blocking detection for sliding pieces
- ✓ Capture support
- ✓ Boundary validation

## Files Structure

```
Chess_pyqt-css/
├── src/
│   ├── domain/              (Business logic)
│   │   ├── entities.py      (Position, Piece, PieceType, Team)
│   │   └── board.py         (Board aggregate, starting positions)
│   ├── infrastructure/      (Data & creation)
│   │   ├── factories.py     (PieceFactory)
│   │   └── repositories.py  (Data access)
│   ├── application/         (Business operations)
│   │   ├── services.py      (BoardSetup, MoveValidator, MoveExecutor)
│   │   ├── usecases.py      (Game operations)
│   │   └── rendering.py     (Procedural piece drawing)
│   └── presentation/        (UI layer)
│       ├── controller.py    (ChessController)
│       └── ui.py            (ChessBoardWidget)
├── tests/                   (36 comprehensive tests)
│   ├── test_domain.py
│   ├── test_factories.py
│   ├── test_moves.py
│   ├── test_rendering.py
│   └── test_services.py
├── main.py                  (Entry point)
├── requirements.txt         (PyQt6, pytest)
└── README.md               (This file)
```

## Code Quality

- ✅ **Self-documenting**: Zero comments, clear naming
- ✅ **Type hints**: Full type annotations throughout
- ✅ **No magic**: Clear constants and enums
- ✅ **Immutable values**: Position is frozen, cannot be accidentally modified
- ✅ **Comprehensive tests**: 36 tests covering domain, services, rendering, moves
- ✅ **Clean errors**: Explicit validation with meaningful error messages

## Next Steps (Easy to Add)

With the current DDD architecture, these are straightforward extensions:

- **Check/Checkmate detection**: Add `CheckDetectionService`
- **En passant**: Extend `MoveValidator._get_pawn_moves()`
- **Castling**: Add special move in `ExecuteMoveUseCase`
- **Promotion**: Add pawn promotion in `MoveExecutor.execute_move()`
- **Move history**: Add `MoveHistoryRepository`
- **AI opponent**: Add `MiniMaxService` with `BoardEvaluationService`
- **Network play**: Add `GameNetworkService`, `P2PRepository`
- **Timers**: Add `TimerService` for speed chess
- **Undo/Redo**: Add `UndoRedoService`

## Dependencies

- **PyQt6**: GUI framework
- **pytest**: Testing framework

All dependencies installed via `requirements.txt` in the virtual environment.

## Technical Notes

### Why DDD?
Domain-Driven Design separates business logic from infrastructure concerns:
- **Domain**: Chess rules (valid moves, piece behavior) — independent of UI/database
- **Infrastructure**: How data is created/stored — easy to swap implementations
- **Application**: Business operations (move execution) — pure orchestration
- **Presentation**: UI interaction — thin layer calling use cases

This makes the code:
- **Testable**: Test rules without UI (all 36 tests run without GUI)
- **Maintainable**: Changes to rules don't affect UI or persistence
- **Extensible**: Add new features by adding services/use cases
- **Reusable**: Domain logic usable in CLI, web, AI, etc.

### Performance
- 36 tests complete in <1 second
- No external assets — board renders instantly
- Smooth resizing with dynamic square calculations
- Efficient piece lookup (O(1) by position)

### Cross-Platform
- Works on macOS, Linux, Windows (tested on macOS)
- Uses PyQt6 (native cross-platform GUI)
- Dynamic font/rendering — adapts to platform
