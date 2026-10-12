"""Bounded transformation tests using explicit synthetic DEX text, not Android."""
import copy
import unittest

from constructor_owner import ConstructorOwnerError, digest, restore_constructor_owners


CHILD = '.class public final LChild;\n.super LParent;\n'
PARENT = '.class public LParent;\n.super Ljava/lang/Object;\n.method public constructor <init>(ILContinuation;)V\n.locals 0\nreturn-void\n.end method\n'
ORIGINAL = '.method public static create()LChild;\n.locals 3\nnew-instance v0, LChild;\n.line 20\ninvoke-direct {v0, v1, v2}, LParent;-><init>(ILContinuation;)V\nreturn-object v0\n.end method'
COMPILED = ORIGINAL.replace('LParent;-><init>', 'LChild;-><init>').replace('.line 20', 'const/4 v1, 0x2\nconst/4 v2, 0x0')


class ConstructorOwnerTests(unittest.TestCase):
    def setUp(self):
        self.entry = {'original_method_sha256': digest(ORIGINAL), 'constructor_owner_mappings': [
            {'allocated_type': 'LChild;', 'original_owner': 'LParent;', 'constructor': '<init>(ILContinuation;)V', 'occurrences': 1}]}
        self.sources = {'LChild;': CHILD, 'LParent;': PARENT}

    def transform(self, compiled=COMPILED, original=ORIGINAL):
        return restore_constructor_owners(self.entry, compiled, original, self.sources.__getitem__)

    def test_exact_owner_rewrite_preserves_every_other_byte(self):
        result, evidence = self.transform()
        self.assertEqual(result, COMPILED.replace('LChild;-><init>', 'LParent;-><init>'))
        self.assertEqual(evidence[0]['owner_references_changed'], 1)
        self.assertEqual(evidence[0]['allocation_types_changed'], 0)
        self.assertEqual(evidence[0]['constructors_added'], 0)
        self.assertFalse(evidence[0]['android_verifier_executed'])

    def test_unconfigured_body_is_untouched(self):
        self.assertEqual(restore_constructor_owners({}, COMPILED, '', lambda _: self.fail()), (COMPILED, []))

    def test_changed_original_hash_is_rejected(self):
        with self.assertRaisesRegex(ConstructorOwnerError, 'pinned SHA-256'):
            self.transform(original=ORIGINAL + '\n')

    def test_unrelated_parent_is_rejected(self):
        self.sources['LChild;'] = CHILD.replace('LParent;', 'LOther;')
        with self.assertRaisesRegex(ConstructorOwnerError, 'direct subclass'):
            self.transform()

    def test_existing_child_constructor_is_rejected(self):
        self.sources['LChild;'] += '\n.method public constructor <init>()V\n.locals 0\nreturn-void\n.end method\n'
        with self.assertRaisesRegex(ConstructorOwnerError, 'no constructor'):
            self.transform()

    def test_non_public_or_non_concrete_parent_constructor_is_rejected(self):
        for replacement in ['private constructor', 'public static constructor', 'public abstract constructor', 'public native constructor']:
            with self.subTest(flags=replacement), self.assertRaisesRegex(ConstructorOwnerError, 'public concrete'):
                self.sources['LParent;'] = PARENT.replace('public constructor', replacement)
                self.transform()

    def test_allocation_type_or_receiver_mismatch_is_rejected(self):
        for replacement in ['new-instance v0, LOther;', 'new-instance v2, LChild;']:
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ConstructorOwnerError, 'straight-line allocation'):
                self.transform(COMPILED.replace('new-instance v0, LChild;', replacement))

    def test_receiver_constant_overwrite_is_rejected(self):
        with self.assertRaisesRegex(ConstructorOwnerError, 'overwritten'):
            self.transform(COMPILED.replace('const/4 v1', 'const/4 v0'))

    def test_wide_constant_cannot_overwrite_receiver_high_word(self):
        altered = COMPILED.replace('v0', 'v1').replace('const/4 v1, 0x2', 'const-wide/16 v0, 0x2')
        with self.assertRaisesRegex(ConstructorOwnerError, 'overwritten'):
            self.transform(altered)

    def test_branch_label_alias_or_side_effect_between_allocation_and_init_is_rejected(self):
        for instruction in [':label', 'if-eqz v1, :elsewhere', 'move-object v0, v3', 'invoke-static {}, LOther;->effect()V', 'const-class v2, LOther;']:
            with self.subTest(instruction=instruction), self.assertRaisesRegex(ConstructorOwnerError, 'straight-line allocation'):
                self.transform(COMPILED.replace('const/4 v1, 0x2', instruction))

    def test_original_shape_is_validated_independently(self):
        original = ORIGINAL.replace('new-instance v0, LChild;', 'new-instance v0, LOther;')
        self.entry['original_method_sha256'] = digest(original)
        with self.assertRaisesRegex(ConstructorOwnerError, 'straight-line allocation'):
            self.transform(original=original)

    def test_missing_and_extra_occurrences_are_rejected(self):
        duplicate = COMPILED.replace('return-object v0', 'new-instance v0, LChild;\ninvoke-direct {v0, v1, v2}, LChild;-><init>(ILContinuation;)V\nreturn-object v0')
        for compiled in [COMPILED.replace('LChild;-><init>', 'LOther;-><init>'), duplicate]:
            with self.subTest(compiled=compiled), self.assertRaisesRegex(ConstructorOwnerError, 'occurrence counts'):
                self.transform(compiled)

    def test_wrong_invocation_kind_and_range_are_rejected(self):
        for opcode in ['invoke-virtual', 'invoke-direct/range']:
            with self.subTest(opcode=opcode), self.assertRaisesRegex(ConstructorOwnerError, 'non-range direct'):
                self.transform(COMPILED.replace('invoke-direct', opcode))

    def test_constructor_register_words_are_validated(self):
        with self.assertRaisesRegex(ConstructorOwnerError, 'register list'):
            self.transform(COMPILED.replace('{v0, v1, v2}', '{v0, v1}'))

    def test_rules_require_an_exact_positive_count(self):
        for count in [0, -1, True, 1.0, '1']:
            with self.subTest(count=count), self.assertRaisesRegex(ConstructorOwnerError, 'occurrence count'):
                self.entry['constructor_owner_mappings'][0]['occurrences'] = count
                self.transform()

    def test_duplicate_rules_and_unknown_fields_are_rejected(self):
        rule = copy.deepcopy(self.entry['constructor_owner_mappings'][0])
        self.entry['constructor_owner_mappings'].append(rule)
        with self.assertRaisesRegex(ConstructorOwnerError, 'Duplicate'):
            self.transform()
        self.entry['constructor_owner_mappings'] = [rule]
        rule['unreviewed'] = True
        with self.assertRaisesRegex(ConstructorOwnerError, 'schema'):
            self.transform()

    def test_parameter_alias_cannot_overwrite_receiver(self):
        for allocation, overwrite, invocation in [('v3', 'const/4 p0, 0x0', 'v3'), ('p0', 'const-wide/16 v2, 0x0', 'p0')]:
            compiled = ('.method public static create(I)LChild;\n.locals 3\nnew-instance ' + allocation + ', LChild;\n' +
                        overwrite + '\ninvoke-direct {' + invocation + ', v1, v2}, LChild;-><init>(ILContinuation;)V\nreturn-object ' + invocation + '\n.end method')
            with self.subTest(allocation=allocation), self.assertRaisesRegex(ConstructorOwnerError, 'overwritten'):
                self.transform(compiled)

    def test_registers_directive_normalizes_parameter_aliases(self):
        compiled = ('.method public static create(I)LChild;\n.registers 4\nnew-instance v3, LChild;\nconst/4 p0, 0x0\n'
                    'invoke-direct {v3, v1, v2}, LChild;-><init>(ILContinuation;)V\nreturn-object v3\n.end method')
        with self.assertRaisesRegex(ConstructorOwnerError, 'overwritten'):
            self.transform(compiled)

    def test_indented_child_constructor_is_not_missed(self):
        self.sources['LChild;'] += '  .method public constructor <init>()V\n.locals 0\nreturn-void\n.end method\n'
        with self.assertRaisesRegex(ConstructorOwnerError, 'no constructor'):
            self.transform()

    def test_unknown_constant_opcode_is_not_a_safe_gap(self):
        with self.assertRaisesRegex(ConstructorOwnerError, 'straight-line allocation'):
            self.transform(COMPILED.replace('const/4 v1', 'const/notanopcode v1'))


if __name__ == '__main__':
    unittest.main()
