package recovered.probe;

import defpackage.zhh;

/** Standalone constructor allocation probe; not an application replacement. */
public final class ConstructorProbe {
    public static zhh allocate() {
        return new zhh(2, null);
    }

    public static void main(String[] args) {
        zhh value = allocate();
        if (value.getArity() != 2) throw new AssertionError("Unexpected original constructor arity");
        System.out.println("CONSTRUCTOR_ALLOCATION_OK class=" + value.getClass().getSimpleName() + " arity=" + value.getArity());
    }
}
