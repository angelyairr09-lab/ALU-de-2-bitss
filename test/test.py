import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Iniciando pruebas de la ALU de 2 bits")

    # Configurar reloj de 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Secuencia de Reset inicial
    dut._log.info("Aplicando Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    # Probar las 16 combinaciones posibles de A (0..3) y B (0..3)
    for a in range(4):
        for b in range(4):
            a0 = a & 1
            a1 = (a >> 1) & 1
            b0 = b & 1
            b1 = (b >> 1) & 1

            # Armar entrada ui_in: IN0=A0, IN1=A1, IN2=B0, IN3=B1
            ui_val = (b1 << 3) | (b0 << 2) | (a1 << 1) | a0
            dut.ui_in.value = ui_val

            await ClockCycles(dut.clk, 2)

            # Calcular resultados esperados según las ecuaciones de la ALU
            eq = 1 if (a == b) else 0
            gt = 1 if (a > b) else 0

            # Resta A - B en complemento a 2 de 3 bits (R2 = signo/borrow, R1, R0)
            diff = (a - b) & 0b111
            r2 = (diff >> 2) & 1
            r1 = (diff >> 1) & 1
            r0 = diff & 1

            # Suma A + B de 3 bits (S2 = carry, S1, S0)
            suma = a + b
            s2 = (suma >> 2) & 1
            s1 = (suma >> 1) & 1
            s0 = suma & 1

            # Construir el byte esperado respetando el orden fijo Y0..Y7
            expected_uo = (
                (eq << 0) |  # Y0: A = B
                (gt << 1) |  # Y1: A > B
                (r2 << 2) |  # Y2: R2 (signo)
                (r1 << 3) |  # Y3: R1
                (r0 << 4) |  # Y4: R0
                (s2 << 5) |  # Y5: S2
                (s1 << 6) |  # Y6: S1
                (s0 << 7)    # Y7: S0
            )

            actual_uo = int(dut.uo_out.value)

            dut._log.info(
                f"A={a} ({a1}{a0}), B={b} ({b1}{b0}) -> "
                f"uo_out={actual_uo:08b} (esperado={expected_uo:08b})"
            )

            assert actual_uo == expected_uo, (
                f"Fallo en A={a}, B={b}: "
                f"salida obtenida {actual_uo:08b} != esperada {expected_uo:08b}"
            )

    dut._log.info("¡Las 16 combinaciones pasaron exitosamente!")
