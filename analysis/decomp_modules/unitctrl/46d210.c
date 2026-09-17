
void __thiscall FUN__text__0046d210(int param_1,int param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_2 + 0x503) != '\x03') {
    local_c = (short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10) -
              *(short *)(param_1 + 0x2a30e);
    local_10 = ((short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10) -
               *(short *)(param_1 + 0x2a310)) + 0x1e;
    local_8 = param_1;
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined2 *)(local_8 + 0xde688) = 8;
    FUN__text__00407870(0x5a,(int)*(short *)(&DAT_0061878c + (uint)*(byte *)(param_2 + 0x503) * 2));
    *(undefined4 *)(local_8 + 0xde68c) = 1;
    *(undefined1 *)(local_8 + 0xde697) = 0xc0;
    *(undefined1 *)(local_8 + 0xde696) = 0x80;
    *(undefined1 *)(local_8 + 0xde695) = 0x80;
    *(undefined1 *)(local_8 + 0xde694) = 0x80;
    *(undefined2 *)(local_8 + 0xde6a6) = param_3;
    FUN__text__004079c0((int)local_c,(int)local_10);
  }
  local_8 = 0x46d32f;
  FUN__text__0056ce80();
  return;
}

