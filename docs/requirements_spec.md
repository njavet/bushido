# Bushido Core v1 — Requirements Specification

## 1. Purpose

Bushido is a long-lived personal activity data system.

Its primary purpose is to:

- reliably record activities and observations;
- preserve this history over long periods;
- represent different activities using appropriate structured data;
- provide a foundation for later retrieval, statistics, comparison, visualization, and cross-domain analysis.

Bushido Core v1 focuses on **capturing correct data**.

Advanced analytics, goals, gamification, recommendations, natural-language querying, and similar features are explicitly not required for Core v1.

## 2. Design Principles

### 2.1 Store facts, derive information, postpone judgment

Bushido records what happened.

It should not currently determine whether a day, week, training session, or behavior was "good" or "bad."

Future systems may provide goals, scoring, or recommendations using the recorded data.

### 2.2 Useful data over maximum data

Bushido should not collect measurements merely because they can be measured.

Data should primarily support:

- historical reconstruction;
- frequency and consistency analysis;
- performance analysis;
- trend analysis;
- future cross-domain analysis.

Additional information can remain free text until a concrete requirement justifies structured representation.

### 2.3 Avoid false precision

Unknown information must remain unknown.

Examples:

- A duration-only work unit must not receive an invented start time.
- Old units lacking a newly introduced measurement remain valid.
- A squat does not require precise start/end timestamps if those times have no analytical value.

### 2.4 Historical data remains valid

Schemas may evolve.

New fields must not invalidate historical records.

If RPE is added to squat in the future, old squat records remain valid with RPE unknown.

Unknown values must not be silently replaced with defaults or estimates.

### 2.5 Manual records are authoritative

For Core v1, manually entered Bushido data is authoritative.

Future Garmin, Withings, or other imports may enrich or create records, but external-device measurements must not automatically override known-correct manual information.

### 2.6 Logging must remain low-friction

Detailed tracking must not become mandatory merely because Bushido supports it.

For example:

- a lifting session does not require every exercise to be recorded;
- a Kyokushin session does not require every drill to be recorded;
- optional metrics may be omitted;
- comments can preserve unstructured information without requiring new schema.

## 3. Unit Concept

A **unit** is a named, typed record representing an activity, event, or observation.

Each unit:

- has a unique unit name;
- has defined semantics;
- has its own structured data;
- may define its own BCL grammar;
- has an occurrence date/time or equivalent temporal context;
- may optionally contain free-text information.

A unit is not restricted to exercise.

Examples include:

- squat;
- running;
- lifting;
- work;
- Wim Hof;
- split-machine work;
- generic logs;
- future body-composition observations.

BCL is an interface for creating units. BCL does not define what a unit fundamentally is.

## 4. Mutation

Units may be updated or deleted to correct mistakes.

Bushido Core v1 does not require:

- event sourcing;
- revision history;
- tombstones;
- audit logs.

Replacing incorrect data with corrected data is sufficient.

The distinction between correcting a mistake and intentionally rewriting history is currently the user's responsibility.

## 5. Comments

Units may support optional free-text comments where appropriate.

Comments provide an escape hatch for useful information that does not yet justify structured modeling.

Example:

    kyokushin 1900-2030 dojo # hard sparring, new kata

Bushido should prefer this over prematurely introducing fields such as `sparring_intensity` or `kata_practiced`.

## 6. Lifting Performance Units

The five primary barbell lifting units are:

- squat;
- deadlift;
- bench;
- overheadpress;
- row.

`row` currently means barbell row.

### 6.1 Grammar concept

    <lift> (<rest_seconds> <weight_kg> <reps>)+
           [--variant <variant>]
           [--gear bandage]
           [# comment]

At least one set is required.

### 6.2 Set data

Each set contains:

- rest duration in seconds;
- weight in kilograms;
- repetitions.

Weight and repetitions may be non-integer numeric values.

Rest represents the rest preceding the corresponding set.

The first set may therefore have a rest value of zero.

### 6.3 Unit-level context

Variant applies to the complete lifting unit.

Gear applies to the complete lifting unit.

Current gear requirement only needs to represent
