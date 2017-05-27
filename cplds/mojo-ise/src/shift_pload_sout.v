`ifndef _shift_pload_sout_vh_
`define _shift_pload_sout_vh_

module shift_pload_sout (
    // Clock for shifting
    input clk,
	 // Operations are ignored unless CS is high
    input cs,
	 // Load parallel data
    input aload,
	 // Data to load from
    input [7:0]data,
	 // output bit from the left.
    output sout
);

reg [7:0]tmp;

always @(posedge clk) begin
    if (cs) begin
        if (aload) tmp = data;
        else tmp = {tmp[6:0], 1'b0};
     end
end

assign sout = tmp[7];

endmodule

`endif
