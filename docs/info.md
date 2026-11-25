## How it works

Este proyecto implementa una Unidad Aritmético-Lógica (ALU) combinacional de 2 bits que opera sobre dos números binarios sin signo: **A** (`A1 A0`) y **B** (`B1 B0`). De manera simultánea calcula la comparación (`A = B`, `A > B`), la resta (`A - B`) y la suma (`A + B`), reflejando los resultados en las salidas `uo[0]` a `uo[7]` (`Y0` a `Y7`).

## How to test

1. Configura los primeros 4 interruptores de entrada (`ui[0]` a `ui[3]`):
   - `ui[0]`: **A0**
   - `ui[1]`: **A1**
   - `ui[2]`: **B0**
   - `ui[3]`: **B1**
2. Observa los 8 LEDs de salida (`uo[0]` a `uo[7]`):
   - **Y0 (`uo[0]`)**: Se enciende cuando `A = B`.
   - **Y1 (`uo[1]`)**: Se enciende cuando `A > B`.
   - **Y2–Y4 (`uo[2]:uo[4]`)**: Resultado de `A - B` (`R2` signo/borrow, `R1`, `R0`).
   - **Y5–Y7 (`uo[5]:uo[7]`)**: Resultado de `A + B` (`S2` carry, `S1`, `S0`).

## External hardware

No se requiere hardware externo adicional; utiliza los interruptores DIP y LEDs estándar de la placa de demostración de Tiny Tapeout.
