
void FUN__text__0048ea90(int param_1,int param_2)

{
  ushort uVar1;
  int iVar2;
  ushort uVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  uint local_18;
  ushort local_14;
  undefined2 uStack_12;
  ushort local_10;
  undefined2 uStack_e;
  ushort local_c;
  undefined2 uStack_a;
  undefined4 local_8;
  
  puVar4 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar2 = FUN__text__004693b0(param_1);
  if (iVar2 == 0) {
    *(undefined1 *)(param_1 + 0x260) = *(undefined1 *)(param_2 + 2);
    for (local_18 = 0; local_18 != 0x14; local_18 = local_18 + 1) {
      *(undefined2 *)(param_1 + 0x262 + local_18 * 2) = 0xffff;
    }
    for (local_18 = 0; local_18 != *(byte *)(param_2 + 3); local_18 = local_18 + 1) {
      uVar3 = ((ushort)*(byte *)(param_2 + 4) & (ushort)(1 << (7U - (char)local_18 & 0x1f))) <<
              ((char)local_18 + 1U & 0x1f);
      _local_c = CONCAT22(uStack_a,uVar3);
      uVar1 = (ushort)*(byte *)(param_2 + local_18 + 5);
      _local_10 = CONCAT22(uStack_e,uVar1);
      uVar3 = uVar3 | uVar1;
      _local_14 = CONCAT22(uStack_12,uVar3);
      if (uVar3 == 0) {
        *(undefined2 *)(param_1 + 0x262 + local_18 * 2) = 0xffff;
      }
      else {
        *(ushort *)(param_1 + 0x262 + local_18 * 2) = uVar3 - 1;
      }
    }
    FUN__text__0048e4d0(param_1,0xc);
    FUN__text__00475370(param_1,0x11,0xffffffff);
  }
  local_8 = 0x48ebe6;
  FUN__text__0056ce80();
  return;
}

