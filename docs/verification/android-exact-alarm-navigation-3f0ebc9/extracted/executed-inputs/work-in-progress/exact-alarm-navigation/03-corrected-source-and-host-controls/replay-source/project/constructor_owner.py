#!/usr/bin/env python3
"""Restore explicitly pinned original superclass constructor owners in DEX bodies.

This deliberately supports a narrow straight-line allocation shape: a new-instance,
optional numeric constants that do not overwrite its receiver, then invoke-direct.
It never adds a constructor or changes an allocation type. Unknown shapes fail.
The transformation is bounded source evidence, not an ART verification result.
"""
from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from pathlib import Path


class ConstructorOwnerError(ValueError):
    pass


CLASS = r'L[A-Za-z0-9_$/]+;'
REGISTER = r'[vp][0-9]+'
NEW = re.compile(r'new-instance\s+(' + REGISTER + r'),\s*(' + CLASS + r')$')
CALL = re.compile(r'(invoke-\S+)\s+\{([^}]*)\},\s*(' + CLASS + r')->(<init>\([^)]*\)V)$')
CONST = re.compile(r'(const(?:/4|/16|/high16)?|const-wide(?:/16|/32|/high16)?)\s+(' + REGISTER + r'),\s*[-+]?0x[0-9a-fA-F]+[Ll]?$')
METHOD = re.compile(r'^[ \t]*\.method[ \t]+([^\n]*?)[ \t]+(\S+)[ \t]*$', re.M)
PARAMETER = re.compile(r'\[*[ZBSCIJFD]|\[*L[^;\s]+;')


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def words(constructor: str) -> int:
    if not constructor.startswith('<init>(') or not constructor.endswith(')V'):
        raise ConstructorOwnerError('Expected a void constructor descriptor')
    arguments = constructor[len('<init>('):-2]
    tokens = PARAMETER.findall(arguments)
    if ''.join(tokens) != arguments:
        raise ConstructorOwnerError('Invalid constructor parameter descriptor')
    return 1 + sum(2 if token in ('J', 'D') else 1 for token in tokens)


def declaration(text: str, expected: str) -> tuple[str | None, dict[str, frozenset[str]], frozenset[str]]:
    header = re.search(r'^[ \t]*\.class[ \t]+([^\n]+)$', text, re.M)
    if header is None or header[1].split()[-1] != expected:
        raise ConstructorOwnerError('Preserved class declaration does not match its identity')
    parent = re.search(r'^[ \t]*\.super[ \t]+(' + CLASS + r')[ \t]*$', text, re.M)
    declarations = METHOD.findall(text)
    methods = {signature: frozenset(flags.split()) for flags, signature in declarations}
    if len(methods) != len(declarations):
        raise ConstructorOwnerError('Duplicate preserved method declaration')
    return parent[1] if parent else None, methods, frozenset(header[1].split()[:-1])


def code_lines(text: str) -> list[tuple[int, str]]:
    result = []
    for index, raw in enumerate(text.splitlines(keepends=True)):
        line = raw.strip()
        if not line or line.startswith('#') or line.startswith(('.line ', '.local ', '.end local', '.restart local')):
            continue
        # Labels, catch boundaries and every unrecognized directive are barriers.
        result.append((index, line))
    return result


