`timescale 1ns / 1ps

`include "latch_8bit.v"

module test_latch_8bit;

  // Inputs
  reg le;
  reg [0:7] din;

  // Outputs
  wire [0:7] dout;

  // Instantiate the Unit Under Test (UUT)
  latch_8bit uut (
    .le(le), 
    .din(din), 
    .dout(dout)
  );

  initial begin
    // Initialize Inputs
    le = 0;
    din = 0;

    // Wait for global reset to finish
    #1;
    
    $display("Test: initial state");
    #1 if (dout != 0) begin
      $display("not initialized properly, dout: %h", dout);
      $finish;
    end
        
    $display("Test: latch a value");
    #1 din = 8'hAA;
    #1 le = 1;
    #1 le = 0;
    #1 if (dout != 8'hAA) begin
      $display("Error dout not 8'hAA, was %h", dout);
      $finish;
    end
    
    $display("Test: latch holds while input changes");
    #1 din = 8'h00;
    #1 if (dout != 8'hAA) begin
      $display("Error dout not 8'hAA, was %h", dout);
      $finish;
    end
    
    $display("Test: verify latches on posedge");
    #1 le = 1;
    #1 if (dout != 0) begin
      $display("Error dout not 0, was %h", dout);
      $finish;
    end
    #1 le = 0;
    
    $display("Success");
    $finish;
  end
      
endmodule