#!/usr/bin/env python3
"""Author explicit one-body faults against the immutable narrowed-observer baseline."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
HELPER_SHA = '67f5a47013ffbffa67859f9103d2034b3225521d10be9d96d65acd31599d45ee'
BASELINE_SHA = '06986104338d570dd78e4abf34f2691756f772c8f6e521769a9ebf06ea97edbe'


def main():
    root = HERE / 'checkpoints/07-cast-source-original-jvm-coverage-gap'
    source = (root / 'source/java/recovered/ui/VideoMonitorMethods.java').read_text()
    if hashlib.sha256(source.encode()).hexdigest() != HELPER_SHA or hashlib.sha256((root / 'checkpoint.json').read_bytes()).hexdigest() != BASELINE_SHA:
        raise RuntimeError('Frozen catalog baseline differs')
    controls = []
    def add(name, reason, find, replace, label, count=1, extra=()):
        edits = [{'find': find, 'replace': replace, 'count': count}] + list(extra)
        candidate = source
        for edit in edits:
            if candidate.count(edit['find']) != edit['count']:
                raise RuntimeError('Unexpected anchor count for ' + name + ': ' + repr(edit['find']))
            candidate = candidate.replace(edit['find'], edit['replace'])
        if candidate == source:
            raise RuntimeError('No actual mutation for ' + name)
        controls.append({'name': name, 'reason': reason, 'edits': edits, 'expected_failure_labels': [label]})

    add('initial-delay-duration', 'Initial suspension delay is exactly 5000ms.',
        'sz6.s(5000L, self)', 'sz6.s(4000L, self)', 'video-entry:0:false:0')
    add('initial-label-before-delay', 'The continuation is label1 before the first delay boundary.',
        'self.label = 1;', 'self.label = 2;', 'video-inactive-label:0')
    add('initial-result-validation', 'Initial failure result must escape before changing state or delaying.',
        'if (label == 0) {\n            u2f.P(result);', 'if (label == 0) {', 'video-entry:0:false:3')
    add('label-one-result-validation', 'Label1 validates its result outside the monitor catch.',
        '} else if (label == 1) {\n            u2f.P(result);', '} else if (label == 1) {', 'video-entry:1:false:3')
    add('label-three-result-validation', 'Label3 validates its result outside the monitor catch.',
        '} else if (label == 3) {\n            u2f.P(result);', '} else if (label == 3) {', 'video-entry:3:false:3')
    add('retain-dead-file-cast', 'Label2 retains the otherwise unused saved File cast.',
        '            File ignoredFile = (File) self.L$1;\n', '', 'video-dead-casts:0:2')
    add('retain-dead-flag-cast', 'Label2 retains the otherwise unused saved qnc cast.',
        '            qnc ignoredFlag = (qnc) self.L$0;\n', '', 'video-dead-casts:2:0')
    add('dead-cast-order', 'Distinct malformed source types expose File-before-qnc order.',
        '            File ignoredFile = (File) self.L$1;\n            qnc ignoredFlag = (qnc) self.L$0;',
        '            qnc ignoredFlag = (qnc) self.L$0;\n            File ignoredFile = (File) self.L$1;', 'video-dead-casts:2:2')
    add('label-two-result-validation', 'A stopped-operation failure must enter its original error/retry path.',
        '            try {\n                u2f.P(result);\n                return unit;',
        '            try {\n                return unit;', 'video-label-two-resume-failure:3')
    add('label-two-catches-exception-only', 'Error from a label2 resumed result escapes.',
        '                return unit;\n            } catch (Exception failure) {',
        '                return unit;\n            } catch (Throwable failure) {', 'video-label-two-resume-failure:4')
    add('invalid-label-defensive-return', 'The injected returning guard follows the exact defensive null return.',
        'e6d.r("call to \'resume\' before \'invoke\' with coroutine");\n            return null;',
        'e6d.r("call to \'resume\' before \'invoke\' with coroutine");\n            return unit;', 'video-invalid-guard-returns-injected')
    add('companion-read-before-recording', 'The companion getClass check occurs before reading the recording flag.',
        '            BaseVideoRecordingService.A.getClass();\n', '', 'video-companion-before-recording:false')
    add('inactive-unit-identity', 'An inactive recording returns the captured Unit identity.',
        'if (!BaseVideoRecordingService.B) return unit;', 'if (!BaseVideoRecordingService.B) return null;', 'video-inactive-label:1')
    add('recording-parent-directory-read', 'The existing file parent must be consulted before fallback.',
        'if (directory != null) directory = directory.getParentFile();',
        'if (directory != null) directory = null;', 'video-profile:0:1')
    add('movies-directory-argument', 'Fallback forwards the actual Environment movies constant.',
        'String movies = Environment.DIRECTORY_MOVIES;', 'String movies = null;', 'video-profile:3:1')
    add('captured-storage-owner-read', 'A successful c call keeps its captured owner for x reads.',
        'long previousAvailable = storageOwner.x;', 'long previousAvailable = self.this$0.x;', 'video-captured-storage-owner-survives-field-null')
    add('captured-storage-owner-write', 'The x write uses the captured storage owner after owner-field mutation.',
        'storageOwner.x = available;', 'self.this$0.x = available;', 'video-captured-storage-owner-survives-field-null')
    add('storage-state-before-info-log', 'Availability state changes before the logger can observe or throw.',
        '                        storageOwner.x = available;\n', '', 'video-profile:0:1', extra=[{
            'find': '                        kjf.q(storageOwner.s, text);',
            'replace': '                        kjf.q(storageOwner.s, text);\n                        storageOwner.x = available;', 'count': 1}])
    add('strict-storage-report-threshold', 'Equality at a 100MiB reduction must not emit a fresh availability report.',
        'available < previousAvailable - 104857600L', 'available <= previousAvailable - 104857600L', 'video-exact-storage-report-threshold:0')
    add('storage-report-interval', 'The report interval is 100MiB, not 1MiB.',
        'available < previousAvailable - 104857600L', 'available < previousAvailable - 1048576L', 'video-exact-storage-report-threshold:0')
    add('zero-prior-storage-reports', 'An initial zero availability value enters the reporting branch.',
        'previousAvailable <= 0L', 'previousAvailable < 0L', 'video-profile:0:1')
    add('strict-critical-storage-threshold', 'Exactly 128MiB is outside the critical-storage condition.',
        'available < 134217728L', 'available <= 134217728L', 'video-space:134217728:0')
    add('storage-megabyte-log-units', 'Available and critical storage text uses division by 1048576.',
        'available / 1048576L', 'available / 1024L', 'video-profile:0:1', 2)
    add('captured-storage-log-identifier', 'The storage log identifier belongs to the captured owner.',
        'kjf.q(storageOwner.s, text);', 'kjf.q(self.this$0.s, text);', 'video-captured-storage-owner-survives-field-null')
    add('missing-file-does-not-read-length', 'A missing file produces size zero without a length call.',
        '                                size = 0L;\n                            }\n                        } else',
        '                                size = file.length();\n                            }\n                        } else', 'video-profile:6:1')
    add('file-reread-after-exists', 'The file field is read again after exists returns.',
        'file = fileOwner.t;\n                                file.getClass();',
        'file = file;\n                                file.getClass();', 'video-file-length-rereads-captured-owner-file')
    add('descriptor-size-sentinel', 'A non-null file descriptor without File yields the negative sentinel.',
        'size = fileOwner.u != null ? -1L : 0L;', 'size = fileOwner.u != null ? 0L : 0L;', 'video-profile:4:1')
    add('file-size-catches-exception-only', 'An Error during File access escapes the inner Exception catch.',
        '                    } catch (Exception failure) {', '                    } catch (Throwable failure) {', 'video-fault:0:4:1')
    add('file-error-fallback-zero', 'A caught File-size Exception resumes with size zero.',
        '                        size = 0L;\n                    }\n\n                    if (size >= 0L)',
        '                        size = -1L;\n                    }\n\n                    if (size >= 0L)', 'video-profile:7:1')
    add('zero-file-size-is-processed', 'Zero size still logs and updates the monitoring state.',
        'if (size >= 0L)', 'if (size > 0L)', 'video-numeric-contract:2')
    add('file-kilobyte-log-units', 'Current file size uses binary kilobytes.',
        'size / 1024L', 'size / 1000L', 'video-size:1023:0:0')
    add('strict-positive-previous-size', 'The prior-size branch requires a strictly positive value.',
        'previousSize > 0L', 'previousSize >= 0L', 'video-numeric-contract:2')
    add('growth-subtraction-direction', 'Growth subtracts previous size from current size.',
        'long growth = size - previousSize;', 'long growth = previousSize - size;', 'video-numeric-contract:4')
    add('equal-size-is-stalled', 'A zero growth value increments the stalled counter.',
        'growth <= 0L', 'growth < 0L', 'video-numeric-contract:5')
    add('stall-counter-wraps-as-int', 'Integer.MAX_VALUE increments with signed int wraparound.',
        'int checks = previousOwner.w + 1;', 'int checks = previousOwner.w == Integer.MAX_VALUE ? Integer.MAX_VALUE : previousOwner.w + 1;', 'video-numeric-contract:8')
    add('stall-counter-increments-once', 'Each stopped-growth check increments by exactly one.',
        'int checks = previousOwner.w + 1;', 'int checks = previousOwner.w + 2;', 'video-numeric-contract:5')
    add('third-stalled-check-stops', 'The critical stalled threshold includes check three.',
        'checks >= 3', 'checks > 3', 'video-numeric-contract:6')
    add('stall-counter-owner-reread', 'The post-log counter comes from a fresh owner-field read.',
        'checks = self.this$0.w;', 'checks = previousOwner.w;', 'video-mutation:2:7:0')
    add('stall-seconds-wide-multiply', 'Counter-to-seconds multiplication remains long before arithmetic.',
        '(long) checks * 3000L / 1000L', '(long) (checks * 3000) / 1000L', 'video-counter-seconds-remain-long')
    add('growth-resets-stall-counter', 'Positive growth resets the captured counter to zero.',
        'previousOwner.w = 0;', 'previousOwner.w = 1;', 'video-numeric-contract:4')
    add('growth-kilobyte-log-units', 'Growth text uses binary kilobytes too.',
        'growth / 1024L', 'growth / 1000L', 'video-size:1024:1:0')
    add('final-size-owner-reread', 'The final previous-size write uses a freshly read owner.',
        'self.this$0.v = size;', 'previousOwner.v = size;', 'video-mutation:0:7:0')
    add('stop-callback-captures-owner', 'The stop callback captures the current owner.',
        'new d31(self.this$0, null)', 'new d31(null, null)', 'video-profile:1:1')
    add('stop-callback-null-completion', 'The stop callback constructor has null completion.',
        'new d31(self.this$0, null)', 'new d31(self.this$0, self)', 'video-profile:1:1')
    add('stop-dispatcher-identity', 'Dispatch uses at9.a after the preserved discarded dispatcher read.',
        'm47 dispatcher = at9.a;', 'defpackage.i93 dispatcher = zp4.a;', 'video-profile:1:1')
    add('clear-saved-flag-before-suspension', 'L0 is cleared at every preserved suspension preparation.',
        'self.L$0 = null;', '', 'video-dispatch-result:0', 3)
    add('clear-saved-file-before-suspension', 'L1 is cleared at every preserved suspension preparation.',
        'self.L$1 = null;', '', 'video-dispatch-result:0', 3)
    add('stop-resume-label', 'Stop dispatch stores label2.',
        'self.label = 2;', 'self.label = 3;', 'video-profile:1:1')
    add('repeat-delay-duration', 'Both retry-delay sites use exactly 3000ms.',
        'sz6.s(3000L, self)', 'sz6.s(1000L, self)', 'video-profile:0:1', 2)
    add('repeat-resume-label', 'Both repeated-delay sites store label3.',
        'self.label = 3;', 'self.label = 1;', 'video-profile:0:1', 2)
    add('delay-marker-reference-identity', 'An equals-only marker lookalike must not count as suspended.',
        'delayed == suspended', 'java.util.Objects.equals(delayed, suspended)', 'video-delay-result:0:5', 3)
    add('dispatch-marker-reference-identity', 'Stop dispatch also compares the suspension marker by identity.',
        'stopped == suspended', 'java.util.Objects.equals(stopped, suspended)', 'video-dispatch-result:5')
    add('monitor-catches-exception-only', 'Error during storage monitoring escapes the outer catch.',
        '                }\n            } catch (Exception failure) {\n                String message',
        '                }\n            } catch (Throwable failure) {\n                String message', 'video-fault:0:2:1')
    add('outer-error-logger-escapes', 'The error logger is not protected by another swallowing catch.',
        'kjf.g(self.this$0.s, text);', 'try { kjf.g(self.this$0.s, text); } catch (Exception ignored) { }', 'video-outer-logger-escapes-after-inner:0', 3)
    add('exception-message-read-once', 'Each catch reads Throwable.getMessage once before concatenation.',
        'String message = ((Throwable) failure).getMessage();',
        'String message = ((Throwable) failure).getMessage(); ((Throwable) failure).getMessage();', 'video-profile:7:1', 3)
    add('callback-before-stop-state-preparation', 'The callback constructor observes the old continuation state.',
        '                    self.label = 2;\n', '', 'video-profile:1:1', extra=[{
            'find': '                    d31 callback = new d31(self.this$0, null);',
            'replace': '                    self.label = 2;\n                    d31 callback = new d31(self.this$0, null);', 'count': 1}])
    add('critical-conditions-dispatch-stop', 'Both critical conditions set the stop flag.',
        'stop = true;', 'stop = false;', 'video-profile:1:1', 2)

    value = {'method': 'Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;',
        'helper_sha256': HELPER_SHA, 'baseline_checkpoint_sha256': BASELINE_SHA,
        'baseline_study_directory': 'original-jvm-07-cast-source', 'expected_cases': 1118,
        'expected_independent_checks': 230, 'scope': 'Actual compiled one-body faults only; unchanged baseline raw coverage remains failed.',
        'controls': controls}
    target = HERE / 'video_method_mutants.json'
    if target.exists():
        raise FileExistsError(target)
    target.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'path': str(target), 'controls': len(controls), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
