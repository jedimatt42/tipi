`timescale 1ns / 1ps

module test_tipi_top;

  // Inputs
  reg [0:3] crub;
  reg r_clk;
  reg r_nibrst;
  reg ti_cruclk;
  reg ti_dbin;
  reg ti_memen;
  reg ti_we;
  reg ti_ph3;
  reg [0:15] ti_a;

  // Outputs
  wire led0;
  wire db_dir;
  wire db_en;
  wire dsr_b0;
  wire dsr_b1;
  wire dsr_en;
  wire r_reset;
  wire ti_cruin;
  wire ti_extint;

  // Bidirs
  wire [0:3] r_nib;
  wire [0:7] tp_d;
  
  reg inout_control = 1;
  reg [3:0] r_nib_in = 0;
  assign r_nib = inout_control ? r_nib_in : 4'bz;
  
  reg dbusio_control = 1;
  reg [7:0] dbus_in = 0;
  assign tp_d = dbusio_control ? dbus_in : 8'bz;

  // Instantiate the Unit Under Test (UUT)
  tipi_top uut (
    .led0(led0), 
    .crub(crub), 
    .db_dir(db_dir), 
    .db_en(db_en), 
    .dsr_b0(dsr_b0), 
    .dsr_b1(dsr_b1), 
    .dsr_en(dsr_en), 
    .r_clk(r_clk),
    .r_nibrst(r_nibrst),
    .r_nib(r_nib), 
    .r_reset(r_reset), 
    .ti_cruclk(ti_cruclk), 
    .ti_cruin(ti_cruin), 
    .ti_dbin(ti_dbin), 
    .ti_memen(ti_memen), 
    .ti_we(ti_we), 
    .ti_ph3(ti_ph3), 
    .ti_extint(ti_extint), 
    .ti_a(ti_a), 
    .tp_d(tp_d)
  );
    
  initial begin
    // Initialize Inputs
    crub = 4'hf;
    r_clk = 0;
    r_nibrst = 0;
    ti_cruclk = 1;
    ti_dbin = 1;
    ti_memen = 1;
    ti_we = 1;
    ti_ph3 = 1;
    ti_a = 16'h0000;

    // Wait for global reset to finish
    #1;
    
    // simulate an initial clock cycle
    #1 ti_ph3 = 0;
    #1 ti_ph3 = 1;
    
    test_cru_enable_bit();
    test_cru_reset_bit();
    test_cru_paging();
    test_access_TD();
    test_access_TC();
    
    $display("Success: All tests passed");
    $finish;
  end
  
  task enable_cru_bit_1;
  begin
    #1 ti_a = 16'h1001;
    #1 ti_cruclk = 0;
    #1 ti_cruclk = 1;
  end
  endtask
  
  task test_cru_enable_bit;
  begin
    $display("Test: initial cru enable state");
    #1 if (uut.cru_state != 4'h0) begin
      $display("Error, cru bits should be all 0, was %b", uut.cru_state);
      $finish;
    end
    
    $display("Test: initial bus state while enable bit unset");
    #1 if (tp_d != 8'hz) begin
      $display("Error, expected bus tp_d to be 8'hz, was %b", tp_d);
      $finish;
    end
      
    $display("Test: can read TC while enabled");
    #1 uut.tc.latch_q = 8'h00;
    #1 ti_a = 16'h5ffd;
    #1 ti_memen = 0;
    #1 if (tp_d != 8'hz) begin
      $display("Error, 5ffd should be 8'hz, was %h", tp_d);
      $finish;
    end
    #1 ti_memen = 1;
        
    $display("Test: set crubit 0");
    #1 ti_a = 16'h1001;
    #1 ti_cruclk = 0;
    #1 ti_cruclk = 1;
    #1 if (uut.cru_state[0] != 1) begin
      $display("Error, crubit 0 should be set, was %b", uut.cru_state);
      $finish;
    end
    
    $display("Test: can read TC while enabled");
    #1 uut.tc.latch_q = 8'h55;
    #1 ti_a = 16'h5ffd;
    #1 ti_memen = 0;
    #1 if (tp_d != 8'h55) begin
      $display("Error, 5ffd should be 55, was %h", tp_d);
      $finish;
    end
    #1 ti_memen = 1;
    
    $display("Test: can read cru enabled bit");
    #1 ti_ph3 = 0;
    #1 ti_ph3 = 1;
    #1 if (ti_cruin != 1'bz) begin
      $display("Error, expected ti_cruin to be z, was %b", ti_cruin);
      $finish;
    end
    #1 ti_a = 16'h1000;
    #1 ti_ph3 = 0;
    #1 ti_ph3 = 1;
    #1 if (ti_cruin != 1'b1) begin
      $display("Error, expected ti_cruin to be 1, was %b", ti_cruin);
      $finish;
    end
    
    #1 ti_a = 16'h0000;
  end
  endtask
  
  task test_cru_paging;
  begin
    $display("Test: cru paging crubit 2");
    #1 if (dsr_b0 != 0 || dsr_b1 != 0) begin
      $display("Error, expected dsr_b0 and dsr_b1 to be 0, was %b, %b", dsr_b0, dsr_b1);
      $finish;
    end
    
    #1 ti_a = 16'h1005;
    #1 ti_cruclk = 0;
    #1 ti_cruclk = 1;
    #1 if (dsr_b0 != 1) begin
      $display("Error, dsr_b0 should be high, was %b", dsr_b0);
      $finish;
    end
    #1 ti_a = 16'h1004;
    #1 ti_cruclk = 0;
    #1 ti_cruclk = 1;
    
    $display("Test: cru paging crubit 3");
    #1 ti_a = 16'h1007;
    #1 ti_cruclk = 0;
    #1 ti_cruclk = 1;
    #1 if (dsr_b1 != 1) begin
      $display("Error, dsr_b1 should be high, was %b", dsr_b1);
      $finish;
    end
    #1 ti_a = 16'h1006;
    #1 ti_cruclk = 0;
    #1 ti_cruclk = 1;
  end
  endtask
  
  task test_cru_reset_bit;
  begin
    $display("Test: initial reset output");
    #1 if (r_reset != 1) begin
      $display("Error, r_reset output should be high, was %b", r_reset);
      $finish;
    end
    
    $display("Test: set cru reset bit");
    #1 ti_a = 16'h1003; // lsb (cru_out) is 1
    #1 ti_cruclk = 0;
    #1 ti_cruclk = 1;
    #1 if (uut.cru_state[1] != 1) begin
      $display("Error, crubit 1 (reset) should be set, was %b", uut.cru_state);
      $finish;
    end
    #1 if (r_reset != 0) begin
      $display("Error, r_reset output should be low, was %b", uut.cru_state);
      $finish;
    end
    
    $display("Test: clear cru reset bit");
    #1 ti_a = 16'h1002; // lsb (cru_out) is 0
    #1 ti_cruclk = 0;
    #1 ti_cruclk = 1;
    #1 if (r_reset != 1) begin
      $display("Error, r_reset output should be high, was %b", r_reset);
      $finish;
    end
  end
  endtask
  
  task test_access_TD;
  begin
    $display("Test: read TD");
    enable_cru_bit_1();
    
    #1 uut.td.latch_q = 8'haa;
    #1 ti_a = 16'h5fff;
    #1 ti_memen = 0;
    #1 if (tp_d != 8'haa) begin
      $display("Error, 5fff should be aa, was %h", tp_d);
      $finish;
    end
    #1 ti_memen = 1;
    
    $display("Test: write TD");
    #1 if (uut.td.latch_q != 8'haa) begin
      $display("Error, TD latch register should be aa, was %h", uut.td.latch_q);
      $finish;
    end
    #1 dbus_in = 8'hff;
    #1 dbusio_control = 1;
    #1 ti_memen = 0;
    #1 ti_we = 0;
    #1 ti_we = 1;
    #1 ti_memen = 1;
    #1 dbusio_control = 0;
    #1 ti_a = 16'h0000;
    #1 if (uut.td.latch_q != 8'hff) begin
      $display("Error, TD latch register should be ff, was %h", uut.td.latch_q);
      $finish;
    end
    
    $display("Test: re-read TD");
    #1 ti_a = 16'h5fff;
    #1 ti_memen = 0;
    #1 if (db_dir != 1) begin
      $display("Error, db_dir should be 1, was %b", db_dir);
      $finish;
    end
    #1 if (tp_d != 8'hff) begin
      $display("Error, 5fff should be ff, was %h", tp_d);
      $finish;
    end
    #1 ti_memen = 1;
  end
  endtask

  task test_access_TC;
  begin
    $display("Test: read TC");
    enable_cru_bit_1();
    
    #1 uut.tc.latch_q = 8'h55;
    #1 ti_a = 16'h5ffd;
    #1 ti_memen = 0;
    #1 if (tp_d != 8'h55) begin
      $display("Error, 5ffd should be 55, was %h", tp_d);
      $finish;
    end
    #1 ti_memen = 1;
    
    $display("Test: write TC");
    #1 if (uut.tc.latch_q != 8'h55) begin
      $display("Error, TC latch register should be 55, was %h", uut.tc.latch_q);
      $finish;
    end
    #1 dbus_in = 8'hff;
    #1 dbusio_control = 1;
    #1 ti_memen = 0;
    #1 ti_we = 0;
    #1 ti_we = 1;
    #1 ti_memen = 1;
    #1 dbusio_control = 0;
    #1 ti_a = 16'h0000;
    #1 if (uut.tc.latch_q != 8'hff) begin
      $display("Error, TC latch register should be ff, was %h", uut.tc.latch_q);
      $finish;
    end
    
    $display("Test: re-read TC");
    #1 ti_a = 16'h5ffd;
    #1 ti_memen = 0;
    #1 if (db_dir != 1) begin
      $display("Error, db_dir should be 1, was %b", db_dir);
      $finish;
    end
    #1 if (tp_d != 8'hff) begin
      $display("Error, 5ffd should be ff, was %h", tp_d);
      $finish;
    end
    #1 ti_memen = 1;
  end
  endtask
        
endmodule
