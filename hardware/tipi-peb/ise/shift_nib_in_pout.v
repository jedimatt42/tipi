`ifndef _shift_nib_in_pout_vh_
`define _shift_nib_in_pout_vh_

// 8 bit serial in, parallel out shift register.
module shift_nib_in_pout(
    // clock input
    input clk,
    // select line
    input select,
    // latch data to expose internal shifter.
    input le,
    // input nibble
    input [0:3]din,
    // output byte
    output [0:7]dout
);

reg [0:7] latch_q = 0;
reg [0:7] shift_q = 0;

always @(posedge clk) begin
  if (select) begin
    if (le) latch_q <= shift_q;
    else shift_q <= { shift_q[4:7], din };
  end
end

assign dout = select ? latch_q : 8'bz;

endmodule

`endif 
