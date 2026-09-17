
void __fastcall FUN__text__00472960(int param_1)

{
  undefined1 uVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  short local_10;
  undefined2 local_c;
  int local_8;
  
  puVar4 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if ((*(char *)(param_1 + 0x3098c) != '\0') && (*(char *)(param_1 + 0x3098d) == 'd')) {
    uVar3 = *(short *)(param_1 + 0x3098e) * 0x20 + 0x10;
    local_c = (undefined2)uVar3;
    local_10 = *(short *)(param_1 + 0x30990) * 0x10 + 8;
    FUN__text__004728e0(uVar3 & 0xffff,CONCAT22((short)(uVar3 >> 0x10),local_10));
  }
  if ((*(short *)(local_8 + 0x10f9c0) != -1) && (*(short *)(local_8 + 0x10f9c2) != -1)) {
    uVar1 = FUN__text__0040a100(local_8 + 0x109dc8);
    *(undefined1 *)(local_8 + 0x109d84) = uVar1;
    if (*(char *)(local_8 + 0x109d84) != '\0') {
      *(undefined2 *)(local_8 + 0x10f9c2) = 0xffff;
      *(undefined2 *)(local_8 + 0x10f9c0) = 0xffff;
    }
    *(short *)(local_8 + 0x109d8a) = *(short *)(local_8 + 0x109d8a) + 1;
  }
  local_8 = 0x472a60;
  FUN__text__0056ce80();
  return;
}

