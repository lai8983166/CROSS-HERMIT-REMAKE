
void __thiscall FUN__text__004c4b80(int param_1,int param_2,int param_3)

{
  undefined2 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_a78 [16];
  uint local_a38;
  uint local_a34;
  int local_a30 [10];
  undefined1 auStack_a08 [2552];
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_a78;
  for (iVar3 = 0x29d; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_3;
  local_8 = param_1;
  local_10 = FUN__text__004c2120(*(undefined4 *)(param_1 + 0x18 + param_2 * 0x1c8),
                                 *(undefined2 *)(param_3 + 4));
  if (*(char *)(local_8 + 0x1cc) != -1) {
    local_a34 = local_a34 & 0xffff0000;
    while ((local_a34 & 0xffff) < 10) {
      local_a30[local_a34 & 0xffff] = (int)(auStack_a08 + (local_a34 & 0xffff) * 0xff);
      local_a34 = CONCAT22(local_a34._2_2_,(short)local_a34 + 1);
    }
    uVar1 = FUN__text__004cd5b0(local_10,local_a30);
    local_a38 = CONCAT22(local_a38._2_2_,uVar1);
    local_a34 = local_a34 & 0xffff0000;
    while ((local_a34 & 0xffff) < (local_a38 & 0xffff)) {
      if ((local_a34 & 0xffff) == (local_a38 & 0xffff) - 1) {
        uVar2 = FUN__text__004cb080();
        FUN__text__004cabd0(local_a30[local_a34 & 0xffff],uVar2);
      }
      else {
        FUN__text__004cabd0(local_a30[local_a34 & 0xffff],0);
      }
      local_a34 = CONCAT22(local_a34._2_2_,(short)local_a34 + 1);
    }
  }
  local_8 = 0x4c4d71;
  FUN__text__0056ce80();
  return;
}

