"""Retry XML acquisition failures without relaxing screen or freshness checks."""
from __future__ import annotations
import json
import time
import xml.etree.ElementTree as ET
import editor_journey as runner


class EvidenceRecorder(runner.Recorder):
    def snapshot(self, label, owner):
        # The base recorder retains every command, raw XML, screenshot and PID.
        # A failed acquisition is never substituted for a valid capture.
        for attempt in range(1, 4):
            name = f'{label}-acquisition-{attempt}'
            try:
                return super().snapshot(name, owner)
            except ET.ParseError as error:
                self.save(name + '-acquisition-error.json', json.dumps({
                    'status': 'INVALID_UI_XML', 'attempt': attempt,
                    'reason': str(error), 'accepted_as_evidence': False,
                }, indent=2).encode())
                if attempt == 3:
                    raise runner.JourneyError('UI XML acquisition failed after three fresh attempts') from error
                time.sleep(0.5)
        raise AssertionError('Unreachable acquisition state')
