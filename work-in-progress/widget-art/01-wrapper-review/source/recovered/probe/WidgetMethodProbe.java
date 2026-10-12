package recovered.probe;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.Collections;
import java.util.List;

/** Reflection-only probe. Every Android/application class comes from the guest
 * boot classpath or the single unchanged application APK on the command line.
 * No nonempty widget list, application Context, logger or renderer is supplied.
 */
public final class WidgetMethodProbe {
    private static Class<?> managerType;
    private static Class<?> stateType;
    private static Constructor<?> stateConstructor;
    private static Method update;
    private static Object manager;
    private static Object unit;

    private WidgetMethodProbe() {}

    private static void require(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }

    private static Field field(String name) throws Exception {
        Field value = stateType.getDeclaredField(name);
        value.setAccessible(true);
        return value;
    }

    private static void prepare() throws Exception {
        ClassLoader loader = WidgetMethodProbe.class.getClassLoader();
        Class<?> looper = Class.forName("android.os.Looper", true, loader);
        Object mainLooper = looper.getMethod("getMainLooper").invoke(null);
        if (mainLooper == null) {
            require(looper.getMethod("myLooper").invoke(null) == null,
                "Guest main thread already has a non-main Looper");
            looper.getMethod("prepareMainLooper").invoke(null);
            mainLooper = looper.getMethod("getMainLooper").invoke(null);
        }
        require(mainLooper != null && looper.getMethod("myLooper").invoke(null) == mainLooper,
            "Guest main Looper was not prepared on this thread");

        managerType = Class.forName("com.arlosoft.macrodroid.widget.custom.WidgetUpdateManager", true, loader);
        stateType = Class.forName("com.arlosoft.macrodroid.widget.custom.b", true, loader);
        Class<?> continuationType = Class.forName("o73", false, loader);
        Class<?> unitType = Class.forName("blg", true, loader);
        for (Class<?> type : new Class<?>[]{managerType, stateType, continuationType, unitType}) {
            require(type.getClassLoader() == loader, "Application class came from another classloader: " + type.getName());
        }
        manager = managerType.getField("a").get(null);
        unit = unitType.getField("a").get(null);
        require(manager != null && manager.getClass() == managerType, "Real manager singleton identity is invalid");
        require(unit != null && unit.getClass() == unitType, "Real Unit singleton identity is invalid");
        Class<?> contextType = Class.forName("android.content.Context", false, loader);
        update = managerType.getDeclaredMethod("m", contextType, List.class, continuationType);
        require(update.getDeclaringClass() == managerType && update.getReturnType() == Object.class,
            "Selected method has an unexpected owner or return type");
        require(update.getModifiers() == (Modifier.PUBLIC | Modifier.FINAL),
            "Selected method is not the preserved public final instance method");
        stateConstructor = stateType.getDeclaredConstructor(managerType, continuationType);
        stateConstructor.setAccessible(true);
        require(managerType.getField("d").get(null) == null, "Guest initialization unexpectedly set an application Context");
    }

    private static Object newState(int label, Object[] slots) throws Exception {
        Object state = stateConstructor.newInstance(new Object[]{manager, null});
        field("label").setInt(state, label | Integer.MIN_VALUE);
        field("result").set(state, unit);
        field("I$0").setInt(state, -13);
        field("I$1").setInt(state, 417);
        field("I$2").setInt(state, Integer.MAX_VALUE);
        for (int index = 0; index < slots.length; index++) field("L$" + index).set(state, slots[index]);
        return state;
    }

    private static Object[] slots() {
        return new Object[]{null, null, null, null, null, Collections.emptyList().iterator(), new Object(), null};
    }

    private static void unchangedState(Object state, int label, Object[] slots) throws Exception {
        require(field("label").getInt(state) == label, "Continuation high bit or saved label changed incorrectly");
        require(field("result").get(state) == unit && field("this$0").get(state) == manager,
            "Continuation result or owner identity changed");
        require(field("I$0").getInt(state) == -13 && field("I$1").getInt(state) == 417
                && field("I$2").getInt(state) == Integer.MAX_VALUE,
            "Saved integer state changed on a service-free branch");
        for (int index = 0; index < slots.length; index++) {
            require(field("L$" + index).get(state) == slots[index], "Saved object slot changed: L$" + index);
        }
    }

    private static Object invoke(List<?> widgets, Object state) throws Exception {
        return update.invoke(manager, new Object[]{null, widgets, state});
    }

    private static Throwable failure(List<?> widgets, Object state, Class<?> expected) throws Exception {
        try {
            invoke(widgets, state);
        } catch (InvocationTargetException wrapped) {
            Throwable actual = wrapped.getCause();
            require(actual != null && actual.getClass() == expected,
                "Expected " + expected.getName() + " but observed " + (actual == null ? "null" : actual.getClass().getName()));
            return actual;
        }
        throw new AssertionError("Expected target method to throw " + expected.getName());
    }

    private static void passed(String name) throws Exception {
        require(managerType.getField("d").get(null) == null, "A probe case changed the application Context field");
        System.out.println("WIDGET_ART_CASE_OK " + name);
    }

    public static void main(String[] args) throws Exception {
        require(args.length == 0, "Widget probe takes no arguments");
        prepare();
        require(invoke(Collections.emptyList(), null) == unit, "Fresh empty list did not return the real Unit singleton");
        passed("fresh-empty-unit-identity");

        Object[] zeroSlots = slots();
        Object zero = newState(0, zeroSlots);
        require(invoke(Collections.emptyList(), zero) == unit, "Reused label 0 did not return Unit");
        unchangedState(zero, 0, zeroSlots);
        passed("reused-label-zero-empty");

        Object[] twoSlots = slots();
        Object two = newState(2, twoSlots);
        require(invoke(null, two) == unit, "Label 2 with empty iterator did not return Unit");
        unchangedState(two, 2, twoSlots);
        passed("resumed-label-two-empty");

        Object[] invalidSlots = slots();
        Object invalid = newState(3, invalidSlots);
        Throwable invalidFailure = failure(null, invalid, IllegalStateException.class);
        require("call to 'resume' before 'invoke' with coroutine".equals(invalidFailure.getMessage()),
            "Invalid-label exception message differs from the preserved literal");
        unchangedState(invalid, 3, invalidSlots);
        passed("invalid-label-exact-exception");

        for (int slot : new int[]{7, 4, 1}) {
            Object[] castSlots = slots();
            castSlots[slot] = Integer.valueOf(839);
            Object cast = newState(2, castSlots);
            failure(null, cast, ClassCastException.class);
            unchangedState(cast, 2, castSlots);
            passed("label-two-dead-cast-L" + slot);
        }

        failure(null, null, NullPointerException.class);
        passed("null-list-exception-type");
        System.out.println("WIDGET_METHOD_ART_OK cases=8");
    }
}
