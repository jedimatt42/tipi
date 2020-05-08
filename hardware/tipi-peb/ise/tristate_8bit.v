`ifndef _tristate_8bit_vh_
`define _tristate_8bit_vh_

module tristate_8bit(
    input T,
    input [7:0] I,
    output [7:0] O
    );

assign O = T ? I: 8'bZ;

endmodule

`endif
