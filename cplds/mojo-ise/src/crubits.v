`ifndef _crubits_vh_
`define _crubits_vh_

// 4 bits of CRU
module crubits(
    // select
    input [0:3]cru_base,
    // TI clock input
    input cru_clk,
    // cru_address
    input [0:14]addr,
    // input
    input [0:7]cru_in,
    // bits
    output [0:3]bits
);

reg [0:3] bits_q;

always @(negedge cru_clk) begin
  if ((addr[0:3] == 4'b0001) && (addr[4:7] == cru_base)) begin
    if (addr[8:14] == 7'h00) bits_q[0] <= cru_in;
    else if (addr[8:14] == 7'h01) bits_q[1] <= cru_in;
    else if (addr[8:14] == 7'h02) bits_q[2] <= cru_in;
    else if (addr[8:14] == 7'h03) bits_q[3] <= cru_in;
  end
end

assign bits = bits_q;

endmodule

`endif 
