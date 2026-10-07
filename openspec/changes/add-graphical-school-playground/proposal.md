## Why

The verified school rules are currently exposed through text-heavy research panels and disconnected examples. Players need a visible, guided school experience that can preserve their choices and results between launches.

## What Changes

- Add a graphical fourth-week school playground with original portraits/background, named students, class cards, course choices, attribute details and result cards.
- Reuse the verified independent school session for every gameplay command; provide an explicit sequence from grouping through course growth, confirmation and MVP.
- Add versioned local playground saves restored through validated command replay, including source-rule fingerprints and atomic file replacement.
- Make the graphical playground the default launch scene, keeping the existing battle/research scene available.
- Preserve the explicit fourth-week boundary: no invented chapter completion, calendar advancement, original-save compatibility or complete-campaign claims.

## Capabilities

### New Capabilities

- `school/playground`: Graphical, guided school interaction and visible outcomes over the supported school domain.
- `school/playground-save`: Versioned save/recovery of an isolated playground session through validated commands.

### Modified Capabilities

None.

## Impact

New presentation assets/exporter, school UI/scene and playground controller/save module, project launch setting, focused tests and documentation. Existing audit panels, native evidence and source rule modules remain usable. No new external dependency or asset generation service.
