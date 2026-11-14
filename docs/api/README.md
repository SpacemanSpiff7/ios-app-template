# Apple API grounding

Before using an Apple API not already present in this project, inspect its public signature in the installed SDK
.swiftinterface (or authoritative Apple documentation). Record the signature, availability, SDK/toolchain and
source path/link in a short topic file here when multiple tasks will use it.
Compile a minimal use before distributing interfaces to workers. Report a missing signature rather than guessing.
Refresh or mark the reference superseded when the toolchain changes; bootstrap detects the installed toolchain.