def matching_calls(text: str, allocated: str, owner: str, constructor: str) -> list[int]:
    headers = METHOD.findall(text)
    if len(headers) != 1:
        raise ConstructorOwnerError('Constructor mapping requires one complete method')
    flags, signature = headers[0]
    start, end = signature.find('('), signature.find(')')
    if start < 0 or end < start:
        raise ConstructorOwnerError('Invalid enclosing method descriptor')
    parameters = words('<init>' + signature[start:end + 1] + 'V') - 1 + ('static' not in flags.split())
    layouts = re.findall(r'^[ \t]*\.(locals|registers)[ \t]+([0-9]+)[ \t]*$', text, re.M)
    if len(layouts) != 1:
        raise ConstructorOwnerError('One explicit method register layout is required')
    kind, amount = layouts[0]
    total = int(amount) + parameters if kind == 'locals' else int(amount)
    base = total - parameters
    if base < 0:
        raise ConstructorOwnerError('Method has fewer registers than parameter words')
    def physical(register: str) -> int:
        index = int(register[1:])
        if register[0] == 'p':
            if index >= parameters:
                raise ConstructorOwnerError('Parameter register is outside the method layout')
            index += base
        if index >= total:
            raise ConstructorOwnerError('Register is outside the method layout')
        return index
    lines = code_lines(text)
    found = []
    for index, (raw_index, line) in enumerate(lines):
        call = CALL.fullmatch(line)
        if call is None or call.groups()[2:] != (owner, constructor):
            continue
        if call[1] != 'invoke-direct':
            raise ConstructorOwnerError('Only non-range direct constructor calls are supported')
        registers = [value.strip() for value in call[2].split(',')]
        if len(registers) != words(constructor) or any(re.fullmatch(REGISTER, value) is None for value in registers):
            raise ConstructorOwnerError('Constructor register list does not match its descriptor')
        physical_registers = [physical(register) for register in registers]
        receiver = physical_registers[0]
        cursor = index - 1
        while cursor >= 0:
            before = lines[cursor][1]
            numeric = CONST.fullmatch(before)
            if numeric is None:
                break
            destination = physical(numeric[2])
            writes = {destination}
            if numeric[1].startswith('const-wide'):
                if destination + 1 >= total:
                    raise ConstructorOwnerError('Wide constant exceeds the method register layout')
                writes.add(destination + 1)
            if receiver in writes:
                raise ConstructorOwnerError('Constructor receiver was overwritten after allocation')
            cursor -= 1
        allocation = NEW.fullmatch(lines[cursor][1]) if cursor >= 0 else None
        if allocation is None or physical(allocation[1]) != receiver or allocation[2] != allocated:
            raise ConstructorOwnerError('Constructor lacks the pinned straight-line allocation')
        found.append(raw_index)
    return found


def restore_constructor_owners(entry: dict, compiled: str, original: str,
                               source: Callable[[str], str]) -> tuple[str, list[dict]]:
    rules = entry.get('constructor_owner_mappings')
    if rules is None:
        return compiled, []
    if not isinstance(rules, list) or not rules:
        raise ConstructorOwnerError('Constructor owner mappings must be an explicit nonempty list')
    if digest(original) != entry.get('original_method_sha256'):
        raise ConstructorOwnerError('Original method differs from its pinned SHA-256')
    result = compiled
    evidence = []
    seen = set()
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) != {'allocated_type', 'original_owner', 'constructor', 'occurrences'}:
            raise ConstructorOwnerError('Unexpected constructor owner mapping schema')
        allocated, owner, constructor = (rule[key] for key in ('allocated_type', 'original_owner', 'constructor'))
        if not all(isinstance(value, str) for value in (allocated, owner, constructor)):
            raise ConstructorOwnerError('Constructor mapping identities must be strings')
        if re.fullmatch(CLASS, allocated) is None or re.fullmatch(CLASS, owner) is None or allocated == owner:
            raise ConstructorOwnerError('Distinct valid subclass and superclass identities are required')
        count = rule['occurrences']
        if type(count) is not int or count < 1:
            raise ConstructorOwnerError('A positive exact occurrence count is required')
        words(constructor)
        key = (allocated, constructor)
        if key in seen:
            raise ConstructorOwnerError('Duplicate constructor owner mapping')
        seen.add(key)
        child_text, parent_text = source(allocated), source(owner)
        parent, child_methods, child_flags = declaration(child_text, allocated)
        _, parent_methods, _ = declaration(parent_text, owner)
        if parent != owner or child_flags & {'interface', 'abstract'}:
            raise ConstructorOwnerError('Allocation must name a concrete direct subclass of the original owner')
        if any(signature.startswith('<init>(') for signature in child_methods):
            raise ConstructorOwnerError('Pinned subclass must declare no constructor')
        flags = parent_methods.get(constructor, frozenset())
        if not {'public', 'constructor'} <= flags or flags & {'static', 'abstract', 'native'}:
            raise ConstructorOwnerError('Original owner must declare the public concrete constructor')
        original_calls = matching_calls(original, allocated, owner, constructor)
        compiled_calls = matching_calls(result, allocated, allocated, constructor)
        if len(original_calls) != count or len(compiled_calls) != count:
            raise ConstructorOwnerError('Original and compiled constructor occurrence counts differ from the rule')
        lines = result.splitlines(keepends=True)
        old_reference, new_reference = allocated + '->' + constructor, owner + '->' + constructor
        before = digest(result)
        for index in compiled_calls:
            if lines[index].count(old_reference) != 1:
                raise ConstructorOwnerError('Ambiguous constructor reference')
            lines[index] = lines[index].replace(old_reference, new_reference, 1)
        result = ''.join(lines)
        if len(matching_calls(result, allocated, owner, constructor)) != count:
            raise ConstructorOwnerError('Rewritten allocation/constructor shape was not preserved')
        evidence.append({**rule, 'original_method_sha256': digest(original),
                         'allocated_class_sha256': digest(child_text), 'owner_class_sha256': digest(parent_text),
                         'compiled_before_sha256': before, 'compiled_after_sha256': digest(result),
                         'owner_references_changed': len(compiled_calls), 'allocation_types_changed': 0,
                         'constructors_added': 0, 'android_verifier_executed': False})
    return result, evidence


