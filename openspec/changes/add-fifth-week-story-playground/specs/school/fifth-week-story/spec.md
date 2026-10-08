## Purpose

Let playground players read the actual fifth-week scene and preserve its progress and verified exit while retaining earlier school results.

## ADDED Requirements

### Requirement: Verified fifth-week selection and exit
The fifth-week continuation SHALL select the source CH001 4/5 branch, execute Chapter018 control flow and expose its verified workroom-entry request. Evidence MUST distinguish original execution, readiness waits, scheduler boundaries and unexecuted workroom/school bodies.

#### Scenario: Ready continuation
- **WHEN** the completed native fourth-week chain loads CH001 at 4/5 and presentation is ready
- **THEN** Chapter018 is selected, its effectful exit executes once and pending8 is recorded.

#### Scenario: Pending presentation
- **WHEN** key, UI or fade readiness blocks the continuation
- **THEN** the evidence records a bounded wait without falsely declaring Chapter018 completion.

### Requirement: Original mixed character presentation
The fifth-week reader SHALL display all original Chapter018 text in order with current slot speakers, source background, visible large characters and small portraits, including character resource replacements. Presentation resources MUST carry verifiable source/output hashes.

#### Scenario: Portrait replacement
- **WHEN** Chapter018 changes a visible slot resource
- **THEN** subsequent pages use the replacement image and speaker identity while preserving earlier pages.

### Requirement: Durable once-only fifth-week progress
Players SHALL start, advance, revisit, return from and confirm skipping the fifth-week story, then reach the workroom-entry summary. Repeated completion MUST preserve date, growth, MVP counts and audited exit state. Invalid commands or saves MUST leave state unchanged; valid version1/2 saves MUST migrate.

#### Scenario: Resume inside fifth-week story
- **WHEN** a player saves after a portrait replacement and loads again
- **THEN** the exact page, slot images and prior results are restored.

#### Scenario: Skip cancellation and repeated completion
- **WHEN** the player cancels skipping or repeats completion after reaching the exit
- **THEN** cancellation changes nothing and completion cannot advance another week or repeat course results.

#### Scenario: Previous arrival save
- **WHEN** a valid version2 4/5 arrival save is loaded
- **THEN** its original state is retained and the fifth-week story becomes available.

### Requirement: Graphical continuation acceptance
The default playground SHALL provide visible fifth-week story and workroom-entry navigation, saving and battle-preview return. It MUST state the unimplemented school arrangement boundary and pass rendered checks for readable dialogue and unobscured controls.

#### Scenario: Battle preview round trip
- **WHEN** a player enters battle preview from the fifth-week exit and returns
- **THEN** the persisted exit and date4/5 are restored with unchanged course results.
