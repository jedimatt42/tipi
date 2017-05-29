`ifndef _shift_pload_sout_vh_
`define _shift_pload_sout_vh_

module shift_pload_sout (
    // Clock for shifting
    input clk,
	 // Operations are ignored unless CS is high
    input aload,
	 // Data to load from
    input [7:0]data,
	 // output bit from the left.
    output sout,
	 // debugging
	 output [7:0] dout
);

reg [7:0]tmp;

always @(posedge clk) begin
    if (aload) tmp = data;
    else tmp = {tmp[6:0], 1'b0};
end

assign sout = tmp[7];
assign dout = tmp;

endmodule

`endif
