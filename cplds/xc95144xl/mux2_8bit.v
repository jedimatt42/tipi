`ifndef _rreg_mux_vh_
`define _rreg_mux_vh_

module mux2_8bit(clk, s, a, b, c, d, o);
input clk;
input [0:2]s;
input [7:0]a;
input [7:0]b;
input [7:0]c;
input [7:0]d;
output [7:0]o;
reg [7:0]o;

always @(negedge clk)
  begin
    case (s)
      3'b001 : o = a;
      3'b011 : o = b;
      3'b101 : o = c;
		3'b111 : o = d;
      default : o = 8'h00;
    endcase
  end
endmodule

`endif
