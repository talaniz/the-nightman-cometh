"""Game-specific recovery around the unchanged M2 audition director."""

def retry_audio(director, remaining, paused):
    """Recover the current cue without resetting the game's transformation or pause.

    The audition's retry intentionally resets its own demo state. Gameplay owns
    those states, so use its current timer and retain the existing mixer policy.
    This adapter is the boundary to the director's internal playback entrypoint.
    """
    director.remaining = remaining
    director.paused = paused
    director.elapsed = 0
    director.unlocked = True
    return director._play()

def gameplay_manifest(manifest):
    """Adapt audition metadata for player-controlled game scene progression."""
    return {**manifest, "next": {}}
