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

Current gear requirement only needs to represent `bandage`.

Warm-up classification, RPE, failed repetitions, tempo, and similar measurements are not required for Core v1.

### 6.4 Future analysis requirements

The stored representation must make it possible to later calculate:

- heaviest weight;
- highest repetitions;
- highest repetitions at a given weight;
- best matching schemes such as 5x5;
- total sets;
- total repetitions;
- tonnage;
- frequency;
- performance trends;
- variant comparisons;
- geared versus ungeared comparisons.

Tonnage is:

    sum(weight × repetitions)

Tonnage is primarily meaningful within comparable lifts and is a secondary metric.

A set scheme may occur within a larger unit. For example, five 105 kg × 5 sets followed by a 110 kg single still contains a valid 105 kg 5x5 performance.

## 7. Training Sessions

Current training-session units include:

- lifting;
- kyokushin;
- grappling.

Conceptual grammar:

    <unit_name> <start_time>-<end_time> <gym> [# comment]

A session records:

- start time;
- end time;
- gym;
- optional comment.

Duration is derived from start and end time.

### 7.1 Detailed units and sessions

Detailed performance units may belong to sessions.

Example:

    lifting session
        squat
        bench

The relationship is useful and should eventually be represented.

However:

- the performance unit must be valid without a session;
- the session must be valid without detailed performance units;
- a performance unit may be created before its corresponding session exists;
- association must therefore be possible after creation;
- association must not make the normal logging workflow more cumbersome.

The precise implementation of association is not a Core v1 requirements decision.

## 8. Running

Conceptual grammar:

    running <start_time> <running_time> <gym> <distance>
            [--avghr=<bpm>]
            [--maxhr=<bpm>]
            [--cal=<kcal>]
            [# comment]

Example:

    running 1800 28:52 wettingen 5.2 --avghr=134 --maxhr=160 --cal=500

Required data:

- start time;
- running duration;
- gym;
- distance;
- optional average heart rate;
- optional maximum heart rate;
- optional calories;
- optional comment.

`gym` is intentional domain terminology. For example, `wettingen` may imply the known 400 m running track.

Derived values such as pace and average speed should not need manual entry.

### 8.1 Future analysis

The representation must support future calculation of:

- running frequency;
- total distance;
- total running time;
- longest distance;
- fastest comparable runs;
- pace trends;
- heart-rate trends;
- performance at comparable distances;
- performance relative to body weight/body composition.

## 9. Swimming

Swimming follows the general cardio concept of running.

It additionally supports:

- optional water temperature;
- optional pool length.

Swimming distance remains manually authoritative because device measurements may be incorrect.

Exact BCL option names for the additional measurements are not yet specified.

## 10. Skipping

Skipping follows the general cardio concept of running but does not contain distance.

It may contain:

- start time;
- duration;
- gym;
- average heart rate;
- maximum heart rate;
- calories;
- comment.

Exact final grammar remains to be specified.

## 11. Wim Hof

Conceptual grammar:

    wimhof (<breaths> <retention_seconds>)+
            [--zen-mode]
            [--guide=<guide>]
            [# comment]

At least one round is required.

Each round contains:

- number of breaths as an integer;
- retention duration as integer seconds.

Unit-level context may contain:

- zen mode;
- guide;
- comment.

### 11.1 Future analysis

The representation must support:

- frequency;
- longest retention;
- retention trends;
- retention relative to number of breaths;
- comparisons under similar breath counts;
- comparison by zen mode or guide;
- future cross-domain analysis against stress/mood data.

Retention must not be interpreted independently of breath count when making performance comparisons.

## 12. Chrono Units

Chrono units represent activities where duration is the primary relevant measurement.

Conceptual grammar:

    <unit_name> <time_string>

Examples:

    splitmachine 16
    plank 1:25
    someunit 1:02:30

Duration syntax:

- integer → minutes;
- `MM:SS` → minutes and seconds;
- `HH:MM:SS` → hours, minutes, and seconds.

Internally these forms represent the same duration concept.

Chrono units do not require explicit start/end times, gym, or additional context unless future requirements justify them.

Future analysis includes:

- frequency;
- total duration;
- average duration;
- average duration per day;
- longest duration;
- duration trends.

## 13. Work

Work supports both exact time intervals and duration-only records.

Conceptual grammar:

    work <time_spec> <gym> <project> <content> [# comment]

where:

    time_spec :=
        <duration>
        OR
        <start_time>-<end_time>

Examples:

    work 2h nautilus rust ownership
    work 1100-1430 risktec project-x start

`gym` intentionally represents the place/context.

For example:

- `nautilus` may represent home;
- `risktec` may represent the Risktec office.

Work records:

- duration;
- optional start/end time when known;
- gym;
- project;
- content;
- optional comment.

When an interval is supplied, duration is derived.

A duration-only work record must not receive invented start/end times.

Future analysis includes totals and averages grouped by:

- project;
- content;
- gym;
- time period.

## 14. Generic Log

Conceptual grammar:

    log <text>

A generic log records:

- occurrence time;
- arbitrary private text.

Bushido must not require generic logs to have categories.

The meaning/content of private log entries is outside the requirements specification.

## 15. Temporal History

All units should participate in a common historical view where meaningful.

Bushido should eventually be able to answer:

    What did I do last Saturday?

The result should include the units Bushido knows were recorded for that day.

Absence of a unit does not technically prove an activity did not occur, although the user may treat absence as meaningful for activities they consistently record.

Bushido must not invent activities to fill temporal gaps.

## 16. Query and Analysis Requirements

Rich querying is not required for Core v1.

However, the stored data must support future capabilities including:

### Retrieval

- activities on a given day;
- recent instances of a unit;
- historical records around a given date.

### Aggregation

- counts;
- sums;
- averages;
- minima/maxima;
- frequency.

### Records

Examples:

- heaviest deadlift;
- most repetitions;
- longest run;
- longest Wim Hof retention.

### Temporal analysis

- streaks;
- frequency;
- trends;
- historical comparisons.

Example:

    longest streak of days containing at least one training unit

### Period comparison

Example:

    Compare the last three weeks against six months ago.

### Cross-domain analysis

Example:

    Compare body weight, lifting performance, and running performance.

Cross-domain analysis is a future capability but must not be prevented by the Core v1 data model.

## 17. BCL Scope

BCL is a small deterministic command language.

Core v1 should prioritize unit creation/logging.

Sophisticated query commands are not required before the logging system is complete.

A future simple query may look like:

    find squat -m 6

BCL should remain:

- deterministic;
- predictable;
- easy to parse;
- easy to use interactively.

BCL does not need to become a complete analytical query language.

## 18. Client/API Separation

BCL must not become Citadel's internal protocol.

Citadel should expose structured application capabilities that clients can consume directly.

For example, a Textual squat tab should be able to retrieve structured squat/set data without:

1. generating a BCL `find` command;
2. receiving formatted terminal output;
3. parsing that output back into structured data.

BCL, Textual, Elm, future Rust clients, and future natural-language interfaces should operate on the same underlying application/domain functionality.

## 19. Future Natural-Language Interface

A future LLM interface may support questions such as:

    How was my running six months ago compared with now?

The LLM should preferably translate user intent into structured Bushido operations.

It should not require direct database access or parsing human-formatted BCL output.

This is outside Core v1.

## 20. External Data

Future external sources include at least:

- Withings body composition;
- Garmin activity/fitness data.

Withings may provide observations including:

- weight;
- body-fat percentage;
- muscle measurements;
- PWV;
- other device measurements.

External import is outside Core v1.

The Core architecture should nevertheless permit imported typed observations to coexist with manually created units.

## 21. Deferred Domains

The following are explicitly deferred:

- dumbbell/unilateral strength modeling;
- broader strength-training modeling;
- food/nutrition;
- detailed Kyokushin content;
- detailed grappling content;
- Garmin import;
- Withings import;
- mood/stress modeling;
- goals;
- gamification;
- overall day/week scoring;
- recommendations;
- natural-language querying.

Deferral does not mean these features are rejected. Core v1 should simply avoid unnecessary design commitments that would make them difficult to add later.

## 22. Core v1 Success Criterion

The fundamental pipeline is:

    input
      ↓
    parse
      ↓
    validate
      ↓
    domain representation
      ↓
    persist
      ↓
    retrieve
      ↓
    same correct information

For every Core v1 unit, Bushido should reliably preserve the meaningful information supplied by the user.

The implementation should be well tested before sophisticated analytics are added.

## 23. Core v1 Non-Goals

Core v1 does not need to answer:

    Was this a good week?

It does not need:

- scoring;
- optimization;
- recommendations;
- comprehensive analytics;
- AI;
- automatic behavioral judgment.

The immediate goal is simpler:

> **Build a reliable, well-engineered foundation containing correct personal activity data from which those capabilities can later be built.**