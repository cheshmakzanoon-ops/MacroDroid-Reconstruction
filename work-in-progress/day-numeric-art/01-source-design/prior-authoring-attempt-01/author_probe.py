#!/usr/bin/env python3
"""Derive a neutral reflection-only numeric probe from the exact closed case corpus."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat

BASE = Path('/dev/shm/macrodroid-day-numeric-art')
OUT = BASE / 'source-draft-01'
NUMERIC = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-source-promotion-proposal/proposed/project')
PARENT = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest, 'mode': stat.S_IMODE(path.stat().st_mode)}


def block(text, anchor):
    start = text.index(anchor)
    opening = text.index('{', start)
    depth = 0
    for end in range(opening, len(text)):
        if text[end] == '{':
            depth += 1
        elif text[end] == '}':
            depth -= 1
            if depth == 0:
                return text[start:end + 1]
    raise ValueError('Unclosed known source method')


JAVA_START = r'''package recovered.probe;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.Set;

/** Exact numeric input corpus on the real original/candidate APK classes.
 * This neutral probe defines no application or Android class. Reflection builds
 * only private disposable test objects. It installs no app and schedules no alarm.
 * --inventory prints inputs/expectations only and never loads application classes.
 */
public final class DayNumericMethodProbe {
    static final String BASE = "com.arlosoft.macrodroid.variables.VariableValue";
    static final String TARGET = "com.arlosoft.macrodroid.triggers.DayTrigger";
    static final String INVENTORY_SHA256 = "e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79";
    static String name(Object[] input) { return (String) input[0]; }
    static String kind(Object[] input) { return (String) input[1]; }
    static long bits(Object[] input) { return ((Long) input[2]).longValue(); }
    static String text(Object[] input) { return (String) input[3]; }
    static void require(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }
    static String hex(byte[] bytes) {
        StringBuilder value = new StringBuilder();
        for (byte item : bytes) value.append(String.format(Locale.ROOT, "%02x", item & 255));
        return value.toString();
    }
    static String sha(byte[] bytes) {
        try { return hex(MessageDigest.getInstance("SHA-256").digest(bytes)); }
        catch (java.security.NoSuchAlgorithmException error) { throw new AssertionError(error); }
    }
    static String inputJson(Object[] input) {
        String id = name(input), category = kind(input), value = text(input);
        require(id.matches("[a-z0-9.+-]+") && category.matches("[a-z-]+"), "Unexpected literal case name");
        require(value == null || value.matches("[0-9.]*"), "Unexpected numeric-corpus text");
        return "{\"case\":\"" + id + "\",\"kind\":\"" + category
            + "\",\"rawBitsHex\":\"" + String.format(Locale.ROOT, "%016x", bits(input)) + "\""
            + (value == null ? "" : ",\"text\":\"" + value + "\"") + "}";
    }
    static String inputInventorySha256(List<Object[]> inputs) {
        StringBuilder value = new StringBuilder("[");
        for (Object[] input : inputs) {
            if (value.length() != 1) value.append(',');
            value.append(inputJson(input));
        }
        return sha(value.append(']').toString().getBytes(StandardCharsets.UTF_8));
    }
    static String rawMessage(String message) {
        if (message == null) return "null";
        StringBuilder value = new StringBuilder("utf16:");
        for (int i = 0; i < message.length(); i++)
            value.append(String.format(Locale.ROOT, "%04x", (int) message.charAt(i)));
        return value.toString();
    }
'''

JAVA_END = r'''
    static Class<?> ownedType(String name, ClassLoader expected) throws Exception {
        Class<?> value = Class.forName(name);
        require(value.getName().equals(name) && value.getClassLoader() == expected,
                "Application type is not from the same actual APK classpath: " + name);
        return value;
    }
    static Object entry(Object[] input, Class<?> valueType, Class<?> entryType,
                        Class<?> integerType, Class<?> decimalType, Class<?> stringType,
                        Class<?> booleanType, Class<?> dictionaryType) throws Exception {
        if (kind(input).equals("null-entry")) return null;
        Object value;
        String category = kind(input);
        if (category.equals("integer")) {
            value = integerType.getConstructor(long.class, List.class).newInstance(bits(input), null);
            long observed = ((Long) integerType.getMethod("getIntValue").invoke(value)).longValue();
            require(observed == bits(input), "Integer input bits changed: " + name(input));
        } else if (category.equals("decimal")) {
            value = decimalType.getConstructor(double.class, List.class)
                .newInstance(Double.longBitsToDouble(bits(input)), null);
            double observed = ((Double) decimalType.getMethod("getDecimalValue").invoke(value)).doubleValue();
            require(Double.doubleToRawLongBits(observed) == bits(input), "Decimal input bits changed: " + name(input));
        } else if (category.equals("string")) {
            value = stringType.getConstructor(String.class, List.class)
                .newInstance(text(input) == null ? "" : text(input), null);
            if (text(input) == null) {
                // The host corpus includes an otherwise invalid null text field.
                // Set it only in this new disposable object, then read it back.
                Field field = stringType.getDeclaredField("textValue");
                field.setAccessible(true);
                field.set(value, null);
                require(field.get(value) == null, "Explicit null-text fixture was not constructed");
            }
        } else if (category.equals("boolean")) {
            value = booleanType.getConstructor(boolean.class, List.class).newInstance(bits(input) != 0, null);
        } else if (category.equals("dictionary")) {
            value = dictionaryType.getConstructor(List.class, boolean.class, List.class)
                .newInstance(new ArrayList<Object>(), false, null);
        } else if (category.equals("nested-entry")) {
            Object nested = integerType.getConstructor(long.class, List.class).newInstance(bits(input), null);
            value = entryType.getConstructor(String.class, valueType, List.class).newInstance("nested", nested, null);
        } else if (category.equals("null-value")) {
            value = integerType.getConstructor(long.class, List.class).newInstance(0L, null);
        } else throw new IllegalArgumentException(category);
        Constructor<?> constructor = entryType.getConstructor(String.class, valueType, List.class);
        Object result = constructor.newInstance("numeric", value, null);
        if (category.equals("null-value")) {
            // The real constructor rejects null. This deliberately injected
            // heap state tests the already declared null-contained-value case.
            Field field = entryType.getDeclaredField("variable");
            field.setAccessible(true);
            field.set(result, null);
            value = null;
        }
        require(entryType.getMethod("getVariable").invoke(result) == value,
                "Exact contained input identity differs: " + name(input));
        return result;
    }
    public static void main(String[] args) throws Exception {
        List<Object[]> inputs = cases();
        if (args.length == 1 && args[0].equals("--inventory")) {
            System.out.println("DAY_NUMERIC_INPUTS_BEGIN\tcases=1291\tsha256=" + INVENTORY_SHA256);
            for (Object[] input : inputs)
                System.out.println(inputJson(input) + "\t" + (expected(input) == null
                    ? "exception:java.lang.NullPointerException" : "value:" + expected(input)));
            System.out.println("DAY_NUMERIC_INPUTS_END\tcases=1291\tandroid_executed=false");
            return;
        }
        require(args.length == 0, "No runtime argument or case selection is allowed");
        Class<?> target = Class.forName(TARGET);
        ClassLoader loader = target.getClassLoader();
        require(loader != null, "Application class must not be a bootstrap substitute");
        Class<?> valueType = ownedType(BASE, loader), entryType = ownedType(BASE + "$DictionaryEntry", loader),
            integerType = ownedType(BASE + "$IntegerValue", loader), decimalType = ownedType(BASE + "$DecimalValue", loader),
            stringType = ownedType(BASE + "$StringValue", loader), booleanType = ownedType(BASE + "$BooleanValue", loader),
            dictionaryType = ownedType(BASE + "$Dictionary", loader);
        Method method = target.getDeclaredMethod("r0", entryType);
        require(method.getDeclaringClass() == target && Modifier.isStatic(method.getModifiers())
                && Modifier.isPublic(method.getModifiers()) && method.getReturnType() == int.class,
                "The exact public static r0(DictionaryEntry):int method is required");
        System.out.println("DAY_NUMERIC_ART_BEGIN\tcases=1291\tsha256=" + INVENTORY_SHA256);
        int index = 0;
        for (Object[] input : inputs) {
            Object argument = entry(input, valueType, entryType, integerType, decimalType, stringType, booleanType, dictionaryType);
            String prefix = "DAY_NUMERIC_ART_CASE\t" + index + "\t" + name(input) + "\t" + kind(input)
                + "\t" + String.format(Locale.ROOT, "%016x", bits(input));
            try {
                Object observed = method.invoke(null, argument);
                require(observed instanceof Integer && expected(input) != null
                        && expected(input).equals(observed), "Numeric value mismatch: " + name(input));
                System.out.println(prefix + "\tvalue\t" + observed);
            } catch (InvocationTargetException wrapper) {
                Throwable cause = wrapper.getCause();
                require(kind(input).equals("null-entry") && cause != null
                        && cause.getClass() == NullPointerException.class,
                        "Unexpected target exception: " + name(input) + " " + cause);
                System.out.println(prefix + "\texception\t" + cause.getClass().getName() + "\t" + rawMessage(cause.getMessage()));
            }
            index++;
        }
        require(index == 1291, "Incomplete input corpus");
        System.out.println("DAY_NUMERIC_ART_END\tcases=1291\tpassed=true");
    }
}
'''


def main():
    cases_file = NUMERIC / 'tests/java/DayTriggerParityCases.java'
    assert identity(cases_file)['sha256'] == '1712210dae22e29b04c3be05f5c39b06839ae042ea1b35be799203987b8a09d7'
    text = cases_file.read_text()
    expected = block(text, '    static Integer expected(Input input)')
    expected = expected.replace('expected(Input input)', 'expected(Object[] input)').replace('input.kind()', 'kind(input)').replace('input.bits()', 'bits(input)')
    cases = block(text, '    static List<Input> cases()')
    cases = cases.replace('List<Input>', 'List<Object[]>')
    cases, count = re.subn(r'new Input\((.+)\)\);', r'new Object[]{\1});', cases)
    assert count == 19, count
    anchor = '        require(out.stream().map(Input::name).distinct().count() == out.size(), "Duplicate case identifiers");'
    assert cases.count(anchor) == 1
    cases = cases.replace(anchor, '        Set<String> names = new HashSet<String>();\n        for (Object[] input : out) require(names.add(name(input)), "Duplicate case identifiers");')
    cases = cases.replace('INPUT_INVENTORY_SHA256', 'INVENTORY_SHA256')
    assert 'Input::' not in cases and 'new Input' not in cases
    OUT.mkdir(exist_ok=False)
    shutil.copyfile(__file__, OUT / 'author_probe.py')
    source = OUT / 'source/recovered/probe/DayNumericMethodProbe.java'
    source.parent.mkdir(parents=True)
    source.write_text(JAVA_START + '\n' + expected + '\n\n' + cases + '\n' + JAVA_END)
    copied = []
    def copy(path, relative):
        before = identity(path)
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        assert identity(path) == before and {k:identity(target)[k] for k in ('bytes','sha256')} == {k:before[k] for k in ('bytes','sha256')}
        copied.append({'source': str(path), 'copy': relative, **before})
    copy(cases_file, 'inputs/DayTriggerParityCases.java')
    for name in ('source/ui-methods.json', 'source/java/recovered/ui/DayTriggerValueMethods.java', 'tests/fixtures/original-dependencies.json', 'tests/fixtures/provenance.json'):
        copy(NUMERIC / name, 'inputs/numeric-source/' + name)
    snapshot_path = PARENT / 'reports/release-input-snapshot.json'
    snapshot = json.loads(snapshot_path.read_bytes())
    assert identity(snapshot_path)['sha256'] == 'ca3bed290f18a378c7a3d6cc70d924c8d6ec85481e236b4e7561c31fedafdfbe'
    recorded = {row['path']: row for row in snapshot['entries']}
    selections = []
    patterns = ['DayTrigger_*.smali', 'VariableValue_*.smali', 'VariableValue$DictionaryEntry_*.smali',
        'VariableValue$IntegerValue_*.smali', 'VariableValue$DecimalValue_*.smali', 'VariableValue$StringValue_*.smali',
        'VariableValue$BooleanValue_*.smali', 'VariableValue$Dictionary_*.smali', 'Trigger_*.smali', 'SelectableItem_*.smali']
    for pattern in patterns:
        matches = list((PARENT / 'source/smali/classes3').glob('*/' + pattern)); assert len(matches) == 1
        path = matches[0]; relative = path.relative_to(PARENT).as_posix()
        actual = identity(path)
        assert {k: actual[k] for k in ('bytes', 'sha256')} == {k: recorded[relative][k] for k in ('bytes', 'sha256')}
        copy(path, 'inputs/original-smali/' + path.name)
        selections.append(recorded[relative])
    (OUT / 'baseline-source-rows.json').write_text(json.dumps(selections, indent=2) + '\n')
    (OUT / 'input-identities.json').write_text(json.dumps(copied, indent=2) + '\n')
    protocol = {'schema': 1, 'status': 'INACTIVE_SOURCE_DRAFT_NOT_COMPILED_OR_RUN',
        'target': 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I',
        'original_method_sha256': '8383c90ebe3d35afa63d52cf92cd4c92b54ed4525ca0d8a31a29fe603f9eef21',
        'cases': 1291, 'input_inventory_sha256': 'e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79',
        'original_apk': {'bytes': 95725918, 'sha256': '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'},
        'candidate_apk': {'bytes': 94683136, 'sha256': '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'},
        'class_definition_allowlist': ['Lrecovered/probe/DayNumericMethodProbe;'],
        'direct_type_reference_families': ['java', 'probe class', 'compiler metadata annotations'],
        'constructor_invalid_states_injected_into_disposable_objects': ['null-value', 'string-null'],
        'exception_message_comparison_exception': 'Only null-entry compares exact exception class; the complete raw message is retained as lossless UTF-16 hexadecimal.',
        'separate_guest_processes': ['original', 'candidate'], 'guest_timeout_seconds': 120,
        'verification_mode': '-Xverify:all', 'full_input_inventory_required_each_run': True,
        'android_executed': False, 'application_build_executed': False, 'probe_compiled': False,
        'app_installed': False, 'app_ui_interaction': False, 'alarms_scheduled': False,
        'full_runtime_1_to_1_established': False, 'new_recovered_method_credit': 0}
    (OUT / 'protocol.json').write_text(json.dumps(protocol, indent=2) + '\n')
    (OUT / 'README.md').write_text('''# Direct numeric ART probe source draft

This inactive draft prepares a direct AndroidRuntime check of the exact numeric method already accepted on the host. It has not been compiled, executed on Android, or activated. Its eventual two separate guest processes will load the exact original and numeric candidate APKs, define only the neutral probe class, and invoke the real public static `DayTrigger.r0(DictionaryEntry):int` through reflection. No application or Android stubs belong on that classpath.

The 1,291 inputs preserve the complete existing corpus and its fixed compact-JSON digest. Integer expectations use modular signed arithmetic. Decimal expectations use integer-only IEEE-754 decomposition, including truncation, saturation, infinities and NaNs. These expectation and case methods are mechanically adapted from the exact closed numeric host source; the recovered numeric implementation is never substituted for the real target.

Real application constructors build the argument graph. The real entry and string constructors reject null fields, while the existing host corpus explicitly includes `null-value` and `string-null`. Those two cases therefore create valid private test objects and inject only the declared null field, then read it back. They measure those deliberately injected heap states, not constructor acceptance or ordinary UI reachability. Every integer/decimal getter is observed before the target call to require the exact input bits. Every contained object identity is checked.

Only the declared null-entry case accepts an exact `java.lang.NullPointerException` class. Its complete message is preserved losslessly as UTF-16 hexadecimal and is not required to match compiler-dependent wording. All other unexpected exceptions fail. The output preserves every case, value and exception in fixed order, with no case selection or retry mode. The inventory-only host mode does not load application classes and makes no Android claim.

The intended runner derives from the previously reviewed bounded app_process probe, retaining exact APK and DEX hashes, the fixed disposable AVD identity, enabled verification, separate original/candidate processes, complete raw streams and owned-file cleanup. That runner and workflow remain to be authored and validated. This draft changes no active source, workflow, APK, setting, installed app or alarm. Full runtime parity remains unestablished.
''')
    rows = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint = {'schema': 1, 'status': protocol['status'], 'created_utc': datetime.now(timezone.utc).isoformat(),
        'repo_target': 'work-in-progress/day-numeric-art/01-source-design', 'active_files': [],
        'android_executed': False, 'application_build_executed': False, 'probe_compiled': False, 'files': rows}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'source': identity(source), 'payloads': len(rows)}, indent=2))


if __name__ == '__main__':
    main()
