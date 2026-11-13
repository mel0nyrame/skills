# Attribution and licensing

## Upstream skill

This directory contains a modified version of Matt Pocock's `wait-what` skill.

- Repository: <https://github.com/mattpocock/skills>
- Reference revision: `d80fa0f4ebe0c5714af0adf8670336065233ecc6`
- Original skill: <https://github.com/mattpocock/skills/blob/main/skills/productivity/wait-what/SKILL.md>
- Original UI metadata: <https://github.com/mattpocock/skills/blob/main/skills/productivity/wait-what/agents/openai.yaml>
- Upstream license: <https://github.com/mattpocock/skills/blob/main/LICENSE>
- Copyright (c) 2026 Matt Pocock.

The adaptation is based on the upstream skill and UI metadata at the reference revision above. The upstream MIT license is reproduced in [LICENSE](LICENSE). This skill adaptation is also distributed under that license. Preserve the copyright and full license text when copying or redistributing it; keep this notice with the adaptation to preserve its provenance.

### Modifications

- Retained the short, conversational re-pitch prompt and organized the guidance into core recovery actions and communication principles.
- Replaced the direct ASD-STE100 instruction with self-contained guidance on clarity, explicit logic, consistent terminology, structured delivery, and facts versus assumptions.
- Used the user's current language instead of requiring English.
- Removed the requirement to find `GLOSSARY.md` or `GLOSSARY-MAP.md`.
- Preserved the skill name and manual-only invocation settings. Kept upstream UI metadata unchanged, including the absence of `interface.default_prompt`.

This is an independent adaptation, not an official upstream release. No endorsement by Matt Pocock is implied.

## ASD-STE100 reference

ASD-STE100 Simplified Technical English is owned by the Aerospace, Security and Defence Industries Association of Europe (ASD). Its name is a registered trademark of ASD. The standard has its own copyright and usage terms; it is not covered by this directory's MIT license.

Official background and guidance:

- [About STE](https://asd-ste100.org/about_STE.html)
- [STE FAQ](https://asd-ste100.org/STE_faq.html)

The adaptation draws on general clarity principles associated with ASD-STE100; the skill does not require readers or agents to consult the standard. It does not bundle the standard, reproduce its controlled dictionary or rule text, or provide a translation of the standard. It does not claim full compliance with ASD-STE100, certification, or endorsement by ASD or its Simplified Technical English Maintenance Group. Consult the official sources for the standard itself and its usage terms.
