# scientist

Scientific research suite with 195 specialized sub-skills.

- Source path: `scientist`
- Version: `v0.6.0`

## v0.6.0 Highlights

- **Shorter root instructions**: Root scientist SKILL is compressed to reduce prompt overhead
- **Process trace logging**: `logs/process-log.jsonl` is required for prompt, skill handoff, and file-write audit trails
- **File-first workflow**: Reports, figures, results, processed data, and logs must be persisted to disk
- **Verification loop**: Root workflow is `PLAN → EXECUTE → VERIFY → REPORT → LOG`
