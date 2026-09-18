# Independence declaration

## Packet received

- Packet ID: `nex1-independent-conformance-packet-v0.1`
- Core version: `NEX-1 Core v0.1`
- Frozen source commit recorded by the packet: `4f9c50aed13cdbdf72c9ce6510521477d49c05a5`
- Uploaded packet ZIP SHA-256 measured in this environment: `7e93ffc3f7fc2fb5e871195e553c9fcbe667bb96c454a2a0270a7e81fdc41b91`
- `PACKET-MANIFEST.generated.json` SHA-256 measured in this environment: `f4d60a54ca73433991fc1250747872b3f65a2395e59ef96904d2248c0df75df0`

The generated packet manifest's per-file SHA-256 values are checked by `python verify.py` before any tests run.

## Materials used

Implementation decisions were based only on files contained in the supplied frozen packet and Python standard-library behavior. No external theoretical source was needed to resolve an NEX-specific rule, so no external theory source was consulted during this implementation.

The user-provided experiment instructions were also available as task instructions; they did not provide reference implementation code or extra NEX semantics beyond directing use of the packet.

## Existing implementation

The existing Go implementation was not searched for, opened, read, or compared. No `reference/go` path was accessed. No GitHub search for NEX implementation code was performed. No other implementation output was used beyond the language-neutral conformance material in the packet.

## Host

- Required target: Python 3.12+
- Python used for verification in this environment: Python 3.13.5
- Dependencies: Python standard library only

## Independent work before checkpoint

Before the independent checkpoint, the following were implemented and tested from the packet: wire codec, resource-separated decoding, closed scope validation, HM rank-1 inference and canonical type observation, all Core primitive schemes, weak call-by-name evaluation, selective forcing, partial primitive application, general recursion through `fix`, and evaluation resource refusal.

No comparison with an existing implementation is permitted before the checkpoint recorded for this project.
