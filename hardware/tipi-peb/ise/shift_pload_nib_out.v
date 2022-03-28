`ifndef _shift_pload_nib_out_vh_
`define _shift_pload_nib_out_vh_

module shift_pload_nib_out (
    // Clock for shifting
    input clk,
	 // Select
	 input select,
	 // load tmp with data to shift out.
    input le,
	 // Data to load from
    input [7:0]data,
	 // output bit from the left.
    output [3:0]nout
);

reg [7:0]tmp = 0;

always @(posedge clk) begin
  if (le && select) tmp[7:0] = data;
  else if (select) tmp[7:0] = { tmp[3:0], 4'h0 };
end

assign nout = select ? tmp[7:4] : 4'bz;

endmodule

`endif
