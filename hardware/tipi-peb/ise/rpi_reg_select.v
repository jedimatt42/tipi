`ifndef _rrpi_reg_select_vh_
`define _rrpi_reg_select_vh_

/*
 Latch a 4 bit selection register of first clk that follows 
 the internal counter being zero.. 
 Reset clears the register and clears the counter to zero.
 next clock sets the register.
 next 2 clocks are ignored. 
 then a 3rd clock sets the register
 repeat.
*/
module rpi_reg_select(reset, clk, din, reg_sel);
input reset;
input clk;
input [3:0]din;
output [3:0]reg_sel;

reg [3:0]tmp = 0;
reg [1:0]count = 0;

always @(posedge clk, posedge reset) begin
  if (reset == 1) begin
    tmp <= 0;
	 count <= 0;
  end
  else begin
    if (count == 0) begin 
	   tmp <= din;
    end
    if (count == 2) count <= 0;
    else count <= count + 1;
  end
end

assign reg_sel = tmp;

endmodule

`endif
