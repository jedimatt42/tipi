# TIPI TI Artist Plus Mouse Driver

This is a mouse driver to enable TIPI mouse with TI Artist Plus.

I don't know or expect it to be compatible with older versions of TI Artist.

## Finding TI Artist Plus

The version of TI Artist Plus I tested this with can be found here:

[whtech](http://ftp.whtech.com/graphics/Inscebot/)  in the disk image.

Extract as TIFILES into a folder on your TIPI named INSCEBOT.

Place the TIPIM file in the folder you extract the disk image into.
Copy aside EXTDSR to JOYST2 (it is different than existing JOYST)

Copy TIPIM to EXTDSR

Now Map DSK1 to the INSCEBOT folder. Plug a USB mouse into your
TIPI, and launch XB. 

## Usage

Left mouse button is fire-button. Rubber-banding is supported so for
tools except D-Draw, click and release, move to preview with rubber band, then click. For most cools, TI Artist warps you back to the
starting point on second click. 

Middle mouse button is space-menu. It activates on release of the button.

Right mouse button restricts movement to a single pixel, so in draw mode you'll never get gaps. But this is more of a throw-back UX compromise. You have to adjust how you move to get sweeping motions.

The speed will never be perfect, but it reminds me of back in the day. For best results use a low DPI mouse as you can find.
