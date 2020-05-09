`ifndef _latch_8bit_vh_
`define _latch_8bit_vh_

// Simple 8 bit latch
module latch_8bit(
    // clock input
    input le,
    // input
    input [0:7]din,
    // output
    output [0:7]dout
);

reg [0:7] latch_q;

always @(posedge le) begin
  latch_q <= din;
end

assign dout = latch_q;

endmodule

`endif 
