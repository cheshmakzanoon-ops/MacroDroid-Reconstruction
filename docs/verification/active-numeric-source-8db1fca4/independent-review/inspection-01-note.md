# Retained reviewer inspection mistake

An initial ad hoc display of the retained numeric command rows used `row['label']`. The actual numeric schema-2 producer names this field `name`. That display command stopped with the following literal error after printing the first command, pipeline and fault summaries:

```text
Traceback (most recent call last):
  File "<stdin>", line 10, in <module>
KeyError: 'label'
```

The failing expression was:

```python
[(v['label'], v.get('returncode'), v.get('expected_returncode'), v.get('timeout_seconds'))
 for v in x['commands']]
```

This was an inspection-only field-name assumption, not a failure of the application, recorded command producer, archive collector or acceptance gates. The corrected display reads `name`, actual `returncode` and exact `timeout_seconds`; it does not invent an `expected_returncode` field in numeric rows. No report or source bytes were changed. All subsequent analysis uses the retained files from the original single ZIP content pass; the APKs and ZIP payloads were not read a second time.
