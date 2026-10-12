import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;

/** Execute an existing suite while proving the stricter oracle was the loaded class. */
public final class OracleRegressionLauncher {
    public static void main(String[] args) throws Throwable {
        Path expected = Paths.get(args[0]).toRealPath();
        Path actual = Paths.get(BytecodeOracle.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath();
        if (!actual.equals(expected)) throw new AssertionError("Wrong oracle class origin: " + actual);
        Set<String> allowed = Set.of("OracleSemanticsTests", "EngineOracleConformance", "UiOracleConformance", "ParityTests", "CoreParityTests", "EnvironmentParityTests", "EngineParityTests", "UiParityTests");
        if (!allowed.contains(args[1])) throw new IllegalArgumentException("Unselected baseline suite");
        Class<?> suite = Class.forName(args[1]);
        try { suite.getMethod("main", String[].class).invoke(null, (Object) Arrays.copyOfRange(args, 2, args.length)); }
        catch (InvocationTargetException failure) { throw failure.getCause(); }
        int checked = 0;
        for (Field field : suite.getDeclaredFields()) {
            if (Modifier.isStatic(field.getModifiers()) && field.getType() == BytecodeOracle.class) {
                field.setAccessible(true);
                BytecodeOracle oracle = (BytecodeOracle) field.get(null);
                if (oracle == null) continue;
                if (!oracle.parentConstructorAdapters.isEmpty() || !oracle.parentConstructorAdapterCalls.isEmpty())
                    throw new AssertionError("Baseline suite configured or used a parent adapter");
                checked++;
            }
        }
        if (checked == 0) throw new AssertionError("No executed oracle instances inspected");
        System.out.println("STRICT_ORACLE_REGRESSION origin=" + actual + " instances=" + checked + " rules=0 adaptations=0");
    }
}
