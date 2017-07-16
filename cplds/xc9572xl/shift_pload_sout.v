`ifndef _shift_pload_sout_vh_
`define _shift_pload_sout_vh_

module shift_pload_sout (
    // Clock for shifting
    input clk,
	 // load tmp with data to shift out.
    input aload,
	 // Data to load from
    input [7:0]data,
	 // output bit from the left.
    output sout,
	 // debugging
	 output [7:0] dout
);

reg [8:0]tmp;

always @(posedge clk) begin
    if (aload) tmp = { 1'b0, data };
    else tmp = {tmp[7:0], 1'b0};
end

assign sout = tmp[8];
assign dout = tmp[7:0];

endmodule

`endif
