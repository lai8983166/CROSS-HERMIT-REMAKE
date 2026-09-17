
void __fastcall FUN__text__00524cb0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0x142) == '\x01') {
    *(short *)(param_1 + 0x14c) =
         *(short *)(param_1 + 0x14c) + (short)(char)(&DAT_0075bab8)[*(ushort *)(param_1 + 0x144)];
    *(short *)(param_1 + 0x144) = *(short *)(param_1 + 0x144) + 1;
    if (0x24 < *(ushort *)(param_1 + 0x144)) {
      *(undefined2 *)(param_1 + 0x144) = 0;
      *(undefined1 *)(param_1 + 0x142) = 2;
    }
  }
  if (*(char *)(param_1 + 0x142) == '\x02') {
    *(ushort *)(param_1 + 0x14c) =
         *(short *)(param_1 + 0x14c) - (ushort)(byte)(&DAT_0075bae0)[*(ushort *)(param_1 + 0x144)];
    *(short *)(param_1 + 0x144) = *(short *)(param_1 + 0x144) + 1;
    if (0x65 < *(ushort *)(param_1 + 0x144)) {
      *(undefined2 *)(param_1 + 0x144) = 0;
      *(undefined1 *)(param_1 + 0x142) = 3;
    }
  }
  local_8 = param_1;
  if (*(char *)(param_1 + 0x142) == '\x03') {
    *(short *)(param_1 + 0x14c) =
         *(short *)(param_1 + 0x14c) + (short)(char)(&DAT_0075bb48)[*(ushort *)(param_1 + 0x144)];
    *(short *)(param_1 + 0x144) = *(short *)(param_1 + 0x144) + 1;
    if (0x17 < *(ushort *)(param_1 + 0x144)) {
      *(undefined2 *)(param_1 + 0x144) = 0;
      *(undefined1 *)(param_1 + 0x142) = 0;
      *(undefined1 *)(param_1 + 0x143) = 1;
      *(undefined2 *)(param_1 + 0x146) = 0;
      *(undefined2 *)(param_1 + 0x14e) = *(undefined2 *)(param_1 + 0x14c);
      FUN__text__00409ff0(param_1 + 0x5a8,0,1,0x80);
    }
  }
  if (*(char *)(local_8 + 0x143) == '\x01') {
    *(ushort *)(local_8 + 0x14e) =
         *(short *)(local_8 + 0x14e) - (ushort)(byte)(&DAT_0075bb60)[*(ushort *)(local_8 + 0x146)];
    *(short *)(local_8 + 0x146) = *(short *)(local_8 + 0x146) + 1;
    if (0x21 < *(ushort *)(local_8 + 0x146)) {
      *(undefined2 *)(local_8 + 0x146) = 0;
      *(undefined1 *)(local_8 + 0x143) = 0;
    }
  }
  local_8 = 0x524f0f;
  FUN__text__0056ce80();
  return;
}

