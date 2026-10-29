# Map Internals Deep Dive

> Implementation model updated for Go 1.24 Swiss tables (verified 2026-10-26 against the C08 research spec). Passages about buckets and overflow chains describe Go 1.23 and earlier and are kept only in the historical section at the end.

## Hash Table Structure (Go 1.24 and later)

Since Go 1.24, the runtime map uses a Swiss-table design (the runtime type is built around tables and groups, in `runtime/internal/maps`). The ideas that matter for reasoning about performance and memory:

- Entries live in **groups of 8 slots**. Each group holds 8 keys, 8 values, and one 64-bit control word.
- The control word carries **one metadata byte per slot**. Each byte is one of: an empty marker, a deleted marker (a tombstone left by deletion so probe sequences stay correct), or a **7-bit hash fragment called H2** taken from the key hash for an occupied slot.
- The rest of the hash (called H1) selects which group to start probing in.
- **Lookup is group-at-a-time probing:** the runtime compares all 8 H2 bytes of a group against the wanted fragment in parallel, checks only the candidate slots whose H2 matches, and probes the next group on a miss. There are no overflow buckets and no per-bucket chains to walk.
- Deleting a key marks its slot deleted rather than clearing the group, so other keys that probe through the same group are still found.

## Memory Growth and Capacity

- A table holds a whole number of groups. **Growth adds groups:** when the load factor gets too high (too many occupied or deleted slots per group on average), the runtime allocates a larger table with more groups and rehashes entries into it.
- Growth is incremental in effect for the programmer: there is no API-visible rehash step, and iteration order stays unspecified and randomized, exactly as before.
- **No `cap()` function:** capacity depends on hash distribution and group occupancy, not a fixed per-bucket limit. Preallocation (`make(map[string]int, expectedSize)`) is worthwhile for large maps to avoid repeated growth cycles.
- Maps do not promise to return memory when keys are deleted. Deleted slots become reusable tombstones; a map that once grew large generally keeps its table. If a long-lived map spikes and then empties, replace it with a fresh map when the memory matters, and prove the problem with a heap profile before optimizing.

## Preallocation

```go
// Without preallocation: repeated growth as entries are added
m := map[string]int{}

// With preallocation: the runtime sizes the table for the hint up front
m := make(map[string]int, expectedSize)
```

Preallocation avoids repeated growths. The hint is approximate: the runtime picks a group count whose capacity covers the hint at the target load factor.

## Pointers vs Values

For large value types, storing pointers reduces copy overhead:

```go
// Large struct: copied on every read and write
m := map[string]BigStruct{}  // copies large struct

// Pointer: only the pointer is copied
m := map[string]*BigStruct{} // copies 8-byte pointer
```

Trade-off: pointer maps add GC pressure. For small structs (under about 128 bytes, an estimate from common practice, not a runtime guarantee), value maps are typically faster. Measure with benchmarks and heap profiles for your own key and value types.

## `maps` Package (Go 1.21+)

| Function | Description |
| --- | --- |
| `Clone`, `Equal`, `EqualFunc` | Shallow copy and equality comparison |
| `Keys`, `Values`, `All` (1.23+) | Iterators over keys, values, or pairs |
| `Collect`, `Insert` (1.23+) | Build maps from iterators or insert entries |

See `samber/cc-skills-golang@golang-safety` skill for `Clone`, `Equal`, and sorted iteration patterns.

## Map Key Requirements

Map keys must be comparable (`==` must work). This includes:

- All numeric types, `string`, `bool`
- Pointers, channels, interfaces (compared by identity)
- Arrays of comparable types
- Structs where all fields are comparable

Slices, maps, and functions **cannot** be map keys.

## Historical: the pre-1.24 bucket design (Go 1.23 and earlier)

> Historical reference only. Nothing in this section describes the current runtime. It is kept so old profiles, old blog posts, and old code comments still make sense.

Before Go 1.24, a map was an array of buckets. The header held a count, a `B` field (log2 of the bucket count), a buckets pointer, and an oldbuckets pointer used during growth. Each bucket held 8 key-value pairs, with keys and values in separate arrays to reduce padding, plus a tophash byte per slot. Collisions beyond 8 entries in one bucket spilled into overflow buckets chained from the bucket. Growth doubled the bucket count (2^B to 2^(B+1)) when the average load passed about 6.5 entries per bucket or overflow chains grew too long, and entries evacuated incrementally from old buckets to new ones during later operations. Rules of thumb derived from that design (bucket math, overflow chain length, tophash reasoning) do not transfer to the Swiss-table runtime: use group and load-factor reasoning instead.
