## Purpose

Provide an approachable graphical school experience that exposes verified grouping, teaching and result behavior with clear character identities and visible changes.

## ADDED Requirements

### Requirement: Graphical school planning
The playground SHALL show original portraits and character names, five classes, waiting members and available course choices; member moves and assignments MUST use supported school rules.

#### Scenario: Arrange a teaching class
- **WHEN** the player moves a teacher and students to a class and chooses an available course
- **THEN** the portraits, class membership and course display update to the validated session state

### Requirement: Guided result sequence
The playground SHALL guide the player through planning, growth, confirmation and MVP with enabled actions appropriate to the current stage; completed results SHALL show attribute changes and MVP identity without repeating writes.

#### Scenario: Complete teaching
- **WHEN** the player settles, confirms and completes the supported teaching result
- **THEN** student growth and MVP are displayed once, and the date remains April week four with the chapter pending

### Requirement: Accessible playground launch
The default project launch SHALL open the graphical playground and SHALL retain access to the existing battle/research scene and a route back to the playground.

#### Scenario: Navigate to battle and return
- **WHEN** the player opens the battle preview and returns to the playground
- **THEN** the previously saved playground choices and result can be restored

### Requirement: Visible scope and input feedback
The playground SHALL present its fourth-week scope, readable failure feedback, character details and selection state at 1024 by 768, and SHALL prevent accidental battle commands while the school is open.

#### Scenario: Unsupported move
- **WHEN** a player attempts to place a student in a class without a teacher
- **THEN** a readable instruction is displayed and the school state remains unchanged
