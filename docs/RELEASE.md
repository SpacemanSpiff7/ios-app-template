# Release and device evidence

## Before an archive

- Run scripts/test-gate.sh; retain its structured xcresult, source identity and verification manifest.
- Analyze and smoke-launch the same source. Inspect normal/AX3, light/dark.
- Set version/build, usage descriptions and entitlements in project.yml; regenerate.
- Inspect the built app and every extension: identifier, display name, versions and UIDeviceFamily.
- Match capabilities, privacy manifest and App Privacy declarations to visible behavior.
- Prepare current screenshots, reviewer instructions and applicable purchase-sandbox evidence.

## Exact source and artifact

scripts/device.sh build creates a signed artifact manifest with commit (when present), dirty paths, source digest,
app-tree digest, bundle/build identifiers and signature verification. Install refuses changed source or artifact.
Install and launch create separate evidence tied to that build manifest. A subsequent source patch requires a new
build and install. Record the manifest link in STATUS; include dirty state rather than claiming a clean commit.
A build, install or normal launch does not prove a camera flow, VoiceOver, haptic, purchase or service request.

## Gates

| Gate | Required evidence | Status | Dated evidence |
|---|---|---|---|
| Signing/capabilities | Approved team/ids/capabilities and successful signed build | open | |
| App Store Connect | Listing, privacy, age rating, availability and agreements | open | |
| Physical interaction | Primary task, keyboard, discard, interruptions, VoiceOver, AX3/dark | open | |
| System integrations | Actual camera, permissions, haptics, widgets/background work used by this app | open | |
| Purchases if present | Exact build's successful physical-device/TestFlight sandbox purchase | open | |
| Submission | Explicitly authorized upload/submission and recorded outcome | open | |

Keep unavailable gates open while completing independent repository work. Use observed tool/device evidence or
request the missing human-only step; do not repeat an approval already given. Upload/submission needs authorization.

## Review history

| Date | Version/build/source | Outcome | Guideline | Fix |
|---|---|---|---|---|
