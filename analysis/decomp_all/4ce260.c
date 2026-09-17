
void FUN__text__004ce260(undefined4 param_1,int param_2,undefined4 param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_178 [16];
  undefined1 local_138 [300];
  uint local_c;
  int local_8;
  
  puVar3 = local_178;
  for (iVar2 = 0x5d; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_2 == -1) {
    local_c._0_2_ = 0;
    param_2._0_2_ = (undefined2)local_c;
  }
  local_c = CONCAT22(local_c._2_2_,(undefined2)param_2);
  FUN__text__004ce090((undefined2)param_2);
  *(undefined1 *)(local_8 + 5 + (local_c & 0xffff) * 0x1c8) = 2;
  FUN__text__004cd7b0(param_1,local_138);
  uVar1 = FUN__text__004500b0(local_138);
  uVar1 = FUN__text__0042abc0(uVar1);
  *(undefined4 *)(local_8 + 8 + (local_c & 0xffff) * 0x1c8) = uVar1;
  uVar1 = FUN__text__004500b0(local_138);
  uVar1 = FUN__text__0042ae20(uVar1);
  iVar2 = (local_c & 0xffff) * 0x1c8;
  *(undefined4 *)(local_8 + 0xc + iVar2) = uVar1;
  FUN__text__004ce560(CONCAT22((short)((uint)iVar2 >> 0x10),(undefined2)local_c),param_3);
  local_8 = 0x4ce353;
  FUN__text__0056ce80();
  return;
}

