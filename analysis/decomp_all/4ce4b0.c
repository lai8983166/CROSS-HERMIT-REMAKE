
void FUN__text__004ce4b0(undefined4 param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 == -1) {
    local_c._0_2_ = 0;
    param_2._0_2_ = (undefined2)local_c;
  }
  local_c = CONCAT22(local_c._2_2_,(undefined2)param_2);
  FUN__text__004ce090((undefined2)param_2);
  *(undefined4 *)(local_8 + 8 + (local_c & 0xffff) * 0x1c8) = param_4;
  *(undefined4 *)(local_8 + 0xc + (local_c & 0xffff) * 0x1c8) = param_1;
  iVar1 = (local_c & 0xffff) * 0x1c8;
  *(undefined1 *)(local_8 + 5 + iVar1) = 1;
  FUN__text__004ce560(CONCAT22((short)((uint)iVar1 >> 0x10),(undefined2)local_c),param_3);
  local_8 = 0x4ce555;
  FUN__text__0056ce80();
  return;
}

