# Follow-up: bind the reviewed facts independently of mutable collection rows

The original checkpoint04 argument was reviewed against its exact frozen
instruction operands and JRT excerpts. Its constructor helper checked selected
substrings, while the surrounding class/disassembly hashes came from the
collection manifest. Those checks alone would be insufficient as a future
generic coverage exception: added throwing code could retain the checked
substrings. The frozen argument and original coverage-failure reports remain
unchanged.

The separate follow-up verifier fixes the reviewed collector-manifest hash,
installed release hash, all four actual JRT class hashes, and all four complete
`javap` output hashes in its source. It rejects changed evidence independently
of any hashes supplied by the collection rows. Constructor checks first require
the entire pinned disassembly identity. The existing semantic checks then
describe those exact bytes; they do not accept arbitrary new constructor code
that happens to contain familiar fragments.

An explicit synthetic added-throw disassembly preserves the old searched
fragments. The old frozen substring helper accepts it, while the new complete
identity check rejects it. Two separate subprocess controls change the default
constructor disassembly or a JRT class byte and recompute the relevant supplied
row hash. Both are rejected because the independently fixed collector identity
does not match. These are modified proof-input controls. No modified Java class,
original app method, or Android body is executed.

All eleven structural guards reject their deliberately altered inputs. This
includes an additional invocation inside the protected interval and added
constructor throwing code, as well as divisor/receiver/entry/catch/arity
changes. The new report still gives **zero original coverage credit**, retains
the measured 259/262 and three unvisited instructions, and implements no
coverage-accounting policy.

The runtime identity binding here describes the reviewed saved JRT evidence.
A future execution gate must additionally bind the runtime actually used for
that execution, the exact selected original method and proof/checkpoint bytes,
and report the three statically infeasible instructions separately from the 259
dynamically visited instructions. This follow-up is not such a gate and does not
authorize a generic list of ignored offsets.
