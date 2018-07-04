`ifndef _rreg_mux_vh_
`define _rreg_mux_vh_

module mux2_8bit(a_addr, a, b_addr, b, c_addr, c, d_addr, d, o);
input a_addr;
input b_addr;
input c_addr;
input d_addr;
input [7:0]a;
input [7:0]b;
input [7:0]c;
input [7:0]d;
output [7:0]o;
reg [7:0]tmp;

always @(a_addr, b_addr, c_addr, d_addr) begin
  if (a_addr) tmp <= a;
  else if (b_addr) tmp <= b;
  else if (c_addr) tmp <= c;
  else if (d_addr) tmp <= d;
  else tmp <= 8'h00;
end

assign o = tmp;

endmodule

`endif
