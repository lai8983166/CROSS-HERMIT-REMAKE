
void FUN__text__00458a50(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_3 != -1) {
    local_c = param_3;
    FUN__text__004077c0(DAT_007a49fc);
    FUN__text__00407870(0x5a,7);
    *(undefined2 *)(local_8 + 0x148) = 0xc0;
    *(undefined4 *)(local_8 + 0x14c) = 0;
    *(undefined1 *)(local_8 + 0x157) = 0xff;
    *(undefined1 *)(local_8 + 0x154) = 0x80;
    *(undefined1 *)(local_8 + 0x155) = 0x80;
    *(undefined1 *)(local_8 + 0x156) = 0x80;
    *(undefined2 *)(local_8 + 0x166) = 3;
    *(undefined2 *)(local_8 + 0x128) = *(undefined2 *)(&DAT_0060cb2c + local_c * 8);
    *(undefined2 *)(local_8 + 0x12a) = *(undefined2 *)(&PTR_DAT_0060cb2e + local_c * 2);
    *(undefined2 *)(local_8 + 0x168) = *(undefined2 *)(&DAT_0060cb28 + local_c * 8);
    *(undefined2 *)(local_8 + 0x16a) = *(undefined2 *)(&DAT_0060cb2a + local_c * 8);
    *(short *)(local_8 + 0x16c) =
         *(short *)(&DAT_0060cb28 + local_c * 8) + *(short *)(local_8 + 0x128);
    *(short *)(local_8 + 0x16e) =
         *(short *)(&DAT_0060cb2a + local_c * 8) + *(short *)(local_8 + 0x12a);
    local_10 = param_1 + *(short *)(&DAT_0060cb38 + local_c * 4);
    local_14 = param_2 + *(short *)(&PTR_DAT_0060cb3a + local_c);
    FUN__text__004079c0(local_10,local_14);
  }
  local_8 = 0x458bd1;
  FUN__text__0056ce80();
  return;
}

