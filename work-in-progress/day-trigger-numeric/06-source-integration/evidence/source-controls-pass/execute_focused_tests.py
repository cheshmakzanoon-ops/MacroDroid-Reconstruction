import pathlib,sys,unittest
sys.dont_write_bytecode=True
view=pathlib.Path(sys.argv[1]);sys.path[:0]=[str(view),str(view/'tests')]
import build
build.JAR=pathlib.Path(sys.argv[2])
suite=unittest.defaultTestLoader.loadTestsFromNames(['test_day_numeric','test_ui_mutation_catalog'])
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() and result.testsRun==43 and not result.skipped else 2)
