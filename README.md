# AI-Assisted Multi-Camera Kindergarten Graduation Video Editing Pipeline

## Project Overview
This is a semi-automated 4-camera video editing pipeline designed for kindergarten graduation ceremonies. It utilizes Python and MoviePy to reduce teacher workload by programmatically synchronizing, cutting, and rendering footage based on a CSV-formatted Editing Decision List (EDL).

## Pipeline Workflow
1. **Synchronization:** Manual clap synchronization is implemented via `sync_offset` variables.
2. **EDL Generation:** A `edl.csv` file defines the start/end times, camera angles, transitions, and overlay text.
3. **Human Review:** The CSV format allows teachers to easily review and adjust camera selections offline before rendering.
4. **Rendering:** `main.py` parses the EDL, applies the time offsets, overlays titles/subtitles, applies transitions, and exports the final MP4.

## Folder Structure
```text
project/
│
├── starter-pack/
│   ├── camera1_front_left.mp4
│   ├── camera2_front_right.mp4
│   ├── camera3_wide_back.mp4
│   └── camera4_side_angle.mp4
│
├── main.py
├── edl.csv
└── README.md