`timescale 1ns / 1ps

`include "crubits.v"
`include "latch_8bit.v"
`include "tristate_8bit.v"
`include "mux2_8bit.v"
`include "tipi_4bit_pi_bus.v"

module tipi_top #(
  parameter LOW_ROM_ADDR = 16'h4000,  // CPU address of first byte in DSR ROM
  parameter HIGH_ROM_ADDR = 16'h5ff7, // CPU address of last byte in DSR ROM
  parameter HIGH_MEM_ADDR = 16'h5fff, // CPU address of highest memory mapped IO register
  parameter RC_ADDR = 16'h5ff9, // CPU address of RC register
  parameter RD_ADDR = 16'h5ffb, // CPU address of RD register
  parameter TC_ADDR = 16'h5ffd, // CPU address of TC register
  parameter TD_ADDR = 16'h5fff  // CPU address of TD register
)(
  output led0, // Control for activity LED
  
  input [0:3] crub, // Active low jumper block to set CRU base
  
  output db_dir, // Control external 74LS256 tristate buffer direction
  output db_en,  // Control external 74LS256 tristate buffer output enable
  output dsr_b0, // Control external 32k EPROM high address bit for bank switching the DSR ROM
  output dsr_b1, // Control external 32k EPROM second high address bit for bank switching the DSR ROM
  output dsr_en, // Control external 32K EPROM output enable
  
  // Physical interface to the Raspberry PI
  input r_clk,        // 4bit_pi_bus clock from Raspberry PI
  input r_nibrst,     // 4bit_pi_bus reset from Raspberry PI
  inout [0:3] r_nib,  // 4bit_pi_bus data bus connected to Raspberry PI
  output r_reset,     // Reset signal output to the Raspberry PI

  // CRU for the TMS9900 CPU is a serial protocol. 
  input ti_cruclk,    // clock signal from the TMS9900 CPU for CRU bit transfers
  output ti_cruin,    // data line to the CRU input bit of the TMS9900 CPU 

  // bus control signals from the TMS9900 CPU
  input ti_dbin,      // indicates input based memory operation from CPU (active low)
  input ti_memen,     // indicates address is memory operation vs CRU IO operation (active low)
  input ti_we,        // indicates memory operation is a write (active low) 
  input ti_ph3,       // TMS9900 CPU phase 3 of clock cycle

  // For future use. If set active low, this would trigger an interrupt in the TMS9900.
  output ti_extint,   // interrupt CPU
  
  // TMS9900 address and data bus interface
  input [0:15] ti_a,  // 16bit address bus from TMS9900 CPU
  inout [0:7] tp_d    // 8 bit data bus connects to external 74LS256 before then connecting to the TI-99/4A multiplexer
);

  // For future use. Keep at high-impedance.  
  assign ti_extint = 1'bz; // try to avoid triggering this interrupt (temporarily an input)

  // Process CRU bits
  wire ti_cruout = ti_a[15];  // CRU output is multiplexed onthe LSBit pin of the TI-99/4A external address bus
  wire [0:3] cru_state;       // access to 4 bit register in crubits module
  wire cru_regout;
  crubits cru(~crub, ti_cruclk, ti_memen, ti_ph3, ti_a[0:14], ti_cruout, cru_regout, cru_state); 
  wire cru_dev_en = cru_state[0]; // crubit 0 enables the expansion card, allowing it's IO and ROM to be on data base for addresses 0x4000-0x5fff.
  assign ti_cruin = cru_regout;   // connect the output value of a selected CRU bit for reading by the TMS9900 CPU
  assign r_reset = ~cru_state[1]; // crubit 1 is exposed as active low to the Raspberry PI for system service reset.
  // For a 32k 27C256 chip, these control bank switching.
  assign dsr_b0 = cru_state[2];   // crubit 2 connects to 32K DSR ROM high address line
  assign dsr_b1 = cru_state[3];   // crubit 3 connects to 32K DSR ROM second highest address line
  
  // Latches && Shift Registers for TI to RPi communication - TC & TD

  // address comparisons
  wire rc_addr = ti_a == RC_ADDR;
  wire rd_addr = ti_a == RD_ADDR;
  wire tc_addr = ti_a == TC_ADDR;
  wire td_addr = ti_a == TD_ADDR;

  // TD Latch
  wire tipi_td_le = (cru_dev_en && ~ti_we && ~ti_memen && td_addr); // Indicates we can latch a write operation from the CPU databus to the TD register.
  wire [0:7] rpi_td; // expose the TD register
  latch_8bit td(tipi_td_le, tp_d, rpi_td); // When the tipi_td_le is high, latch the tp_d 8 bit databus into an internal register, and expose it as rpi_td.

  // TC Latch
  wire tipi_tc_le = (cru_dev_en && ~ti_we && ~ti_memen && tc_addr); // Indicates we can latch a write operation from the CPU databus to the TC register.
  wire [0:7] rpi_tc; // expose the TC register
  latch_8bit tc(tipi_tc_le, tp_d, rpi_tc); // when the tipi_tc_le is high, latch the tp_d 8 bit databus into an internal register, and expose it as rpi_tc.

  // 4 bit bus interface from the RPi to be read by the TI.
  wire [0:7] tipi_db_rd; // RD - register defined inside pi_bus
  wire [0:7] tipi_db_rc; // RC - register defined inside pi_bus
  tipi_4bit_pi_bus pi_bus(r_clk, r_nibrst, r_nib, rpi_td, rpi_tc, tipi_db_rd, tipi_db_rc);

  //-- Databus control
  wire tipi_read = cru_dev_en && ~ti_memen && ti_dbin;  // Indicates a CPU memory read is requested
  wire tipi_dsr_en = tipi_read && ti_a >= LOW_ROM_ADDR && ti_a <= HIGH_ROM_ADDR; // Indicates the CPU read is for the external DSR ROM

  // drive the dsr eprom oe and cs lines.
  assign dsr_en = ~(tipi_dsr_en);
  // drive the 74hct245 oe and dir lines.
  assign db_en = ~(cru_dev_en && ~ti_memen && ti_a >= LOW_ROM_ADDR && ti_a <= HIGH_MEM_ADDR);
  assign db_dir = tipi_read;

  // register to databus output selection
  wire [0:7] rreg_mux_out; 
  mux2_8bit rreg_mux(rc_addr, rd_addr, tc_addr, td_addr, tipi_db_rc, tipi_db_rd, rpi_tc, rpi_td, rreg_mux_out);

  wire dbus_ts_en = cru_state[0] && ~ti_memen && ti_dbin && (ti_a >= RC_ADDR && ti_a <= TD_ADDR);  // Enable signal if CPU is accessing any of the memory mapped IO registers
  tristate_8bit dbus_ts(dbus_ts_en, rreg_mux_out, tp_d); // Set the CPLD databus to high impedance unless we are accessing one of the registers

  assign led0 = cru_state[0] && db_en; // enable the LED if the board is enabled and a databus access is occuring.

endmodule
