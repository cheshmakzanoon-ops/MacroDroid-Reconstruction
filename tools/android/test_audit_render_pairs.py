"""Host regressions for unmasked screenshot differential diagnostics."""
from __future__ import annotations
import binascii
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib
from audit_render_pairs import audit_pair, make_report, pixels_as_rgba, main


def png(width, height, rgba, *, mode=6):
    channels = 4 if mode == 6 else 3
    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data +
                struct.pack('>I', binascii.crc32(tag + data) & 0xffffffff))
    pixel = bytes(rgba[:channels])
    scanlines = (b'\x00' + pixel * width) * height
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, mode, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(scanlines)) + chunk(b'IEND', b''))


class RenderAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
    def files(self, first, second):
        a, b = self.path / 'a.png', self.path / 'b.png'
        a.write_bytes(first)
        b.write_bytes(second)
        return a, b
    def test_full_image_exact_match_has_zero_changed_pixels(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(3, 2, (15, 20, 30, 255)))
        r = audit_pair('equal', a, b)
        self.assertTrue(r['exact_pixels_equal'])
        self.assertEqual(r['changed_pixels'], 0)
        self.assertIsNone(r['changed_bbox_xyxy'])
        self.assertFalse(r['whole_app_parity_established'])
    def test_changed_pixels_are_all_counted(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(3, 2, (16, 20, 30, 255)))
        r = audit_pair('different', a, b)
        self.assertEqual(r['changed_pixels'], 6)
        self.assertEqual(r['changed_bbox_xyxy'], [0, 0, 2, 1])
        self.assertEqual(r['rows_with_changes'], 2)
        self.assertEqual(r['columns_with_changes'], 3)
        self.assertEqual(r['common_rgba_changes'][0]['count'], 6)
        self.assertFalse(r['exact_pixels_equal'])
        self.assertEqual(r['pixel_tolerance'], 0)
    def test_dimension_mismatch_is_never_equal(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(4, 2, (15, 20, 30, 255)))
        r = audit_pair('size', a, b)
        self.assertEqual(r['status'], 'DIMENSION_MISMATCH')
        self.assertIsNone(r['changed_pixels'])
        self.assertFalse(r['exact_pixels_equal'])
    def test_equal_rgb_and_rgba_content(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255), mode=2), png(3, 2, (15, 20, 30, 255)))
        self.assertTrue(audit_pair('colors', a, b)['exact_pixels_equal'])
        self.assertFalse(audit_pair('colors', a, b)['identical_png_bytes'])
    def test_alpha_channel_cannot_be_masked(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(3, 2, (15, 20, 30, 254)))
        self.assertEqual(audit_pair('alpha', a, b)['changed_pixels'], 6)
    def test_corrupt_png_crc_is_rejected(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(3, 2, (15, 20, 30, 255)))
        data=bytearray(b.read_bytes());data[-5] ^= 1;b.write_bytes(data)
        with self.assertRaises(ValueError):audit_pair('corrupt', a, b)
    def test_same_file_or_hardlink_cannot_fake_match(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(3, 2, (15, 20, 30, 255)))
        with self.assertRaises(ValueError):audit_pair('same', a, a)
        b.unlink();b.hardlink_to(a)
        with self.assertRaises(ValueError):audit_pair('same', a, b)
    def test_invalid_labels_and_duplicates_fail_closed(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(3, 2, (15, 20, 30, 255)))
        with self.assertRaises(ValueError):audit_pair('../bad', a, b)
        with self.assertRaises(ValueError):make_report([['same', str(a), str(b)], ['same', str(a), str(b)]])
        with self.assertRaises(ValueError):make_report([])
    def test_paired_report_keeps_mismatch_even_when_diagnostic_exits_successfully(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(3, 2, (15, 20, 31, 255)))
        path = self.path / 'report.json'
        self.assertEqual(main(['--pair','check',str(a),str(b),'--output',str(path)]),0)
        report = json.loads(path.read_text())
        self.assertFalse(report['all_pixels_equal'])
        self.assertFalse(report['whole_app_parity_established'])
        self.assertEqual(report['pairs'][0]['status'], 'PIXEL_DIFFERENCE')
    def test_report_must_not_overwrite_input(self):
        a, b = self.files(png(3, 2, (15, 20, 30, 255)), png(3, 2, (15, 20, 31, 255)))
        with self.assertRaises(SystemExit) as cm:
            main(['--pair','check',str(a),str(b),'--output',str(a)])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(a.read_bytes(),png(3, 2, (15, 20, 30, 255)))

if __name__ == '__main__':
    unittest.main()
