# Prepared independent readiness artifact replay

This tool is prepared for the exact workflow 56808b33, activated at e1ade015f938339479216a1a91518e556902fce8. Its Python syntax has been parsed. It has not yet replayed the new Android artifact, and this checkpoint does not claim a device or analysis result.

The caller supplies the actual run and artifact IDs, complete downloaded ZIP hash, raw extraction, exact reference/candidate APK paths, and a fresh output directory. The tool rehashes every ZIP member and raw file; reconstructs all 252 prepared roles; replays both complete recorded comparison objects; checks raw readiness, full-frame captures and hosted test logs; and records full RGBA pixel counts for every available pair. It runs no Android command. Raw evidence and APK hashes are checked after the private replay. A failed or incomplete device result remains a failed or incomplete result even when its independent analysis reproduces it exactly.
