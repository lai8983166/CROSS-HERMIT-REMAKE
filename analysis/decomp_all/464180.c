
void FUN__text__00464180(int param_1)

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
  if (param_1 != -1) {
    local_c = param_1;
    FUN__text__004077c0(DAT_007a49fc);
    FUN__text__00407870(0x5a,2);
    *(undefined2 *)(local_8 + 0x90) = 0xc0;
    *(undefined4 *)(local_8 + 0x94) = 0;
    *(undefined1 *)(local_8 + 0x9f) = 0xff;
    *(undefined1 *)(local_8 + 0x9c) = 0x80;
    *(undefined1 *)(local_8 + 0x9d) = 0x80;
    *(undefined1 *)(local_8 + 0x9e) = 0x80;
    *(undefined2 *)(local_8 + 0xae) = 99;
    *(undefined2 *)(local_8 + 0x70) = *(undefined2 *)(&DAT_0060d0dc + local_c * 8);
    *(undefined2 *)(local_8 + 0x72) = *(undefined2 *)(&DAT_0060d0de + local_c * 8);
    *(undefined2 *)(local_8 + 0xb0) = *(undefined2 *)(&DAT_0060d0d8 + local_c * 8);
    *(undefined2 *)(local_8 + 0xb2) = *(undefined2 *)(&DAT_0060d0da + local_c * 8);
    *(short *)(local_8 + 0xb4) =
         *(short *)(&DAT_0060d0d8 + local_c * 8) + *(short *)(local_8 + 0x70);
    *(short *)(local_8 + 0xb6) =
         *(short *)(&DAT_0060d0da + local_c * 8) + *(short *)(local_8 + 0x72);
    local_10 = (int)*(short *)(&DAT_0060d118 + local_c * 4);
    local_14 = (int)*(short *)(&DAT_0060d11a + local_c * 4) +
               (int)*(short *)(&DAT_0060d0da + local_c * 8);
    FUN__text__004079c0(local_10,local_14);
  }
  local_8 = 0x4642ef;
  FUN__text__0056ce80();
  return;
}

