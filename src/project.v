`default_nettype none

module tt_um_alu_2bits (
    input  wire [7:0] ui_in,    // Entradas dedicadas (DIP switches)
    output wire [7:0] uo_out,   // Salidas dedicadas (LEDs Y0..Y7)
    input  wire [7:0] uio_in,   // IOs: Entrada
    output wire [7:0] uio_out,  // IOs: Salida
    output wire [7:0] uio_oe,   // IOs: Enable (0 = entrada)
    input  wire       ena,      // Siempre 1 cuando el diseño está activo
    input  wire       clk,      // Reloj
    input  wire       rst_n     // Reset activo en bajo
);

  // Desactivar pines bidireccionales no utilizados
  assign uio_out = 8'b00000000;
  assign uio_oe  = 8'b00000000;

  // Mapeo de entradas (DIP 1=A0, 2=A1, 3=B0, 4=B1)
  wire a0 = ui_in[0];
  wire a1 = ui_in[1];
  wire b0 = ui_in[2];
  wire b1 = ui_in[3];

  // Señales internas (idénticas a las compuertas en Wokwi)
  wire p0   = a0 ^ b0;
  wire p1   = a1 ^ b1;
  wire c0   = a0 & b0;
  wire a1b1 = a1 & b1;

  // Suma (A + B)
  wire s0 = p0;
  wire s1 = p1 ^ c0;
  wire s2 = a1b1 | (p1 & c0);

  // Resta (A - B)
  wire bw0 = (~a0) & b0;
  wire d0  = p0;
  wire d1  = p1 ^ bw0;
  wire d2  = ((~a1) & b1) | ((~p1) & bw0);

  // Comparación (A = B y A > B)
  wire eq  = (~p0) & (~p1);
  wire neq = ~eq;
  wire gt  = (~d2) & neq;

  // Asignación fija de salidas Y0..Y7
  assign uo_out[0] = eq;   // Y0: A = B
  assign uo_out[1] = gt;   // Y1: A > B
  assign uo_out[2] = d2;   // Y2: R2 (signo / borrow)
  assign uo_out[3] = d1;   // Y3: R1
  assign uo_out[4] = d0;   // Y4: R0
  assign uo_out[5] = s2;   // Y5: S2 (carry out)
  assign uo_out[6] = s1;   // Y6: S1
  assign uo_out[7] = s0;   // Y7: S0

  // Evitar advertencias por señales sin usar
  wire _unused = &{ena, clk, rst_n, ui_in[7:4], uio_in, 1'b0};

endmodule
