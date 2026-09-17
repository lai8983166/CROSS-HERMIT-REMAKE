
void FUN__text__0047d0e0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined2 local_14;
  undefined2 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((-1 < *(short *)(param_1 + 0x4cc)) && (-1 < *(short *)(param_1 + 0x4ce))) {
    local_c = FUN__text__0047a8e0(param_1);
    local_10 = *(undefined2 *)(param_1 + 0x30c);
    local_14 = *(undefined2 *)(param_1 + 0x30e);
  }
  local_8 = 0x47d182;
  FUN__text__0056ce80();
  return;
}