def restore_from_preserved_source(entry: dict, compiled: str, original: str,
                                 index: dict, root: Path) -> tuple[str, list[dict]]:
    """Use the same pinned transformation in build and both migration verifiers.

    Only explicit mappings consult source. Each consulted class must have one
    unambiguous declaration in the migration target's loader domain and match
    its immutable class-index hash. No framework or compile-only stub is used.
    """
    if entry.get('constructor_owner_mappings') is None:
        return compiled, []
    target = entry.get('target')
    targets = [item for item in index.values() if item.get('descriptor') == target]
    if len(targets) != 1:
        raise ConstructorOwnerError('Constructor mapping needs one unambiguous migration target')
    def domain(item: dict) -> str:
        partition = item.get('partition')
        if not isinstance(partition, str) or not partition:
            raise ConstructorOwnerError('Preserved class loader domain is missing')
        return 'embedded' if partition.startswith('embedded_') else 'main'
    selected_domain = domain(targets[0])
    cache = {}
    source_root = (root / 'source/smali').resolve()
    def source(descriptor: str) -> str:
        if descriptor in cache:
            return cache[descriptor]
        choices = [item for item in index.values()
                   if item.get('descriptor') == descriptor and domain(item) == selected_domain]
        if len(choices) != 1:
            raise ConstructorOwnerError('Constructor class is missing or ambiguous in source domain: ' + descriptor)
        item = choices[0]
        path = root / item['path']
        if path.is_symlink() or not path.resolve().is_relative_to(source_root):
            raise ConstructorOwnerError('Constructor class path is outside preserved smali source')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item.get('sha256'):
            raise ConstructorOwnerError('Constructor class differs from its pinned class-index SHA-256: ' + descriptor)
        cache[descriptor] = raw.decode('utf-8')
        return cache[descriptor]
    original_class = source(target)
    declaration(original_class, target)
    headers = METHOD.findall(original)
    if len(headers) != 1 or headers[0][1] != entry.get('method') or original_class.count(original) != 1:
        raise ConstructorOwnerError('Original mapped method does not match the preserved migration target')
    result, evidence = restore_constructor_owners(entry, compiled, original, source)
    for proof in evidence:
        proof.update(source_domain=selected_domain, target_class_sha256=digest(original_class),
                     target_class_declaration_verified=True)
    return result, evidence
