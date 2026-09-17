
void FUN__text__00464400(int param_1,int param_2,int param_3)

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
    FUN__text__00407870(0x5a,6);
    *(undefined2 *)(local_8 + 0x90) = 0xc0;
    *(undefined4 *)(local_8 + 0x94) = 0;
    *(undefined1 *)(local_8 + 0x9f) = 0xff;
    *(undefined1 *)(local_8 + 0x9c) = 0x80;
    *(undefined1 *)(local_8 + 0x9d) = 0x80;
    *(undefined1 *)(local_8 + 0x9e) = 0x80;
    *(undefined2 *)(local_8 + 0xae) = 0x5a;
    *(undefined2 *)(local_8 + 0x70) = *(undefined2 *)(&DAT_0060d13c + local_c * 8);
    *(undefined2 *)(local_8 + 0x72) = *(undefined2 *)(&PTR_DAT_0060d13e + local_c * 2);
    *(undefined2 *)(local_8 + 0xb0) = *(undefined2 *)(&DAT_0060d138 + local_c * 8);
    *(undefined2 *)(local_8 + 0xb2) = *(undefined2 *)(&DAT_0060d13a + local_c * 8);
    *(short *)(local_8 + 0xb4) =
         *(short *)(&DAT_0060d138 + local_c * 8) + *(short *)(local_8 + 0x70);
    *(short *)(local_8 + 0xb6) =
         *(short *)(&DAT_0060d13a + local_c * 8) + *(short *)(local_8 + 0x72);
    local_10 = param_1 + *(short *)(&DAT_0060d148 + local_c * 4);
    local_14 = param_2 + *(short *)(&PTR_DAT_0060d14a + local_c);
    FUN__text__004079c0(local_10,local_14);
  }
  local_8 = 0x46456c;
  FUN__text__0056ce80();
  return;
}

