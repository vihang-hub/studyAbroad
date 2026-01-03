# Session State Management

This directory tracks implementation progress across Claude Code sessions.

## Files

- `state.json` - Current pipeline state (auto-updated)
- `checkpoints/` - Snapshots at each gate completion
- `logs/` - Execution logs for debugging

## How It Works

1. **Checkpoint on completion**: After each gate passes, state is saved
2. **Resume on primer**: `/primer` reads state and offers to continue
3. **Manual override**: User can restart from any stage

## State Schema

See `state.json` for current progress.
