`ifndef _crubits_vh_
`define _crubits_vh_

// 4 bits of CRU
module crubits(
    // select
    input [0:3]cru_base,
    // TI clock input
    input ti_cru_clk,
	 // TI mem enable (when high, not a memory operation
	 input ti_memen,
	 // TI phase 3 clock for cru input to cpu
	 input ti_ph3,
    // cru_address
    input [0:14]addr,
    // input
    input ti_cru_out,
	 // input to TMS9900 to allow reading curring addressed bit
	 output ti_cru_in,
    // bits
    output [0:3]bits
);

reg [0:3] bits_q;

always @(negedge ti_cru_clk) begin
  if ((addr[0:3] == 4'b0001) && (addr[4:7] == cru_base)) begin 
    if (addr[8:14] == 7'h00) bits_q[0] <= ti_cru_out;
    else if (addr[8:14] == 7'h01) bits_q[1] <= ti_cru_out;
    else if (addr[8:14] == 7'h02) bits_q[2] <= ti_cru_out;
    else if (addr[8:14] == 7'h03) bits_q[3] <= ti_cru_out;
  end
end

assign bits = bits_q;

reg dataout;

always @(negedge ti_ph3) begin
  if (ti_memen && (addr[0:3] == 4'b0001) && (addr[4:7] == cru_base)) begin
    if (addr[8:14] == 7'h00) dataout <= bits_q[0];
    else if (addr[8:14] == 7'h01) dataout <= bits_q[1];
    else if (addr[8:14] == 7'h02) dataout <= bits_q[2];
    else if (addr[8:14] == 7'h03) dataout <= bits_q[3];
  end
  else dataout <= 1'bz;
end

assign ti_cru_in = dataout;

endmodule

`endif 
