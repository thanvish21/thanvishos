# Configuration for ThanvishOS

This file documents the configurable root paths used by the system. All values are optional – if a path is `null` the system will treat it as **UNKNOWN** and skip related processing.

| Setting | Description | Expected type | Default |
|---|---|---|---|
| `COLLEGE_ROOT` | Root directory containing academic timetables, notes, and exam resources. | String (absolute path) | `null` |
| `PROJECTS_ROOT` | Directory that holds all personal and external project folders. | String (absolute path) | `null` |
| `GITHUB_ROOT` | Path where cloned GitHub repositories reside (used by the Open‑Source Engine). | String (absolute path) | `null` |
| `NOTES_ROOT` | Root of the `hyperresearch` knowledge vault (markdown notes). | String (absolute path) | `null` |
| `DOCUMENTS_ROOT` | General personal documents (PDFs, Word files, etc.). | String (absolute path) | `null` |
| `WHATSAPP_EXPORT_ROOT` | Folder containing exported WhatsApp chat archives. | String (absolute path) | `null` |
| `HERMES_ROOT` | Directory with Hermes‑generated data feeds. | String (absolute path) | `null` |

## Usage

The JSON version of this configuration lives at `ThanvishOS/config.json`. The system loads the JSON at runtime, validates each entry, and exposes a Python dictionary via `thanvish.config.load()`.

When a path is set to `null` the corresponding engine will report **UNKNOWN** and ignore that data source until the user provides a valid directory.
